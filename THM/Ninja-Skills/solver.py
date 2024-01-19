import os

file_name = ["8V2L", "bny0", "c4ZX", "D8B3", "FHl1", "oiMO", "PFbD", "rmfX", "SRSq", "uqyw", "v2Vb", "X1Uy"]

def searching(file):
    location = os.system(f'find / 2>/dev/null | grep -i {file}')
    return location


for i in file_name:
    get_loc = searching(i)
    
