# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Unity Catalog
# MAGIC ### who's allowed to see what
# MAGIC
# MAGIC **Goal:** understand the three-level namespace, describe and document data,
# MAGIC see lineage, learn the `GRANT` syntax, and protect a sensitive table.
# MAGIC
# MAGIC > **Free Edition note:** you have a single `workspace` catalog and you're the only
# MAGIC > user in your account, so we organise with **schemas** (not new catalogs) and learn
# MAGIC > the sharing *syntax* rather than granting to a real colleague. The concepts are identical.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. The three-level address: `catalog . schema . table`
# MAGIC Everything you create has an address. Let's look at ours.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN workspace.foodbank;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Every column, type and comment for a table
# MAGIC DESCRIBE TABLE EXTENDED workspace.foodbank.donations;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Document your data
# MAGIC Good comments make data findable in **Catalog Explorer** — and make Genie smarter later.

# COMMAND ----------

# MAGIC %sql
# MAGIC COMMENT ON TABLE workspace.foodbank.distributions IS
# MAGIC   'Distribution sessions — meals and households served, by site and date';

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Lineage — where did a table come from?
# MAGIC Create a table *from* another table. Unity Catalog records the link automatically.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.foodbank.meals_by_site AS
# MAGIC SELECT site, sum(meals_served) AS total_meals
# MAGIC FROM workspace.foodbank.distributions
# MAGIC GROUP BY site;

# COMMAND ----------

# MAGIC %md
# MAGIC Now open **Catalog** (left nav) → `workspace` → `foodbank` → `meals_by_site` → **Lineage** tab.
# MAGIC You'll see it points back to `distributions`. Lineage is how you answer "if I change this, what breaks?"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Sharing — the `GRANT` syntax
# MAGIC This is how you'd give a colleague read access. The statement runs on Free Edition even
# MAGIC though you're the only user — the point is to learn the shape of it.

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE workspace.foodbank.donations TO `account users`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- See who has what
# MAGIC SHOW GRANTS ON TABLE workspace.foodbank.donations;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. 🛠️ Protect the sensitive table
# MAGIC `households` is sensitive — it describes the people we support. Tag it, then create a
# MAGIC **public view** that hides the sensitive `support_needs` column. Sharing the *view*
# MAGIC (not the table) is the simplest way to give people only what they need.

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE workspace.foodbank.households SET TAGS ('sensitivity' = 'restricted');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW workspace.foodbank.households_public AS
# MAGIC SELECT household_id, area, household_size, registration_date
# MAGIC FROM workspace.foodbank.households;   -- support_needs deliberately excluded

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The view shows everything EXCEPT the sensitive column
# MAGIC SELECT * FROM workspace.foodbank.households_public LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC You can now organise data into schemas, document it, read lineage,
# MAGIC use `GRANT`, and protect sensitive data behind a view.
# MAGIC
# MAGIC **Next:** how do we get *more* data in and keep it fresh — without doing it by hand? That's **Lakeflow**.
