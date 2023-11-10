import shutil as su

def main():
    in_dir_name = '/home/jovyan/ODBizOpenTabCompressedOutput/OpenTabCompressedOutput.zip'
    out_dir_name = '/home/jovyan/ODBiz/3-Merging/input'

    su.unpack_archive(in_dir_name, out_dir_name)
    print(f'Files unzipped to {out_dir_name}')

if __name__ == '__main__':
    main()
