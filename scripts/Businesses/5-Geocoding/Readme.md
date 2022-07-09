# Purpose 

The goal of this step is to ensure that each data source has lat/lon coordinates and street address. 

We use geocoding to try and find lat/lon coordinates from facility names and street addresses.  

We use reverse geocoding to find street addresses from lat/lon coordinates.

We have several options for geocoding:
- Open Street Map's nominatim
- StatCan's National Address Register

# Use

1_geocode.py takes combined.csv as its primary input. The final output is "reverse_geocoded_{DATE}.csv". It can read previous outputs to check for previously past coded results.

# Output

Location addresses are given in the columns prefixed with "osm_"

The geo_source columns indicates the 
- Source: geography from source data
- osm_facility_name: osm geocoded from facility name
- osm_address: osm geocoded from facility name
- gc_street_address: osm geocoded from the street address
- osm_city: gc api geocoded from the city
- osm_reverse: osm reverse geocoded from lat/lon
- errornous: no api request or address outside of canada

# API use

Note that OSM advises making limited use of the API. They ask that calls be made no more than once per second and to limit repeated inquiries.