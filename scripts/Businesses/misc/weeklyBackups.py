'''
Backups up .py and .ipynb files, except for exclusions.

Will backup other files too if included.
'''

import os
import shutil as su

ODBiz_root = '/home/jovyan/ODBiz'
folders_to_backup = [
    '1-PreProcessing',
    '2-OpenTabulate',
    '3-Merging',
    '4-Parsing',
    '5-Geocoding',
    '6-AssignCSDs'
]

excluded_files = [
    'test.py',
    'mergingTest.ipynb'
]

include_files = [
    'readMe_PreProcessing.md',
    'opentab.conf',
    'Readme_opentab.md',
    'variablemap.csv',
    'Readme.md'
]

dst_root = '/home/jovyan/LODE-ECDO/scripts/Businesses'

print('Files copied over:')
for folder in folders_to_backup:
    if not(os.path.exists(f'{ODBiz_root}/{folder}')):
        continue
    print(folder)
    for f in os.listdir(f'{ODBiz_root}/{folder}'):
        f_len = len(f)
        include = False
        if f in excluded_files:
            include = False
        elif f_len >= 3 and f[-3:] == '.py':
            include = True
        elif f_len >= 6 and f[-6:] == '.ipynb':
            include = True
        elif f_len >= 3 and f[-3:] == '.md':
            include = True
        elif f in include_files:
            include = True
        else:
            include = False

        if include:
            src_file_path = f'{ODBiz_root}/{folder}/{f}'
            dst_file_path = f'{dst_root}/{folder}/{f}'
            su.copyfile(src_file_path, dst_file_path)
            print(f'    |___{f}')
        else:
            print(f'    |___XXX {f}')


        # print(f)
this_file_path = f'{ODBiz_root}/weeklyBackups.py'
su.copyfile(this_file_path, f'{dst_root}/misc/weeklyBackups.py')
print('weeklyBackups.py')
print('Finished')