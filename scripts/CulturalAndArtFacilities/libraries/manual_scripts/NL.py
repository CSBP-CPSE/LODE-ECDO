#script to extract addresses from kml files
#the remove_html_tags function is by  Jorge Luis Galvis Quintero
#at https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44
from pykml import parser
import csv
kml_file='/home/csis/codes/OpenTabulate/Libraries/NL_Libraries.kml'

NAMES=[]
ADDRESSES=[]
PLACES=[]
POSTALCODES=[]
LATS=[]
LONS=[]


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

with open(kml_file) as f:
    folder=parser.parse(f).getroot().Document.Folder
    
for pm in folder.Placemark:
    NAMES.append(str(pm.name).replace(", "," - "))
    #print(pm.Point.Location)
    html_text=str(pm.description).splitlines()
    i=0
    while i < (len(html_text)):
        line=html_text[i]
       
        if line=='<td>Location</td>':
            PLACES.append(remove_html_tags(html_text[i+2]))
        if line=='<td>Address</td>':
            ADDRESSES.append(remove_html_tags(html_text[i+2]))
        if line=='<td>Postal_Code</td>':
            POSTALCODES.append(remove_html_tags(html_text[i+2]))
        if line=='<td>Longitude</td>':
            LONS.append(remove_html_tags(html_text[i+2]))
        if line=='<td>Latitude</td>':
            LATS.append(remove_html_tags(html_text[i+2]))
        i+=1

            
rows=zip(NAMES,ADDRESSES,PLACES,POSTALCODES,LONS,LATS)
ROW1=['Name','Address','City','Postal Code', 'Longitude','Latitude']
with open('/home/csis/codes/OpenTabulate/pddir/raw/NL_Libraries.csv','w') as f:
    writer=csv.writer(f)
    writer.writerow(ROW1)
    for row in rows:
        writer.writerow(row)

