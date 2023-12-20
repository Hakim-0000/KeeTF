import os

root_path = os.getcwd()
listFiles = os.listdir(root_path)

# passw_file = []

# 0PWQ.txt  8ABn.txt

# for file in listFiles:
with open(file, 'r') as read:
    f = read.readlines()
    for line in f:
        if "password" in line:
            print("This file has the string 'password'")
            break 

# print(passw_file)