# Databricks notebook source
# MAGIC %md
# MAGIC # 04 · Genie
# MAGIC ### ask your data a question, in plain English
# MAGIC
# MAGIC Genie sits on top of your tables, turns a plain-English question into SQL, runs it,
# MAGIC and shows the answer — and always shows you the query it wrote.
# MAGIC
# MAGIC This module is mostly done in the **Genie UI**, not this notebook. Use the notebook to
# MAGIC prep, then follow the steps below.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Make sure your tables are well described
# MAGIC Genie reads table and column comments — good descriptions make it much smarter.
# MAGIC This should return comments for your food-bank tables (added in setup + Module 2).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT table_name, comment
# MAGIC FROM system.information_schema.tables
# MAGIC WHERE table_catalog = 'workspace' AND table_schema = 'foodbank'
# MAGIC ORDER BY table_name;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. 🛠️ Create a Genie Space
# MAGIC 1. Left nav → **Genie** → **New**
# MAGIC 2. Add tables from **`workspace.foodbank`** — start with `distributions`, `donations`,
# MAGIC    `silver_impact` and `volunteers` *(skip the sensitive `households` table)*
# MAGIC 3. Pick the **Serverless Starter Warehouse**
# MAGIC 4. Give it a name: **Riverside Food Bank**
# MAGIC
# MAGIC ## 3. Ask these questions
# MAGIC Type them in the Genie chat, one at a time:
# MAGIC
# MAGIC - *How many meals did we serve in total?*
# MAGIC - *Which site served the most households?*
# MAGIC - *What are the top 3 food categories by weight donated?*
# MAGIC - *How many volunteer hours were logged, by role?*
# MAGIC - *Show meals served per month as a chart*
# MAGIC
# MAGIC ## 4. Look behind the answer
# MAGIC On any answer, click **Show generated code** to see the SQL Genie wrote. Try editing it
# MAGIC and re-running — you're always in control of the query.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Tips for good answers
# MAGIC - **Give context:** in the Space's *Instructions*, add a line like
# MAGIC   *"meals_served is the number of meals; a distribution is one session at one site."*
# MAGIC - **Add example questions** in the Space so Genie learns your language.
# MAGIC - **Trust, but check:** glance at the SQL before you rely on a number in a meeting.
# MAGIC
# MAGIC > **Free Edition note:** the AI model behind Genie is shared. If a question is briefly
# MAGIC > busy, just ask again — it clears quickly.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC You created a Genie Space, asked questions in plain English, and read the SQL behind an answer.
# MAGIC
# MAGIC **Next:** turn a good answer into a page your team can check any time — a **dashboard**.
