# ODHF Processing steps

## Pre-processing and OpenTabulate

1. Create list of all sources
2. Import original data - manually or with scripts
3. Initial preprocessing
    - Format latitude and longitude as separate columns
    - Convert format to CSV 
    - Encode CSV with utf-8
    - Filter out data not related to health
3. Fill out variable map
4. Run OpenTabulate
    - json file generation, configuration file, csv of data ingested 
    - see OpenTab readme for more details
5. Merge files
    - merge data sources
    - more pre-processing for postal code, facility type
6. Parse 
    - parse addresses if applicable
    - merge columns if original data already parsed
7. Geocode addresses
    - ensure every address has a lat/long coordinate
    - provide an address if only lat/long available
    - a variety of options here - we are using Nominatm (OSM) and the National Address Register API (new)
8. Assign CSDs
    - use lat/long point to locate facility within a CSD
9. Remove true duplicates
10. Deduplication
    - create pairs
    - fuzzy matching
11. Final clean and validation


Other:
- assign NAICS code
