"""Incremental file ingestion shared by the Bronze notebooks.

Raw files land in an append-only archive inside a Unity Catalog Volume (one folder per arrival month,
files never overwritten). Bronze ingests them in two steps:

1. ``register_new_files``: Auto Loader (``cloudFiles``, format ``binaryFile``) with ``trigger(availableNow=True)``
   records every file it has not seen before in a file register table (path, size, modification time, SHA-256)
   and stops. The checkpoint is what makes this exactly-once across runs. ``binaryFile`` is used because Excel
   is not a native Auto Loader format; the workbook is parsed afterwards by the notebook.
2. ``pending_files``: registered files whose ``_source_path`` is not yet in the Bronze target. The notebook
   parses each one and appends it in a single write, so a run that fails after step 1 is completed by the next run.
"""
from pyspark.sql import functions as F


def register_new_files(spark, source_dir, glob, checkpoint, files_table, comment=None):
    """Register files in ``source_dir`` (recursive) matching ``glob`` that Auto Loader has not seen. Returns the count."""
    query = (spark.readStream.format("cloudFiles")
             .option("cloudFiles.format", "binaryFile")
             .option("pathGlobFilter", glob)
             .load(source_dir)
             .select(F.col("path").alias("_source_path"),
                     F.element_at(F.split("path", "/"), -1).alias("_source_file"),
                     F.col("length").alias("_source_bytes"),
                     F.col("modificationTime").alias("_source_modified_ts"),
                     F.sha2("content", 256).alias("_source_sha256"),
                     F.current_timestamp().alias("_registered_ts"))
             .writeStream
             .option("checkpointLocation", checkpoint)
             .trigger(availableNow=True)
             .toTable(files_table))
    query.awaitTermination()
    progress = query.recentProgress or []
    if comment:
        spark.sql(f"COMMENT ON TABLE {files_table} IS '{comment}'")
    return sum((p.get("numInputRows") or 0) for p in progress)  # empty micro-batches report None


def pending_files(spark, files_table, target_table):
    """Registered files not yet captured in ``target_table``, oldest arrival first."""
    files = spark.table(files_table).dropDuplicates(["_source_path"])
    if spark.catalog.tableExists(target_table):
        files = files.join(spark.table(target_table).select("_source_path").distinct(), "_source_path", "left_anti")
    return files.orderBy("_source_modified_ts").collect()


def local_path(source_path):
    """Auto Loader reports ``dbfs:/Volumes/...``; Python file APIs need ``/Volumes/...``."""
    return source_path.removeprefix("dbfs:")


def lineage(df, f, batch_id, ingestion_ts):
    """Add the standard Bronze lineage columns for registered file ``f``."""
    return (df.withColumn("_source_file", F.lit(f["_source_file"]))
              .withColumn("_source_path", F.lit(f["_source_path"]))
              .withColumn("_source_sha256", F.lit(f["_source_sha256"]))
              .withColumn("_source_modified_ts", F.lit(f["_source_modified_ts"]).cast("timestamp"))
              .withColumn("_ingestion_ts", F.lit(ingestion_ts).cast("timestamp"))
              .withColumn("_batch_id", F.lit(batch_id)))
