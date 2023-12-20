#!/usr/bin/python3

import os
import zipfile
import exiftool

root_path = os.getcwd()

def unz(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(root_path)

# unzip root zip
# unz(root_path+'/final-final-compressed.zip')

# unzip remaining zip
listFiles = os.listdir(root_path)
for file in listFiles:
    if file.endswith('zip'):
        unz(file)
        # os.remove(file)

# count the extracted files except zip
listFiles = os.listdir(root_path)
file_count = 0
for file in listFiles:
    if file.endswith('txt'):
        file_count+=1

# count the total version
listFiles = os.listdir(root_path)
ver_count = 0
for file in listFiles:
    with exiftool.ExifTool() as et:
        metadata = et.execute_json('-a', '-u', '-g', '-l', file)
    for d in metadata:
        try:
            if(d[u'XMP:Version']):
                ver_count+=1
        except:
            continue

listFiles = os.listdir(root_path)
passw_file = []
for file in listFiles:
    if file.endswith('txt'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as read:
            f = read.readlines()
            for line in f:
                if "password" in line:
                    # print("This file has the string 'password'")
                    passw_file.append(file)
                    break

print(f'Total files: {file_count}\nTotal ver: {ver_count}\nFile contain password : {passw_file}')
