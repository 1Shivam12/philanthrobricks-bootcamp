# Databricks notebook source
# MAGIC %md
# MAGIC # 03 · Lakeflow + Spark Declarative Pipelines
# MAGIC ### getting data in, and keeping it fresh
# MAGIC
# MAGIC This module has **two halves**:
# MAGIC
# MAGIC 1. **Lakeflow Connect** *(watch — the facilitator drives this)*. Connectors reach out to
# MAGIC    external systems (Salesforce, databases, files). Free Edition keeps outbound traffic
# MAGIC    locked to trusted domains, so we demo Connect from a full workspace rather than here.
# MAGIC 2. **Spark Declarative Pipeline (SDP)** *(hands-on — you build this)*. You describe the
# MAGIC    tables you want; the pipeline figures out how to build and refresh them.
# MAGIC
# MAGIC ---
# MAGIC ### ⚠️ This notebook is a *pipeline source*, not a run-all notebook
# MAGIC The cells below define pipeline datasets. Don't run them cell-by-cell — instead attach
# MAGIC this notebook to a **Lakeflow Declarative Pipeline** and start it:
# MAGIC
# MAGIC 1. Left nav → **Jobs & Pipelines** → **Create** → **ETL / Declarative pipeline**
# MAGIC 2. **Serverless**, default catalog **`workspace`**, default schema **`foodbank`**
# MAGIC 3. Add this notebook as the pipeline **source**
# MAGIC 4. Click **Start** and watch the graph build `bronze → silver`
# MAGIC
# MAGIC > Free Edition allows **one active pipeline per type**, so one pipeline each is perfect.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze — raw, as it arrives
# MAGIC A thin pass-through of the source tables. In a real ingest these would be fed by
# MAGIC Lakeflow Connect or Auto Loader; here we read the seeded tables.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW bronze_distributions
# MAGIC   COMMENT 'Raw distribution sessions'
# MAGIC AS SELECT * FROM workspace.foodbank.distributions;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW bronze_donations
# MAGIC   COMMENT 'Raw food donations'
# MAGIC AS SELECT * FROM workspace.foodbank.donations;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver — cleaned and aggregated
# MAGIC The table the rest of the day uses: monthly meals and households served, per site.
# MAGIC Change the `GROUP BY` and restart the pipeline to see it rebuild.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW silver_impact
# MAGIC   COMMENT 'Monthly meals and households served, by site'
# MAGIC AS
# MAGIC SELECT
# MAGIC   date_trunc('month', distribution_date) AS month,
# MAGIC   site,
# MAGIC   sum(meals_served)      AS meals,
# MAGIC   sum(households_served) AS households,
# MAGIC   count(*)               AS sessions
# MAGIC FROM bronze_distributions
# MAGIC GROUP BY 1, 2;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC After the pipeline runs you'll have `workspace.foodbank.silver_impact` — a table that
# MAGIC refreshes itself. That's the table Genie, the dashboard, and the app all use next.
# MAGIC
# MAGIC **No time for the pipeline?** A facilitator can create `silver_impact` directly with the
# MAGIC fallback query in the repo `README.md`, so Modules 4–6 still work.
# MAGIC
# MAGIC **Next:** ask this fresh table questions in plain English — that's **Genie**.
