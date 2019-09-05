#!/usr/bin/python
import sys, os, re
import filecmp
import logging

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
    for f in backup_files:
        try:
            if has_orig(f, orig_files):
                if matches_orig(path, f):
                    print(f + ": files match")
                else:
                    print(f + ": no match")
            else:
                logging.info("No orig file found for: " + f)
        except ValueError:
            logging.warning('Could not identify orig file for: ' + f)
        
def has_orig(bac_file, orig_files):
    orig = [f for f in orig_files if orig_name(bac_file) in f]

    if len(orig) > 1:
        raise ValueError('Found multiple candidates') # This should not be possible to happen
    return len(orig) > 0

def orig_name(bac_file):
        return bac_file[1:-6]
    
def matches_orig(dir, bac_file):
    bac_cand = os.path.join(dir, bac_file)
    orig_cand = os.path.join(dir, orig_name(bac_file))
    
    try:
        return filecmp.cmp(bac_cand, orig_cand)
    except FileNotFoundError:
        logging.error("Could not find: " + bac_cand + " or " + orig_cand)

if __name__ == "__main__":
    main()