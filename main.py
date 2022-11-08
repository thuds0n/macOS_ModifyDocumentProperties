import sys
import os
import subprocess
import pathlib
from datetime import datetime
import glob

def main():
    directory = r"/Users/timothy.hudson/Library/CloudStorage/GoogleDrive-thudson1611@gmail.com/My Drive/Documents/School/Scots/Merits & Demerits"

    if not os.path.exists(directory):
        print("DIRECTORY DOES NOT EXIST")
        sys.exit()

    subfolders = [x[0] for x in os.walk(directory)]

    for folder in subfolders:
        for filename in os.listdir(folder):

            print(filename)
            file_path = os.path.join(folder, filename)

            mod_timestamp = get_modification_time(file_path)
            #print('Modification Timestamp:', mod_timestamp)
            mod_date_time = datetime.fromtimestamp(mod_timestamp)
            #print('Modification Date:', mod_date_time.strftime("%Y/%m/%d  %H:%M:%S"))


            create_timestamp = get_creation_time(file_path)
            #print('Creation Timestamp:', create_timestamp)
            create_date_time = datetime.fromtimestamp(create_timestamp)
            #print('Creation Date:', create_date_time.strftime("%Y/%m/%d  %H:%M:%S"))

            file_path = convert_shell_compatible_string(file_path)

            if mod_date_time.date() < create_date_time.date():
                set_creation_time(file_path, mod_date_time)
            else:
                print('CREATION DATE NOT MODIFIED')

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    #new_timestamp = datetime.timestamp(date_time)
    #print(new_timestamp)

    #print(date.strftime('%m/%d/%Y %H:%M:%S'))

    print('---------------------FINISHED---------------------')
    return

def get_creation_time(path):
    return os.stat(path).st_birthtime
    # filename = pathlib.Path(path)
    # return filename.stat().st_ctime

def get_modification_time(path):
    return os.path.getmtime(path)
    # filename = pathlib.Path(path)
    # return filename.stat().st_mtime

def set_modification_time(path, mod_date_time):
    #mod_timestamp = mod_date_time.timestamp()
    #os.utime(path, (mod_timestamp, mod_timestamp))

    #touch -mt YYYYMMDDhhmm
    command = 'SetFile -m "{}" {}'.format(mod_date_time.strftime('%m/%d/%Y %H:%M:%S'), path)
    #subprocess.call(command, shell=True)
    try:
        subprocess.check_call(command, shell=True)
    except CalledProcessError as e:
        print(e)
        print("{}".format(path))
        print("ERROR MODIFYING DATE")
        sys.exit()
    return

def set_creation_time(path, create_date_time):
    #touch -t YYYYMMDDhhmm
    command = 'SetFile -d "{}" {}'.format(create_date_time.strftime('%m/%d/%Y %H:%M:%S'), path)
    #subprocess.call(command, shell=True)
    try:
        subprocess.check_call(command, shell=True)
    except CalledProcessError as e:
        print(e)
        print("{}".format(path))
        print("ERROR MODIFYING DATE")
        sys.exit()
    return

def convert_shell_compatible_string(file_path):
    file_path = file_path.replace(' ', '\ ')
    file_path = file_path.replace('(', '\(')
    file_path = file_path.replace(')', '\)')
    file_path = file_path.replace('&', '\&')
    file_path = file_path.replace("'", "\\'")
    return file_path

if __name__ == "__main__":
    main()
