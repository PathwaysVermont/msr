import csv

pre_september = open("crtprofile09.csv")
pre_august = open("crtprofile08.csv")
# dest = open('profile_key.txt','w')
#no_match_list = open('no_match_list.txt','w')

september = csv.reader(pre_september,delimiter=';')
august = csv.reader(pre_august,delimiter=';')

august_list = []
september_list = []

for x in september:
	september_list.append(x)

for x in august:
	august_list.append(x)

# count = 0
# for x in september_list[0]:
	# dest.write('%d : %s\n' % (count, x))
	# count += 1

match = []
no_match = []

for x in august_list:
	for y in september_list:
		if x[1] == y[1]:
			match.append(x[1])

for x in august_list:
	if x[1] not in match:
		#no_match_list.write('%s\n' % x[96])
		no_match.append(x[96])
		
print no_match