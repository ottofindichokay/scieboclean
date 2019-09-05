#!/usr/bin/python
import sys, os, re

def main():
    if len(sys.argv) == 1:
        sciebo_dir = "D:\\sciebo\\"
    else:
        sciebo_dir = sys.argv[2]
    
    for dirpath, dirs, filenames in os.walk(sciebo_dir):
        clean_directory(dirpath, dirs, filenames)

def clean_directory(path, dirs, files):
    backup_files = []
    orig_files = []

    for f in files:
        if re.match(r'.*.~[0-9a-fA-F]{0,4}', f):
            backup_files.append(f);
        else:
            orig_files.append(f);

    #if len(backup_files) > 1: print(backup_files)
    for f in backup_files: has_orig(f, orig_files)

def has_orig(bac_file, orig_files):
    cand_name = bac_file[1:-6]
    orig = [f for f in orig_files if cand_name in f]

    if len(orig) == 1:
        print('Found candidate for ' + cand_name)
    else:
        raise Exception('Found multiple candidates') #This should not be possible to happen


if __name__ == "__main__":
    main()