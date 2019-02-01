import os, sys
base_path = sys.path[0][:-8]
base_path = os.path.join(base_path,'writer')
sys.path.insert(0, base_path)
import icd_code_list

print(sys.path)
print(icd_code_list.icd_10_list)
