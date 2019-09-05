#!/usr/bin/python
import sys, os, re
import filecmp
import logging

"""
Walks the specified directory and tries to clean the backup files generated by
Sciebo.
Input argument: path of the top level directory
"""
def main():
    if len(sys.argv) == 1:
        sciebo_dir = "D:\\sciebo\\"
    else:
        sciebo_dir = sys.argv[2]
    
    for dirpath, dirs, filenames in os.walk(sciebo_dir):
        clean_directory(dirpath, dirs, filenames)

"""
Checks if the files in the directory which match the pattern of a sciebo backup
file have a correspoinding file with a standard filename
If this _clean_ file exists it will be deleted.

Arguments:
path: path of the directory to be cleaned
dirs: TODO remove
files: files in the directory
"""
def clean_directory(path, dirs, files):
    backup_files = []
    orig_files = []

    for f in files:
        if re.match(r'.*.~[0-9a-fA-F]{0,4}', f):
            backup_files.append(f);
        else:
            orig_files.append(f);

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

"""
Checks if a sciebo backup file has a counterpart with a normal file name
Raises exceptioin if this counterpart cannot be identified as a single file

Arguments:
bac_file: name of the file matching the backup pattern
orig_files: list of files in which to find the original file
"""
def has_orig(bac_file, orig_files):
    orig = [f for f in orig_files if orig_name(bac_file) in f]

    if len(orig) > 1:
        raise ValueError('Found multiple candidates') # This should not happen
    return len(orig) > 0

"""
Returns the name of the standard file which should exist for a file with the
backup file pattern.

bac_file: 
"""
def orig_name(bac_file):
        return re.split(r'.~[0-9a-fA-F]{0,4}', bac_file[1:])[0]

"""
Check if the backup file has the same content as the file in the standard format
"""
def matches_orig(dir, bac_file):
    bac_cand = os.path.join(dir, bac_file)
    orig_cand = os.path.join(dir, orig_name(bac_file))
    
    try:
        return filecmp.cmp(bac_cand, orig_cand)
    except FileNotFoundError:
        logging.error("Could not find: " + bac_cand + " or " + orig_cand)

# To execute file with main method
if __name__ == "__main__":
    main()