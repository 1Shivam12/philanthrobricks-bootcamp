# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · AI/BI Dashboards
# MAGIC ### turn answers into something you can share
# MAGIC
# MAGIC A dashboard is a page of charts and numbers built on your data. It refreshes on its own,
# MAGIC so the team always sees today's picture. Built in the **Dashboards UI** — this notebook
# MAGIC gives you the exact queries to paste in.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🛠️ Build it
# MAGIC 1. Left nav → **Dashboards** → **Create dashboard**
# MAGIC 2. **Data** tab → add a dataset for each query below (paste the SQL)
# MAGIC 3. **Canvas** tab → add a widget for each, pick the chart type suggested
# MAGIC 4. **Publish** (top right) → open the published view
# MAGIC
# MAGIC The three queries below are pre-tested against `workspace.foodbank`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Dataset A — headline numbers  → *Counter* widgets
# MAGIC Total meals served and households reached.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT sum(meals_served) AS total_meals,
# MAGIC        sum(households_served) AS total_households,
# MAGIC        count(*) AS sessions
# MAGIC FROM workspace.foodbank.distributions;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Dataset B — donations by category  → *Bar* chart

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT food_category, round(sum(weight_kg)) AS total_kg
# MAGIC FROM workspace.foodbank.donations
# MAGIC GROUP BY food_category
# MAGIC ORDER BY total_kg DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Dataset C — meals over time  → *Line* chart

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT date_trunc('month', distribution_date) AS month,
# MAGIC        sum(meals_served) AS meals
# MAGIC FROM workspace.foodbank.distributions
# MAGIC GROUP BY month
# MAGIC ORDER BY month;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Optional — meals by site  → *Bar* chart (add a site filter to the page)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT site, sum(meals_served) AS meals
# MAGIC FROM workspace.foodbank.distributions
# MAGIC GROUP BY site
# MAGIC ORDER BY meals DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Checkpoint
# MAGIC You built a dashboard with a headline counter, a bar chart and a line chart, and published it.
# MAGIC
# MAGIC > **Free Edition note:** you can share within your own account — enough to show the room.
# MAGIC
# MAGIC **Next:** a dashboard shows the picture; sometimes people need to *do* something. That's an **app**.
