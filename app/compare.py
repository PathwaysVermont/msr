import csv

pre_crt = open("crtprofile08.csv")
pre_ffs = open("ffsprofile08.csv")
dupes = open("duplicates.txt",'w')

crt = csv.reader(pre_crt, delimiter=";")
ffs = csv.reader(pre_ffs, delimiter=";")

crt_list = []
ffs_list = []

def name(a):
	return "%s, %s" % (a[78],a[76])

for x in crt:
	crt_list.append(x)

for x in ffs:
	ffs_list.append(x)
	
for x in crt_list:
	for y in ffs_list:
		if name(x) == name(y):
			dupes.write("%s\n" % name(x))