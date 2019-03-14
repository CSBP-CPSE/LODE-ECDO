#!/usr/bin/env python

from xml.etree import ElementTree
import csv
import re
import sys

tree = ElementTree.parse(sys.argv[1])
root = tree.getroot()
ns = {"kml": "http://www.opengis.net/kml/2.2"}
header = "Placemark"

scheme = root.find(".//kml:Schema", ns)
col_iter = scheme.findall('kml:SimpleField', ns)
column_names = []
for element in col_iter:
    column_names.append(element.attrib['name'])

column_names.append("Longitude")
column_names.append("Latitude")

with open(sys.argv[2], 'w') as newdata:
    csvwriter = csv.DictWriter(newdata, fieldnames=column_names, quoting=csv.QUOTE_ALL)
    csvwriter.writeheader()

    for placemark in root.iter('{' + ns["kml"] + '}' + header):
        row = {}
        for data in placemark.findall('.//kml:SimpleData', ns):
            row[data.attrib['name']] = data.text
        
        cord = placemark.find('.//kml:coordinates', ns)
        geo = cord.text.split(',')
        row['Longitude'] = geo[0]
        row['Latitude'] = geo[1]
        csvwriter.writerow(row)
