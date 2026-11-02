# CivicFix Lite

A small API for reporting and resolving civic issues (potholes, streetlights, garbage) in Tier 2/3 cities.
Built as a team internship project on NexusAI.

## Features
- Report an issue with a category, location and description
- Automatic priority score (category weight, age, number of reports)
- List, filter and update issues; mark them resolved
- Duplicate detection for reports at the same place

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```bash
pytest -q
```

## Team
| Member | Area |
|---|---|
| UAT Hiring Test 1 | Issue API and data model |
| UAT Hiring Test 2 | Priority scoring and analytics |
| UAT Hiring Test 3 | Duplicate detection and tests |
