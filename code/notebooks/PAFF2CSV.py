import json
import os
from pathlib import Path

SCHEMA = """
| Column | Type | Nullable | Index | Notes |
|--------|------|----------|-------|-------|
| `id` | bigint | no | PK | Auto-increment |
| `source` | string | no | | Data source identifier (e.g. `gefluegelnews`, `padi_web`) |
| `title` | string | no | | Article headline |
| `url` | string | yes | | Canonical article URL |
| `teaser` | string | yes | | Short excerpt / lead |
| `body` | longText | yes | | Full article text |
| `report_date` | date | no | | Publication date |
| `admin_level_1` | string | yes | yes | Geographic admin level 1 |
| `admin_level_2` | string | yes | | Admin level 2 |
| `admin_level_3` | string | yes | | Admin level 3 |
| `relevance_score` | decimal(5,2) | yes | | Numeric relevance index |
| `relevance_score_string` | string | yes | | Categorical relevance (e.g. high, medium, low) |
| `distance_km` | decimal(8,2) | yes | | Distance from reference point |
| `created_at` | timestamp | no | | |
| `updated_at` | timestamp | no | | |
"""

PAFF_JSONS_DIR = Path("../../data/unstructured/PAFF_extracted")

paff_jsons = [f for f in os.listdir(PAFF_JSONS_DIR) if f.lower().endswith('.json')]

for pj in paff_jsons:
    with open(PAFF_JSONS_DIR / pj, 'r') as f:
        try:
            paff = json.loads(f.read())
            print(paff)
        except Exception as e:
            print(f"Problem with json parsing {PAFF_JSONS_DIR / pj}: {e}")
            exit(1)

    text = paff['extracted_md']
    print(text)
    #print(text.encode().decode('string_escape'))



'id'
'source'
'title'
'url'
'teaser'
'body'
'report_date'
'admin_level_1'
'admin_level_2'
'admin_level_3'
'relevance_score'
'relevance_score_string'
'distance_km'
'created_at'
'updated_at'
