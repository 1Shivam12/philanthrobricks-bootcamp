# Philanthrobricks Bootcamp — Labs

Hands-on labs for the one-day Databricks bootcamp for non-profits. Everything runs on
**Databricks Free Edition** (serverless, Python + SQL only), on a single synthetic dataset —
the fictional **Riverside Food Bank** — that threads through all six modules:

> notebook → governed table → declarative pipeline → a question answered → a dashboard → a live app

## Modules

| # | Notebook | Mode | Produces |
|---|----------|------|----------|
| 0 | `labs/00_setup.py` | run once | `workspace.foodbank` schema + 4 tables |
| 1 | `labs/01_fundamentals.py` | hands-on | your first table (CTAS) |
| 2 | `labs/02_unity_catalog.py` | hands-on | lineage, tags, a governance view |
| 3 | `labs/03_pipeline_sdp.py` | hands-on (pipeline) | `silver_impact` |
| 4 | `labs/04_genie.py` | hands-on (Genie UI) | a Genie Space |
| 5 | `labs/05_dashboard.py` | hands-on (Dashboards UI) | a published dashboard |
| 6 | `labs/06_app.py` + `app/` | hands-on (Apps UI) | the Food Bank Pulse app |

## Start here — clone into your workspace

The whole bootcamp is one public GitHub repo. Attendees pull it in one step:

1. In Databricks: **Workspace → Create → Git folder**
2. Paste the repo URL: `https://github.com/1Shivam12/philanthrobricks-bootcamp`
3. Clone — the notebooks **and** the `data/` CSVs land in your workspace
   (no credentials needed for a public repo on Free Edition)
4. Open **`labs/00_setup`**, attach to **Serverless**, **Run all** — it loads the CSVs into `workspace.foodbank`
5. Work through `labs/01` … `labs/06` in order

That's the point of the design: cloning is the "pull everything" step, and `00_setup` turns the
committed CSVs into tables — no internet egress, which Free Edition restricts anyway.

**Facilitator alternative (bulk import without Git):**
```bash
databricks workspace import-dir labs /Workspace/Users/<you>/philanthrobricks-bootcamp/labs --profile free-edition
```
The Git-folder clone is preferred because it also brings the data.

## Free Edition constraints (designed around)

- **Serverless only**, **Python + SQL only** (no R/Scala), one 2X-Small SQL warehouse.
- **One user per account** — each attendee is alone in their own Free Edition workspace, so
  the "grant to a colleague" story in Module 2 is taught as *syntax*, not a live share.
- **Single `workspace` catalog** — we organise with the `foodbank` **schema**, not new catalogs.
- **One active pipeline per type** — Module 3 is one pipeline each.
- **Apps:** max 3 per account, sleep after 24h idle (redeploy/open to wake).
- **No outbound internet from code** — that's why **Lakeflow Connect is a facilitator demo**,
  not a hands-on lab. Everything else is hands-on.

## Fallback: create `silver_impact` without the pipeline

If a room can't run the Module 3 pipeline, a facilitator can create the table directly so
Modules 4–6 still work:

```sql
CREATE OR REPLACE TABLE workspace.foodbank.silver_impact AS
SELECT date_trunc('month', distribution_date) AS month, site,
       sum(meals_served) AS meals, sum(households_served) AS households, count(*) AS sessions
FROM workspace.foodbank.distributions
GROUP BY 1, 2;
```

## Data dictionary

- **donations** (5,000) — `donation_id, donation_date, food_category, source, weight_kg`
- **distributions** (3,000) — `distribution_id, distribution_date, site, households_served, meals_served`
- **volunteers** (200) — `volunteer_id, name, role, first_active_date, hours_logged`
- **households** (800, *sensitive*) — `household_id, area, household_size, registration_date, support_needs`

Data ships as CSVs in `data/` (regenerate any time with `python data/generate_data.py`).
`00_setup` loads them into tables — deterministic, so every attendee gets identical numbers.
No internet or file upload required beyond the initial Git-folder clone.

## Status

SQL for every module is validated on a live Free Edition workspace. Still needs a live
dry-run before an event: the **Module 3 pipeline** (create + start) and the **Module 6 app**
(deploy + warehouse resource binding). See the deck (`PhilanthrobricksBootcamp.dc.html`) for
facilitator timings and speaker notes.
