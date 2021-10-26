# Swagger-Postman Gap Analysis

This script is callable from the command line and takes the swagger spec as input:

```
python -m gapAnalysis your_swagger_spec.json
```

All postman collections are expected to reside in the `./data/` folder.  A full list can be defined in 
a tab-delimited file in the same folder.  (Default expected filename is `collections.csv`).  The following columns
are expected in this order:

1. Postman collection file name
2. Output csv file name
3. Tally column name for the final csv

The resulting gap analysis is saved to the file `API_Gap_Analysis.csv`.

## Testing

Unit tests are present on the record processing and matching parts:

```
python -m unittest process.py
```
