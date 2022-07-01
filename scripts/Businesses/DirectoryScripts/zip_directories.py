import shutil as su 
from tqdm import tqdm
import os
import zipfile as zf

dir_to_zip = '/home/jovyan/ODBiz'
dirs_to_exclude = [
    '/home/jovyan/ODBiz/3-Merging/input',
    '/home/jovyan/ODBiz/3-Merging/output'
]
output_filename = '/home/jovyan/zipped_dirs.zip'

with zf.ZipFile(output_filename, mode = 'w') as archive:
    for root, dirs, files in os.walk(dir_to_zip):
        if '3-Merging/input' in root or '3-Merging/output' in root:
            continue
        else:
            for f in files:
                filePathName = f'{root}/{f}'
                arcname = filePathName[13:]
                archive.write(filePathName,arcname=arcname)
                print(f'{filePathName} added to archive')

print(f'Archive saved as {output_filename}')

