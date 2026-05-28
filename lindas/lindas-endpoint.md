### Write to LINDAS

``` bash
curl -u "$LINDAS_USERNAME:$LINDAS_PW" \
  -X POST \
  -H "Content-Type: text/turtle" \
  --data-binary @test-upload.ttl \
  "https://int.graphdb.lindas.admin.ch/repositories/lindas/rdf-graphs/service?graph=https://lindas.admin.ch/fsvo/govtech26-tierseuchen-screener"
```

github-secrets:
- LINDAS_USERNAME
- LINDAS_PW

https://cognizone.atlassian.net/wiki/spaces/LEKB1/pages/150929410/Authentication+for+Write+Endpoints

https://lindas.admin.ch/fsvo/fsvo-govtech26-tierseuchen-screener


### Read from LINDAS

``` bash
  curl -G "https://int.lindas.admin.ch/query" \
    --data-urlencode 'query=SELECT * WHERE { GRAPH <https://lindas.admin.ch/fsvo/govtech26-tierseuchen-screener> { ?s ?p ?o . } } LIMIT 10' \
    -H "Accept: application/sparql-results+json"
```

oder auf https://int.lindas.admin.ch/sparql/

```
SELECT * WHERE {
  GRAPH <https://lindas.admin.ch/fsvo/govtech26-tierseuchen-screener> {
    ?s ?p ?o .
  }
}
```