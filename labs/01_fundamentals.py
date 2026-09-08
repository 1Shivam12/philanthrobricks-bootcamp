# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Databricks Fundamentals
# MAGIC ### the lakehouse, and finding your way around
# MAGIC
# MAGIC **Goal:** get comfortable in the workspace — run a notebook on serverless compute,
# MAGIC query the sample data in both SQL and Python, and create your first table.
# MAGIC
# MAGIC **Before you start:** run `00_setup` once so the `workspace.foodbank` data exists.
# MAGIC Attach this notebook to **Serverless** (top right).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. A notebook is just cells you run
# MAGIC This is a cell. Click it and press **Shift+Enter** to run it and move on.
# MAGIC The result appears right underneath — no setup, no servers to manage.

# COMMAND ----------

print("Hello from the Riverside Food Bank bootcamp 👋")
1 + 1

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Look at the data — in SQL
# MAGIC Cells default to Python. Start a cell with `%sql` to write SQL instead.
# MAGIC Your food-bank data lives at the three-level address `workspace.foodbank.<table>`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.foodbank.donations LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. The same data — in Python
# MAGIC `spark.table(...)` reads any table into a DataFrame. Same data, different tool —
# MAGIC that's the lakehouse: one copy, many ways to work with it.

# COMMAND ----------

df = spark.table("workspace.foodbank.donations")
print(f"{df.count():,} donations")
display(df.groupBy("food_category").count().orderBy("count", ascending=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. 🛠️ Your turn — create your first table
# MAGIC Run the cell below to create a summary table: total weight donated per category.
# MAGIC `CREATE TABLE ... AS SELECT` (CTAS) saves the result of a query as a new table.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.foodbank.my_donations_summary AS
# MAGIC SELECT
# MAGIC   food_category,
# MAGIC   count(*)               AS donations,
# MAGIC   round(sum(weight_kg))  AS total_kg
# MAGIC FROM workspace.foodbank.donations
# MAGIC GROUP BY food_category
# MAGIC ORDER BY total_kg DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Preview the table you just made
# MAGIC SELECT * FROM workspace.foodbank.my_donations_summary;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Try it yourself (2 min)
# MAGIC In the empty cell below, write a query against `workspace.foodbank.distributions`.
# MAGIC Idea: which **site** served the most meals? *(hint: `SUM(meals_served)`, `GROUP BY site`, `ORDER BY ... DESC`)*

# COMMAND ----------

# MAGIC %sql
# MAGIC -- your query here

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC You can now move around the workspace, run a notebook on serverless compute,
# MAGIC query data in SQL and Python, and **create a table** from a query.
# MAGIC
# MAGIC **Next:** you made a table — so who's allowed to see it? That's **Unity Catalog**.
