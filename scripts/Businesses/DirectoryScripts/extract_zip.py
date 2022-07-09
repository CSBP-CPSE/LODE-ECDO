import shutil as su

in_dir_name = '/home/jovyan/zipped_dirs.zip'
out_dir_name = '/home/jovyan/'

su.unpack_archive(in_dir_name, out_dir_name)
print(f'Files unzipped to {out_dir_name}')
