import sys
import os
from subprocess import call
import pathlib
from datetime import datetime

def main():
    file_path = r"/Users/timothy.hudson/Library/CloudStorage/GoogleDrive-thudson1611@gmail.com/My Drive/Documents/School/BBC/Year 5/Easter.doc"

    custom_date = '2006/04/27-12:00:00'

    custom_datetime = datetime.strptime(custom_date, '%Y/%m/%d-%H:%M:%S')


    if not os.path.exists(file_path):
        print("FILE DOES NOT EXIST")
        sys.exit()


    print(file_path.split('/')[-1])

    mod_timestamp = get_modification_time(file_path)
    #print('Modification Timestamp:', mod_timestamp)
    mod_date_time = datetime.fromtimestamp(mod_timestamp)
    print('Modification Date:', mod_date_time.strftime("%Y/%m/%d  %H:%M:%S"))


    create_timestamp = get_creation_time(file_path)
    #print('Creation Timestamp:', create_timestamp)
    create_date_time = datetime.fromtimestamp(create_timestamp)
    print('Creation Date:', create_date_time.strftime("%Y/%m/%d  %H:%M:%S"))

    print('Custom Date:', custom_datetime.strftime("%Y/%m/%d  %H:%M:%S"))

    file_path = convert_shell_compatible_string(file_path)

    date_key = input('MODIFY WHICH DATE? MODIFCATION [m] or CREATION [c]: ')
    source_key = input('WHICH SOURCE? MODIFICATION [m] CREATION [c] or CUSTOM [x]: ')

    if date_key == 'm' and source_key == 'x':
        set_modification_time(file_path, custom_datetime)
        print('MODIFICATION DATE CHANGED TO CUSTOM DATE')
    elif date_key == 'm' and source_key == 'c':
        set_modification_time(file_path, create_date_time)
        print('MODIFICATION DATE CHANGED TO CREATION DATE')
    elif date_key == 'c' and source_key == 'x':
        set_creation_time(file_path, custom_datetime)
        print('CREATION DATE CHANGED TO CUSTOM DATE')
    elif date_key == 'c' and source_key == 'm':
        if mod_date_time.date() < create_date_time.date():
            set_creation_time(file_path, mod_date_time)
            print('CREATION DATE CHANGED TO MODIFICATION DATE')
        else:
            print('CREATION DATE NOT MODIFIED')
    else:
        print('INVALID INPUT')
        sys.exit()

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
    call(command, shell=True)
    return

def set_creation_time(path, create_date_time):
    #touch -t YYYYMMDDhhmm
    command = 'SetFile -d "{}" {}'.format(create_date_time.strftime('%m/%d/%Y %H:%M:%S'), path)
    call(command, shell=True)
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
