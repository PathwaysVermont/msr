import os, sys

file_name = "custom.txt"
file_path = os.path.join(sys.path[0], 'writer', file_name)

print(file_path)
