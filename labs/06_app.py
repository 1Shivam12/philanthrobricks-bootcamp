# Databricks notebook source
# MAGIC %md
# MAGIC # 06 · Databricks Apps
# MAGIC ### put it in someone's hands
# MAGIC
# MAGIC The capstone: wrap the data you've built in a small web app your team can actually use —
# MAGIC the **Food Bank Pulse**. It shows headline numbers, meals over time and donations by
# MAGIC category, with a site filter. Built and deployed right on the platform.
# MAGIC
# MAGIC The app code lives in the repo `app/` folder (`app.py`, `app.yaml`, `requirements.txt`).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🛠️ Create and deploy
# MAGIC 1. Left nav → **Compute** → **Apps** → **Create app** → start from the **Streamlit** template
# MAGIC 2. Replace the template files with the three in `app/` (or upload them to the app's folder)
# MAGIC 3. **Edit → Resources → add a SQL warehouse**, name the resource **`sql-warehouse`**
# MAGIC    (this is what `app.yaml` reads for `DATABRICKS_WAREHOUSE_ID`)
# MAGIC 4. **Deploy**, then open the app URL — you should see live food-bank numbers
# MAGIC
# MAGIC The app reads `workspace.foodbank.distributions` and `.donations`, so it works whether or
# MAGIC not you ran the Module 3 pipeline.

# COMMAND ----------

# MAGIC %md
# MAGIC ### What to notice
# MAGIC - It's **interactive** — the site filter re-queries live, it's not a static page.
# MAGIC - It runs **on the platform**, next to the data — nothing else to host.
# MAGIC - It's **governed** — the app can only see what its identity is granted in Unity Catalog.
# MAGIC
# MAGIC > **Free Edition notes:** you can have up to **3 apps** per account, and an app **sleeps
# MAGIC > after 24h idle** — just redeploy (or open it) to wake it up.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch (optional)
# MAGIC - Add a **volunteers** tab (hours by role) from `workspace.foodbank.volunteers`.
# MAGIC - Add a Genie-style question box using the Genie Conversation API.
# MAGIC
# MAGIC ## ✅ Checkpoint — you did the whole platform
# MAGIC From a blank workspace this morning to a **live app** now: notebook → governed table →
# MAGIC pipeline → a question answered → a dashboard → an app. All on an account you keep.
