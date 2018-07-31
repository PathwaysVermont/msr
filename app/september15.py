import csv

pre_ffs = open('FFS_ID_list.csv')
pre_crt = open('CRT_ID_list.csv')

ffs = csv.reader(pre_ffs,delimiter=',')
crt = csv.reader(pre_crt,delimiter=',')

ffs_l = []
crt_l = []
ffs_list = []
crt_list = []
dupe_list = []

for x in ffs:
	ffs_l.append(x)
	
for x in crt:
	crt_l.append(x)

for x in ffs_l[0]:
	ffs_list.append(x)
	
for x in crt_l[0]:
	crt_list.append(x)
	
for x in crt_list:
	if x in ffs_list:
		dupe_list.append(x)
	else:
		print 'no'

print dupe_list