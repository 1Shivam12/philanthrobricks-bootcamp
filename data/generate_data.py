"""Generate the Riverside Food Bank CSVs (deterministic, stdlib only).

Run `python data/generate_data.py` to (re)create the four CSVs in this folder.
The data is committed to the repo, so attendees never run this — `00_setup`
just loads the CSVs. Kept here so the data's provenance is transparent.
"""
import csv
import hashlib
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).parent

FOOD_CATEGORIES = ["Fresh produce", "Canned goods", "Dairy", "Bakery", "Dry goods", "Frozen", "Beverages"]
SOURCES = ["Supermarket Co", "Local Farm", "Community Drive", "Corporate Gift", "Individual"]
SITES = ["Riverside Centre", "North Hub", "East Community Hall", "Mobile Unit"]
ROLES = ["Sorter", "Driver", "Front desk", "Coordinator", "Warehouse"]
FIRST_NAMES = ["Alex", "Sam", "Priya", "Jordan", "Mia", "Omar", "Grace", "Leo", "Nina", "Tom"]
LAST_NAMES = ["Patel", "Jones", "Khan", "Smith", "Okafor", "Lee", "Brown", "Garcia", "Ali", "Walsh"]
AREAS = ["Riverside", "Northgate", "Eastfield", "Southbank", "Hilltop"]
SUPPORT_NEEDS = ["Standard", "Dietary", "Accessibility", "Emergency"]


def h(i: int, salt: int) -> int:
    """Deterministic non-negative int from (id, salt) — stable across machines/runs."""
    digest = hashlib.md5(f"{i}:{salt}".encode()).digest()
    return int.from_bytes(digest[:4], "big")


def write(name, header, rows):
    with open(OUT / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}.csv — {len(rows):,} rows")


def d(base: date, days: int) -> str:
    return (base + timedelta(days=days)).isoformat()


# donations — 5,000
write("donations", ["donation_id", "donation_date", "food_category", "source", "weight_kg"], [
    [i, d(date(2025, 1, 1), h(i, 7) % 250), FOOD_CATEGORIES[h(i, 2) % 7], SOURCES[h(i, 3) % 5],
     round((h(i, 4) % 490) / 10.0 + 1, 1)]
    for i in range(5000)
])

# distributions — 3,000
write("distributions", ["distribution_id", "distribution_date", "site", "households_served", "meals_served"], [
    [i, d(date(2025, 1, 1), h(i, 9) % 250), SITES[h(i, 5) % 4],
     (hh := h(i, 6) % 80 + 10), hh * (h(i, 8) % 4 + 2)]
    for i in range(3000)
])

# volunteers — 200
write("volunteers", ["volunteer_id", "name", "role", "first_active_date", "hours_logged"], [
    [i, f"{FIRST_NAMES[h(i, 1) % 10]} {LAST_NAMES[h(i, 15) % 10]}", ROLES[h(i, 10) % 5],
     d(date(2024, 1, 1), h(i, 16) % 500), h(i, 12) % 120 + 5]
    for i in range(200)
])

# households — 800 (sensitive)
write("households", ["household_id", "area", "household_size", "registration_date", "support_needs"], [
    [i, AREAS[h(i, 13) % 5], h(i, 17) % 6 + 1, d(date(2024, 6, 1), h(i, 14) % 400), SUPPORT_NEEDS[h(i, 18) % 4]]
    for i in range(800)
])

print("Done.")
