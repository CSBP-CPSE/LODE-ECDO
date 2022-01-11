"""
Creates JSON source files for opentabulate according to a variable map csv.

File organization:
    dir/
        json/ (output folder for src files.)
        variablemap.csv
        jsongenerator.py
"""

import csv
import json


def main():
    infraFields = ['source_id', 'source_class', 'surface_type', 'width',
                   'street_name', 'geometry', 'geom_type'] # Info fields for feature
    forceFields = ['prov/terr', 'municipality', 'provider',
                   'source_url', 'licence'] # Forced for all features in data source
    filterFields = ['inscope_filter', 'inscope_value', 'bike_column', 'bike_value',
                    'walk_column', 'walk_value', 'multi_column', 'multi_value'] # Fields to filter by
    input_file = csv.DictReader(open('NS_variablemap.csv')) ## Change varmap per province/territory

    for row in input_file: # Each row is a data source
        if row['subclass'] != "":  # Add subclass to output filename if exists
            OP = open(f"json/{row['prov/terr']}/{row['municipality'].lower().replace(' ', '-')}"
                      f"-{row['subclass'].lower()}.json", "w")
        else:
            OP = open(f"json/{row['prov/terr']}/{row['municipality'].lower().replace(' ', '-')}"
                      f"-{row['class'].lower()}.json", "w")
            
         # Dictionaries for filter, force, schema json fields
        filtdict = {}
        forcedict = {}
        schemadict = {} 

        # Only adding k,v pairs that are not blank
        for f in filterFields:
            if row[f] != '':
                filtdict[f] = row[f]
        for f in forceFields:
            if row[f] != '':
                forcedict[f] = row[f]
        for f in infraFields:
            if row[f] != '':
                schemadict[f] = row[f]

        jsondict = {
            "filename": f"{row['file_name']}.{row['format']}",
            "filetype": row['format'],
            "class": row['class'],
            "filter": filtdict,
            "force": forcedict,
            "schema": schemadict
        }  
        
        # Create the dictionary for the json output
        json_data = json.dumps(jsondict, indent=4)  # Formatting
        OP.write(json_data)  # Write to json
        OP.close()


if __name__ == "__main__":
    main()