import os
import glob
import shutil
import argparse
import subprocess


# convert a .mid file to a .omd file using the omdconvert.exe program by OneTesla
def convert_midi_to_omd(file_path: str):
    # get absolute path from relative path
    absolute_path = os.path.abspath(file_path)

    # execute the omd converter with a subprocess call, supress the non error output
    subprocess.call(["omdconvert.exe", absolute_path], stdout=subprocess.DEVNULL)


# fix file paths to work (theoretically) on both windows and linux machines
def fix_file_path(path: str) -> str:
    return path.replace("\\\\", "\\").replace("/", "\\")


# get the name of the last directory in a path from a path
def get_path_token(path: str, index: int = 1):
    return fix_file_path(path).split("\\")[-1 * index]


# get the relative path from a given path & root
def get_origin_relative_path(path: str, root: str):
    # remove the root component from the path
    return path.replace(root, "")


# move a file from the origin path to the destination dir, keeping the same parent directory structure as the origin
def move_file(file_path: str, destination: str, origin: str):
    # get relative path from origin
    relative_path = file_path.replace(origin, "")

    # create destination path
    destination_path = destination + relative_path

    # move the file to the destination
    os.rename(file_path, destination_path)


# takes glob string, find .mid files, converts to .omd files, moves .omd files to destination
def glob_and_convert(glob_string: str, origin: str, destination: str, verbose: bool = False) -> int:
    # keep track of total converted midi files
    count = 0

    for file in glob.glob(glob_string):
        # correct file name
        file = fix_file_path(file)

        # debug message
        if verbose:
            print("Converting .mid file '" + file + "'...")

        # convert midi to omd file
        convert_midi_to_omd(file)

        # get omd file name from .mid or .midi filename
        omd_filename = file.replace(".mid", ".omd").replace(".midi", ".omd")

        # debug message
        if verbose:
            print("Moving generated .omd file '" + omd_filename + "'...")

        # move new omd file into destination
        move_file(omd_filename, destination, origin)

        # increment count
        count += 1

    return count


# generate new destination folders
def generate_new_folders(origin: str, destination: str, verbose: bool = False):
    # find and iterate over all origin folders and make copies of them
    for path in os.listdir(origin):
        # ignore files
        if os.path.isfile(origin + "\\" + path):
            continue

        # fix the directory path
        path = fix_file_path(path)

        # create directory with same name in destination as in origin
        new_folder = destination + "\\" + get_path_token(path)

        # debug message
        if verbose:
            print("Creating OMD Output Directory '" + new_folder + "'...")

        # create new dir
        os.mkdir(new_folder)


# delete the old destination OMD folders
def delete_old_omd(destination: str, verbose: bool = False):
    # fold all old OMD folders
    for path in glob.glob(destination + "/*"):
        # check if path is file
        if os.path.isfile(path):
            # debug message
            if verbose:
                print("Removing Old .omd File '" + path + "'...")

            # remove file
            os.remove(path)
        else:
            # debug message
            if verbose:
                print("Removing Old .omd Directory '" + path + "'...")

            # remove directory and its files
            shutil.rmtree(path)


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description='A tool for mass converting midi files into .omd files for use in '
                                                 'the OneTesla interrupter.')

    # arguments for parser
    parser.add_argument('-o', "-output", dest='destination', action='store', default="./omd",
                        help="Path to directory where .omd files and subdirectories will be populated into.")
    parser.add_argument('-s', "-source", dest='origin', action='store', default="./midi",
                        help="Path to directory where midi files and subdirectories will be converted and copied from.")
    parser.add_argument('-v', "--verbose", dest='verbose', action='store_const', default=False, const=True,
                        help="If provided will enable verbose logging.")

    # parse args
    args = parser.parse_args()

    # fixed destination file path
    dest = fix_file_path(args.destination)
    orig = fix_file_path(args.origin)
    verb = args.verbose

    # keep track of total converted midi files
    converted_count = 0

    # delete the old data in the destination directory
    delete_old_omd(dest, verb)

    # generate replacement subdirectories
    generate_new_folders(orig, dest, verb)

    # convert and count midi files in all subdirectories
    converted_count += glob_and_convert(orig + "\**\*.mid", orig, dest, verb)

    # convert and count midi files in top level of directory
    converted_count += glob_and_convert(orig + "\*.mid", orig, dest, verb)

    print("Converted " + str(converted_count) + " midi files to .omd files successfully.")
