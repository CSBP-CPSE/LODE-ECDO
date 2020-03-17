import csv


def main():
    otherFields = ['library_name', 'library_type', 'address_full', 'longitude', 'latitude']
    #using hours to hold address string, comdist to hold city, region to hold province, and county to hold data provider
    addressFields = ['unit','street_no','street_name','postcode','city','prov/terr']
    forceFields = ['file_type', 'data_city', 'data_prov/terr', 'data_provider']
    input_file = csv.DictReader(open('variableMap.csv'))
    for row in input_file:
        OP = open("json/" + row['File'].split('.')[0] + ".json","w")
        OP.write('{ \n')
        OP.write('    "localfile": "' + row['File'] + '",\n')
        OP.write('    "url":"",\n')
        OP.write('    "format":"csv",\n')
        OP.write('    "database_type": "library",\n')
        OP.write('    "info": {\n')
        first = True
        other = False
        force = False
        for f in otherFields:
            if row[f] != '':
                if first:  first = False
                else: OP.write(',\n')
                OP.write('        "'+ f +'": "' + row[f] + '"')
                other = True
        for f in forceFields:
            if row[f] != '':
                if first:  first = False
                else: OP.write(',\n')
                if row['File'] != "AllLibraries.csv":
                    OP.write('        "'+ f +'": "force:' + row[f] + '"')
                else:
                    OP.write('        "'+ f +'": "' + row[f] + '"')

                force = True
        if not first: OP.write(',\n')                           #new
        OP.write('        "address_concat": "force: ''"')       #new
        add = False
        for f in addressFields:
            if row[f] != '': add = True
        if add:
            if other or force: OP.write(',\n')
            OP.write('         "address": {\n')
            first = True
            for f in addressFields:
                if row[f] != '':
                    if first:  first = False
                    else: OP.write(',\n')
                    OP.write('            "'+ f + '": "' + row[f] + '"')
            OP.write('        }\n')
        OP.write('    }')
        if row["filter_name"] != "":
            OP.write(',\n    "filter": {\n')
            OP.write('         "'+ row["filter_name"] + '": "' + row["filter_value"] + '"  \n')
            OP.write('    }\n')

        OP.write('}')
        OP.close()

if __name__ == "__main__":
    main()

#Filter	Done	File	.library_name	library_type	unit	street_no	street_name	street_suffix	street_direction	address	postcode	city	prov/terr	PRuid	CSDname	CSDuid	longitude	latitude	 Data_Provider

