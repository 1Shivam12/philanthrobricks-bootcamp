# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Setup — Riverside Food Bank data
# MAGIC
# MAGIC You're seeing this because you cloned the bootcamp repo as a **Git folder**
# MAGIC (Workspace → Create → Git folder → the repo URL). That one step brought in every
# MAGIC notebook **and** the data — the CSVs live in the `data/` folder next to these labs.
# MAGIC
# MAGIC This notebook loads those CSVs into the `workspace.foodbank` schema:
# MAGIC
# MAGIC | Table | Rows | What it holds |
# MAGIC |-------|------|---------------|
# MAGIC | `donations` | 5,000 | Food donations — category, source, weight |
# MAGIC | `distributions` | 3,000 | Sessions — site, households served, meals |
# MAGIC | `volunteers` | 200 | Volunteers — role, hours |
# MAGIC | `households` | 800 | **Sensitive** — anonymised households we support |
# MAGIC
# MAGIC **How to run:** attach to **Serverless**, then *Run all*. No internet needed —
# MAGIC the data comes from the files you just cloned.

# COMMAND ----------

import pandas as pd

# Locate the repo's data/ folder relative to THIS notebook (works inside a Git folder).
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()                     # /Workspace-relative path of this notebook
repo_root = nb_path.rsplit("/labs/", 1)[0]
data_dir = "/Workspace" + repo_root + "/data"
print("Loading CSVs from:", data_dir)

# COMMAND ----------

spark.sql("""
  CREATE SCHEMA IF NOT EXISTS workspace.foodbank
  COMMENT 'Riverside Food Bank — Philanthrobricks bootcamp dataset'
""")

# COMMAND ----------

# Each table: its CSV, the columns to parse as dates, and a comment for Catalog Explorer / Genie.
TABLES = {
    "donations":     (["donation_date"],     "Individual food donations received, by category and source"),
    "distributions": (["distribution_date"], "Distribution sessions — meals and households served, by site"),
    "volunteers":    (["first_active_date"], "Food bank volunteers — role and hours contributed"),
    "households":    (["registration_date"], "Anonymised households supported by the food bank — treat as sensitive"),
}

for name, (date_cols, comment) in TABLES.items():
    pdf = pd.read_csv(f"{data_dir}/{name}.csv")
    for c in date_cols:
        pdf[c] = pd.to_datetime(pdf[c]).dt.date          # load as DATE, not string
    sdf = spark.createDataFrame(pdf)
    (sdf.write.mode("overwrite").option("overwriteSchema", "true")
        .saveAsTable(f"workspace.foodbank.{name}"))
    spark.sql(f"COMMENT ON TABLE workspace.foodbank.{name} IS '{comment}'")
    print(f"  ✓ workspace.foodbank.{name:<14} {sdf.count():>5,} rows")

# COMMAND ----------

# MAGIC %md ### Check everything landed

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'donations' AS table, count(*) AS rows FROM workspace.foodbank.donations
# MAGIC UNION ALL SELECT 'distributions', count(*) FROM workspace.foodbank.distributions
# MAGIC UNION ALL SELECT 'volunteers', count(*) FROM workspace.foodbank.volunteers
# MAGIC UNION ALL SELECT 'households', count(*) FROM workspace.foodbank.households
# MAGIC ORDER BY table;

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ You should see **donations 5000 · distributions 3000 · volunteers 200 · households 800**.
# MAGIC You're ready for Module 1.
