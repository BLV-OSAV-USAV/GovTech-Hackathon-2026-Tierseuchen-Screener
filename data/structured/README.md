# Strukturierte Daten für die Challenge

Als möglicher Startpunkt für eine strukturierte Aufbereitung der Tierseuchenmeldungen liegen hier vorbearbeitete Datensätze aus drei internationalen Meldesysteme vor. Die Daten wurden für die Challenge anonymisiert und aufbereitet (blt).

## Übersicht

| Ordner       | Quelle    | Herausgeber | Beinhaltet  |  Einträge |
|--------------|-----------|-------------|----------|----------|
| `adis/`      | [Animal Disease Information System](https://food.ec.europa.eu/animals/animal-diseases/animal-disease-information-system-adis_en)  | Europäische Kommission / EFSA   | Offene Meldungen der EFSA | 1'423 | 
| `wahis/`     | [WAHIS](https://wahis.woah.org/)     | World Organisation for Animal Health (WOAH)    |  Offizielles Meldesystem für anzeigepflichtige Tierseuchen  | 2'100 | 
| `empres_i/`  | [EMPRES-i](https://empres-i.apps.fao.org/)  | Food and Agriculture Organization of the United Nations (FAO)  | Weltweite Meldungen, enthält Zoonosen und ergänzende Info bezgl. Ansteckung von Menschen  | 87'206 | 


## Export
Daten wurden von den jeweiligen Portale heruntergeladen: <br>
* **ADIS**: Vollständiger Export der offenene Meldungen (19.05.26) <br>
* **WAHIS**: Die letzten 2'100 Meldungen (20.05.26) <br>
* **EMPRES-I**: Export mit nachfolgender Suchmaske (21.05.26):<br>

> Disease: "Influenza - Avian" or "African swine fever" or "Lumpy skin disease" <br>
> Region: *Europe* <br>
> Subregion: *All* <br>
> Diagnosis source: *All* <br>
> Diagnosis status: *All* <br>
> Animal type: *All* <br>

## Aufbereitungsschritte

1. Identifierbare Informationen wurden gehashed (Fallnummer, Landes-Fallnummer) mit einer einfachen String-Replace-Methode.
2. Kolumnen mit identifizierbaren Informationen von Personen, Labore und weiteres wurden gelöscht.
3. *Wo nötig*: Spalte "Longitude" + "Latitude" pro Meldung mit einem random Jitter (+/- 0.02, "random uniform") versehen.

### ADIS

<details>

| Wichtige Spalten                                    |Typ       |Beschreibung |
|:----------------------------------------------------|:---------|:------------|
|Reference                                            |character | Referenznummer (wichtig für Rückschlüsse) |
|National reference                                   |character | Referenznummer (Landesspezifisch) |
|**Country/Territory**                                |character | Land |
|**Disease name**                                     |character | Krankeit |
|Disease type                                         |character | Subtyp Krankheit |
|Submitted on                                         |date (yyyy-mm-dd) | Eintrag ins ADIS |
|Administrative division level 1                      |character | z.B. Bundesland |
|Administrative division level 2                      |character | z.B. Verwaltungsbezirk |
|Administrative division level 3                      |character | z.B. Gemeinde |
|**Latitude**                                         |numeric   |             |
|**Longitude**                                        |numeric   |             |
|Approximate location                                 |character | Sind die Koordinaten genau: "true" / "false" |
|Susceptible 1                                        |numeric   | Verdächtige Population (n)  |
|Cases 1                                              |numeric   |             |
|Dead 1                                               |numeric   |             |
|Killed 1                                             |numeric   |             |
|Slaughtered 1                                        |numeric   |             |
|Outbreak year                                        |date (yyyy) |             |
|**Suspicion/Start date**                             |date (yyyy-mm-dd) | Datum Verdachtsmeldung |
|**Confirmation date**                                |date (yyyy-mm-dd) | Datum Bestätigung der Fachperson |
|**End date**                                         |date (yyyy-mm-dd) | Datum Abschluss im Meldesystem  |
|Status Continuing/Resolved                           |character | Abschluss ()            |
|Clinical signs                                       |character |             |
|Diagnostic tests                                     |character | Wurde die Meldung mit einem (Labor)test bestätgt: "true" / "false" |
|Necropsy                                             |character | "true" / "false" |
|Category 1                                           |character | z.B. "Pathogen detection" |
|Subcategory 1                                        |character | z.B. "Nucleic acid detection" |
|Test name 1                                          |character | z.B. "Polymerase chain reaction (PCR)" |
|Test type 1                                          |character | Wo wurde getested: "Laboratory" |
|**Species 1**                                        |character | Lateinischer Name |
|Result date 1                                        |date (yyyy-mm-dd) | Datum Laborbefund |
|Result type 1                                        |character | "Positive" oder "Negativ" |
|Pertinence                                           |character | "EU" oder "EU and WOAH" |

</details>


### EMPRES-i

<details>

| Wichtige Spalten                 |Typ       |Beschreibung |
|:---------------------------------|:---------|:------------|
|Event.ID                          |character | Referenznummer |
|**Disease**                       |character | Krankheit |
|Serotype                          |character | Subtyp Krankheit |
|Region                            |character | Kontinent (nur "Europa") |
|Subregion                         |character | West, Ost, Nord, Südeuropa |
|**Country**                       |character | Land |
|**Admin.level.1**                 |character | z.B. Bundesland|
|**Latitude**                      |numeric   |             |
|**Longitude**                     |numeric   |             |
|Diagnosis.source                  |character | "WOAH (former OIE)", "National authorities" oder "Media" |
|**Diagnosis.status**              |character | "Suspected" oder "Confirmed" |
|**Animal.type**                   |character | z.B. "Wild - Swan", "Domestic - Swine" |
|Species                           |character | z.B. "Wild - Swan", "Domestic - Swine" |
|**Observation.date..dd.mm.yyyy.** |date(dd/mm/yyyy) | Datum Verdachtsmeldung |
|**Report.date..dd.mm.yyyy.**      |character | Datum Bestätigung der Fachperson |
|Humans.affected                   |numeric | Anzahl betroffene Menschen |
|Human.deaths;                     |numeric | Anzahl verstorbene Menschen|

</details>

### WAHIS

<details> 

| Wichtige Spalten         |Typ       |Beschreibung |
|:-------------------------|:---------|:------------|
|**country**               |character | Land |
|eventId                   |character | Referenznummer Event |
|reportId                  |character | Referenznummer Report |
|**disease**               |character | Krankheit |
|subType                   |character | Subtyp Krankheit |
|**eventStartDate**        |date (dd.mm.yyyy) | Datum Verdachtsmeldung |
|**reason**                |character | Grund des Auftretens, s. Liste unten|
|**reportStatus**          |character | "Validated" |
|**submissionDate**        |date (dd.mm.yyyy) | Datum Aufnahme der Meldung |
|reportNumber              |character | Referenznummer intern |


Liste "**reason**": 
* "Recurrence of an eradicated disease"
* "First occurrence in the country"
* "First occurrence in a zone or a compartment"
* "New strain in a zone or a compartment"
* "Recurrence of an eradicated strain" 
* "Recurrence"
* "New strain in the country" 
* "Unusual host species"
* "Emerging disease"

</details>