# ADIS Outbreaks Schema

Source file: `data/structured/adis/adis-outbreaks-20260519.csv`

The source CSV contains 1,423 data rows and 46 columns. It is encoded with a UTF-8 BOM, uses semicolons as delimiters, double quotes for quoted fields, and comma decimal notation for coordinates.

## Type Inference Notes

- `string`: free text or categorical text.
- `date`: ISO calendar date in `YYYY-MM-DD` format.
- `integer`: whole-number count or year.
- `decimal`: decimal number stored with a comma decimal separator in the CSV.
- `boolean`: literal `true` or `false`.
- Null values were inferred from blank-like markers: `NaN`, `N/A`, and empty values.

## Columns

| Column | Inferred type | Nullable | Non-null | Null | Distinct | Example values |
|---|---|:---:|---:|---:|---:|---|
| `Reference` | `string` | no | 1423 | 0 | 1423 | IT-SHB-2025-xghqg<br>DE-HPAI(NON-P)-2026-xsyaz<br>DE-HPAI(NON-P)-2026-yy25e |
| `National reference` | `string` | yes | 1127 | 296 | 1127 | SHB_2025_0016-zutgb<br>26-015-a0jke<br>26-015-mqw20 |
| `Country/Territory` | `string` | no | 1423 | 0 | 31 | Italien<br>Deutschland<br>Island |
| `Typ` | `string` | no | 1423 | 0 | 2 | Secondary<br>Primary |
| `Disease name` | `string` | no | 1423 | 0 | 19 | Aethina tumida (Inf. with)(Small hive beetle)(2006-)<br>HPAI(NON-P) in Wild Birds<br>Mycobacterium tuberculosis complex (Inf. with)(2019-) |
| `Disease type` | `string` | yes | 301 | 1122 | 4 | H5N1<br>H5N5<br>RABV |
| `Epidemiological unit` | `string` | yes | 1319 | 104 | 9 | Apiary<br>Not applicable<br>Body of water |
| `Submitted on` | `date` | no | 1423 | 0 | 25 | 2026-05-13<br>2026-05-19<br>2026-04-20 |
| `Modified on` | `date` | no | 1423 | 0 | 25 | 2026-05-13<br>2026-05-19<br>2026-04-20 |
| `Administrative division level 1` | `string` | no | 1423 | 0 | 170 | Sicily<br>Nordrhein-Westfalen<br>Hessen |
| `Administrative division level 2` | `string` | yes | 1363 | 60 | 368 | Messina<br>Ennepe-Ruhr-Kreis<br>Hersfeld-Rotenburg |
| `Administrative division level 3` | `string` | yes | 865 | 558 | 313 | Messina<br>Witten<br>Heringen (Werra) |
| `Outbreak occurring inside an already restricted zone` | `boolean` | yes | 1346 | 77 | 2 | true<br>false |
| `Latitude` | `decimal` | yes | 1319 | 104 | 1139 | 38,2093070701438<br>51,4100000000000<br>50,9100000000000 |
| `Longitude` | `decimal` | yes | 1319 | 104 | 1155 | 15,521267481292263<br>7,350000000000000<br>10,010000000000000 |
| `Approximate location` | `boolean` | yes | 1319 | 104 | 2 | false<br>true |
| `Location` | `string` | yes | 1319 | 104 | 511 | Messina<br>Witten<br>Heringen (Werra) |
| `Wildlife type 1` | `string` | yes | 1133 | 290 | 2 | Wild<br>Captive |
| `Production Type 1` | `string` | yes | 81 | 1342 | 2 | Poultry<br>Non-poultry birds |
| `Water type 1` | `string` | yes | 0 | 1423 | 0 |  |
| `Production system 1` | `string` | yes | 1 | 1422 | 1 | Semi-closed (e.g. ponds or raceways) |
| `Measuring unit 1` | `string` | no | 1423 | 0 | 2 | Hives<br>Tiere |
| `Susceptible 1` | `integer` | yes | 288 | 1135 | 197 | 1<br>125<br>181 |
| `Cases 1` | `integer` | yes | 1393 | 30 | 137 | 1<br>2<br>33 |
| `Dead 1` | `integer` | yes | 1256 | 167 | 75 | 0<br>1<br>2 |
| `Killed 1` | `integer` | yes | 730 | 693 | 118 | 0<br>1<br>2 |
| `Slaughtered 1` | `integer` | yes | 501 | 922 | 4 | 0<br>2<br>1 |
| `Vaccinated 1` | `integer` | yes | 351 | 1072 | 3 | 0<br>21<br>42 |
| `Outbreak year` | `integer` | no | 1423 | 0 | 2 | 2025<br>2026 |
| `Suspicion/Start date` | `date` | no | 1423 | 0 | 83 | 2025-12-10<br>2026-01-27<br>2026-01-19 |
| `Confirmation date` | `date` | no | 1423 | 0 | 57 | 2025-12-24<br>2026-01-30<br>2026-02-02 |
| `End date` | `date` | yes | 784 | 639 | 56 | 2026-01-30<br>2026-04-17<br>2026-02-10 |
| `Status Continuing/Resolved` | `string` | no | 1423 | 0 | 2 | Continuing<br>Resolved |
| `Suspicion` | `boolean` | no | 1423 | 0 | 1 | false |
| `Clinical signs` | `boolean` | no | 1423 | 0 | 2 | true<br>false |
| `Diagnostic tests` | `boolean` | no | 1423 | 0 | 2 | true<br>false |
| `Necropsy` | `boolean` | no | 1423 | 0 | 2 | false<br>true |
| `Category 1` | `string` | yes | 1358 | 65 | 3 | Other (other than pathogen or antibody detection)<br>Pathogen detection<br>Antibody detection |
| `Subcategory 1` | `string` | yes | 1358 | 65 | 7 | Other (tests other than pathogen or antibody detection)<br>Nucleic acid detection<br>Antibody detection tests |
| `Test name 1` | `string` | yes | 1358 | 65 | 18 | Morphological identification<br>Real-time polymerase chain reaction (real-time PCR)<br>Polymerase chain reaction (PCR) |
| `Test type 1` | `string` | yes | 1358 | 65 | 2 | Laboratory<br>Field |
| `Laboratory type 1` | `string` | yes | 1357 | 66 | 5 | National Reference Laboratory<br>Private Laboratory<br>Regional Reference Laboratory |
| `Species 1` | `string` | yes | 1358 | 65 | 48 | Bees<br>Anser anser<br>Anserinae (unidentified) |
| `Result date 1` | `date` | yes | 1358 | 65 | 56 | 2025-12-24<br>2026-01-30<br>2026-01-31 |
| `Result type 1` | `string` | yes | 1358 | 65 | 2 | Positive<br>Negative |
| `Pertinence` | `string` | no | 1423 | 0 | 2 | EU and WOAH<br>EU |
