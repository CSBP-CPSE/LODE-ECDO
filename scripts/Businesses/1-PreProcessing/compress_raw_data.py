'''
This script is incomplete and made obsolete by other scripts

I believe it just pretty prints the PreProcessing/raw directory
'''

import os

input_dir = '/home/jovyan/NewServer/ODBiz/1-PreProcessing/raw'

exclude_dirs = [
    '.ipynb_checkpoints',
    'archive',
    'testing'
]

exclude_files = [
    'Business_Licences.geojson'
]


print(f'{input_dir}/')
ori_white_space = '| ' 
for root, dirs, files in os.walk(input_dir):
    if root == input_dir:
        cur_dir = ''
    else:
        start_char = root.rfind('/') + 1
        cur_dir = root[start_char:]

    levels = cur_dir.count('/') + 1
    white_space = ori_white_space * levels

    # Print current directory
    if cur_dir != '':
        print(f'{white_space}|___{cur_dir}/')
        white_space += ori_white_space

    for f in files:
        filename = os.path.join(root, f)
        include = True
        for ef in exclude_files:
            if ef in filename:
                include = False 

        # Print file names in current directory
        if include:
            # stuff
            print(f'{white_space}|___{f}')
        else:
            print(f'{white_space}|___XXX {f}')

    dirs_copy = dirs.copy()
    for d in dirs_copy:
        include = True
        if d in exclude_dirs:
            include = False
        
        # Print excluded directories
        if not(include):
            dirs.remove(d)
            print(f'{white_space}|___XXX {d}/')
    
