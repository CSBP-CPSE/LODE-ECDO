# download the ODA data files

import requests, zipfile, io

provinces = ['AB', 'BC', 'MB', 'NB', 'NT', 'NS', 'ON', 'PE', 'QC', 'SK']

for province_code in provinces:
    zip_file_url = "https://www150.statcan.gc.ca/n1/pub/46-26-0001/2021001/ODA_" + province_code + "_v1.zip"
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data/oda-addresses")