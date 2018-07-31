import csv
from town_code import *
from sys import argv

# -----------------------------------------------------------------------------
# INITIAL INPUT & FILES
#
# Preparing and initializing external files we're working with and getting the
# initial information about the data set we'll be running.
#
# We need to update these with each run through of files, or better yet, we need
# to create a GUI which will allow users to browse and find files tow work with
# -----------------------------------------------------------------------------

script, begindate, enddate, file1, file2, primary_prog = argv

#begindate = '010101' #raw_input("Begin Date of report (YYMMDD) >> ")
#enddate = '010101' #raw_input("End Date of report (YYMMDD) >> ")
#primary_prog = raw_input("If CRT, enter 1. If FFS, enter 2. >> ")

prime_program = ''
if primary_prog == '1':
	prime_program = 'CRT'
else:
	prime_program = 'FFS'

pre_profiles = open(file1)
pre_services = open(file2)
pre_dest = "MSR_%s_%s.txt" % (prime_program,begindate[:4])
pre_error_log = "Error_Log_%s_%s.txt" % (prime_program,begindate[:4])

profiles = csv.reader(pre_profiles, delimiter = ';')
services = csv.reader(pre_services, delimiter = ';')
dest = open(pre_dest, 'w')
error_log = open(pre_error_log, 'w')

# -----------------------------------------------------------------------------	
# DATA EXTRACTION
#
# Useful loops to get data into most workable form for our purposes
# -----------------------------------------------------------------------------

services_list_uncropped = []
for x in services:
	services_list_uncropped.append(x)

services_list = []
# Amend services list to include only those services where we recorded a
# duration of greater than zero minutes
for x in range(len(services_list_uncropped)):
	if len(services_list_uncropped[x][5]) > 0 and services_list_uncropped != '0':
		services_list.append(services_list_uncropped[x])

services_names = []
for x in services_list:
	services_names.append(x[13])

profiles_list_uncropped = []
for x in profiles:
	profiles_list_uncropped.append(x)

profiles_list = []
# Amend profiles list to include only people whose names turn up in both 
# profiles and services reports
for x in profiles_list_uncropped:
	name = "%s, %s" % (x[78], x[76])
	if name in services_names:
		profiles_list.append(x)

# -----------------------------------------------------------------------------
# ERROR LOGGER
#
# Report out errors to a readable text document.
# -----------------------------------------------------------------------------

profile_codes = profiles_list_uncropped[0]
services_codes = services_list_uncropped[0]
line_break = '-----------------------------------------------------------------------------\n'

# Nicely format the Error Logger header
error_log.write('%s\nERROR LOG\n\n%s' % (line_break,line_break))

# Record more critical errors at top of log
error_log.write('Critical Errors:\n\n')

# Record duplicated name errors
# And amend errors
error_log.write('Duplicated names:\n')
dupes = {}
check = []
for x in range(len(profiles_list)):
	n = "%s %s" % (profiles_list[x][76],profiles_list[x][78])
	if n in check:
		error_log.write("%s\n" % n)
		dupes[x] = 0
		for y in range(x):
			n_two = "%s %s" % (profiles_list[y][76],profiles_list[y][78])
			if n_two == n and y not in dupes:
				dupes[y] = 0
		check.append(n)
	else:
		check.append(n)

for x in dupes:
	count = 0
	for y in profiles_list[x]:
		if y == (len(y)*'9') or y == (len(y)*' ') or y == '':
			count += 1
	dupes[x] = count
	
del_list = []
for x in dupes:
	for y in dupes:
		if profiles_list[x][78] == profiles_list[y][78] and x != y and x not in del_list and y not in del_list:
			if dupes[x] < dupes[y]:
				del_list.append(y)
			else:
				del_list.append(x)

profile_index_list = range(len(profiles_list))
for x in del_list:
	profile_index_list.remove(x)
	
profiles_list_temp = []
for x in profile_index_list:
	profiles_list_temp.append(profiles_list[x])

profiles_list = profiles_list_temp
error_log.write('\n')

# Homeless status check
error_log.write('Address/Homlessness conflicts:\n')
count = -1
for x in profiles_list:
	count += 1
	if len(x[84]) < 1 and (x[60] != '11' or x[67] != '11'):
		error_log.write('%s %s, Arrangement at Intake: %s, Current Arrangement: %s\n' % (x[76],x[78],x[60],x[67]))
error_log.write('\n')
		
def error_init(x):
	# Initiate a new section for each individual
	error_log.write('-----------------------------------------------------------------------------\n')
	error_log.write(x.upper())
	error_log.write('\n')

def error_logger(a,b):
	# Log the errors according to which data section and data column they originate
	global error_count
	if a == x:
		error_log.write('\tProfile  | %s: ' % profile_codes[b])
		if len(x[b]) > 1:
			error_log.write('%s\n' % x[b])
		else:
			error_log.write('<blank>\n')
		#global error_count
		error_count += 1
	else:
		error_log.write('\tServices | %s: ' % services_codes[b])
		if len(y[b]) > 1:
			error_log.write('%s\n' % y[b])
		else:
			error_log.write('<blank>\n')
		#global error_count
		error_count += 1
	

# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
#
# Defining useful functions that will be worked with in our "main" script
# -----------------------------------------------------------------------------

def round_to_quart(x):
# Rounds input variable up to nearest 1/4 decimal
	y = int(x)
	suff = x - y
	if suff == 0:
		suff = 0.0
	elif suff <= .25:
		suff = .25
	elif suff <= .5:
		suff = .50
	elif suff <= .75:
		suff = .75
	else:
		suff = 1.00
	return y + suff

def blank(x):
	y = " " * x
	dest.write(y)

def int_test(k,l,m,n):
	#k is the group of data being tested: profiles (x) or services (y)
	#l is the index number in our code sheet
	#m is the number of digits testing for
	#n is the default value to input in case of error, usually '9'
	if len(k[l]) == m:
		try:
			int_test = int(k[l])
			dest.write(k[l])
			spacer = ' ' * (m - len(str(k[l])))
			dest.write(spacer)
		except ValueError:
			dest.write(str(n))
	else:
		dest.write(str(n))
		error_logger(k,l)
	
def string_limiter(k,l,m):
	#k is the group of data being tested: profiles (x) or services (y)
	#l is the index number
	#m is the max length of string
	if len(k[l]) > m:
		dest.write(k[l][:m])
	else:
		dest.write(k[l])
		spacer = ' '
		gap = m - len(k[l])
		spacer = spacer * gap
		dest.write(spacer)
		
def ssn_format(x):
# Formats SSNs received from Face Page, removes hyphens
	split_ssn = x.split('-')
	y = ''
	for i in split_ssn:
		y = y+i
	return y

def dob_format(x):
# Formats DOBs received from Face Page, removes slashes
	 x = x.split('/')
	 y = (x[2][2:])+x[0]+x[1]
	 return y

def gender_parser(x):
	if x[0].lower() == 'm':
		w_to_dest(1)
	elif x[0].lower() == 'f':
		w_to_dest(2)
	else:
		w_to_dest(9)
		return '9'

def w_to_dest(x):
	dest.write(str(x))

def new_line():
	dest.write('\n')
			
# -----------------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------------

for x in profiles_list:
	#Name for later use in Error Log and Syncing with services
	name = "%s, %s" % (x[78],x[76])
	
	error_init(name)
	error_count = 0
	
	#MSR Record Identifier
	w_to_dest(1)
	
	#Client ID
	int_test(x,1,9,123456789)
	
	#MSR Provider ID
	w_to_dest(50)
	
	#Primary Program Assignment Code
	if primary_prog == "1":
		w_to_dest('04')
	elif primary_prog == "2":
		w_to_dest(12)
	else:
		print "Re-run this script with correct reponse to CRT/FFS prompt!"
	
	#Date of Birth
	if len(dob_format(x[97])) == 6:
		w_to_dest(dob_format(x[97]))
	else:
		w_to_dest('ERR004')
		error_logger(x,97)

	#MSR Gender Code
	gender = gender_parser(x[99])
	if gender == '9':
		error_logger(x,99)
	
	#Gross annual family income at intake
	w_to_dest(99991)
	
	#Client Payment Responsibility
	w_to_dest('01')
	
	#Individuals on Income Code
	int_test(x,8,1,9)
	
	#Primary Payer Code
	w_to_dest('01') #Medicaid
	
	#Secondary Payer Code
	w_to_dest('00') #none
	
	#Third Payer Code
	w_to_dest('00') #none

	#DSM-IV Axis I Primary Dx
	prime_dx = x[102].split(',')
	prime_dx = prime_dx[0]
	if '.' in prime_dx:
		prime_dx = prime_dx.split('.')
		prime_dx = prime_dx[0] + prime_dx[1]
		w_to_dest(prime_dx)
		spacer = ' ' * (5 - len(prime_dx))
		w_to_dest(spacer)
	elif len(prime_dx) > 2:
		w_to_dest(prime_dx)
		spacer = ' ' * (5 - len(prime_dx))
		w_to_dest(spacer)
	else:
		w_to_dest('ERR12')
		error_logger(x,102)
	
	#Marital/Family Problem Code
	int_test(x,13,1,9)
	
	#Social/Interpersonal Problem Code
	int_test(x,14,1,9)
	
	#Coping Problem Code
	int_test(x,15,1,9)
	
	#Medical Somatic Problem Code
	int_test(x,16,1,9)
	
	#Depression or Mood Disorder Code
	int_test(x,17,1,9)

	#Attempt, threat or danger of suicide Code
	int_test(x,18,1,9)
	
	#Alcohol Code
	int_test(x,19,1,9)
	
	#Drugs Code
	int_test(x,20,1,9)
	
	#Eating Disorder Code
	int_test(x,21,1,9)
	
	#Thought Disorder Code
	int_test(x,22,1,9)
	
	#Involvement with Criminal Justice code
	int_test(x,23,1,9)
	
	#Abuse/assault/rape Victim Code
	int_test(x,24,1,9)
	
	#Runaway behavior code
	int_test(x,25,1,9)
	
	#Condition on termination code
	int_test(x,26,1,0)
	
	#MSR Begin date of report
	w_to_dest(begindate)
	
	#MSR End date of report
	w_to_dest(enddate)
	
	#C&E Recipient type
	w_to_dest('00')
	
	#Date of 'Income at Intake'
	int_test(x,30,4,'1410') #NEED TO FIX DEFAULT DATE
	
	#Date case opened
	int_test(x,31,6,'141001') #NEED TO FIX DEFAULT DATE

	new_line()
	
	#Date case closed
	int_test(x,33,6,'000000')
	
	#DSM-IV Axis I Secondary Dx
	prime_dx = x[102].split(',')
	if len(prime_dx) > 1:
		prime_dx = prime_dx[1].lstrip()
		if '.' in prime_dx:
			prime_dx = prime_dx.split('.')
			prime_dx = prime_dx[0] + prime_dx[1]
			w_to_dest(prime_dx)
			spacer = ' ' * (5 - len(prime_dx))
			w_to_dest(spacer)
		elif len(prime_dx) > 2:
			w_to_dest(prime_dx)
			spacer = ' ' * (5 - len(prime_dx))
			w_to_dest(spacer)
		else:
			w_to_dest('     ')
	else:
		w_to_dest('     ')
		
	#DSM-IV Axis II Primary Dx
	w_to_dest('     ')
	
	#DSM-IV Axis II Secondary Dx
	w_to_dest('     ')
	
	#Blank (3 spaces)
	blank(3)
	
	#Current level of functioning (GAF)
	int_test(x,38,2,'00')
	
	#Blank (3 spaces)
	blank(3)
	
	#Level of functioning at admission (GAF)
	int_test(x,40,2,'00')
	
	#Blank space
	blank(1)
	
	#Name fragment
	if len(x[78]) < 5:
		frag = x[78][0] + x[78][2] + ' '
		frag = frag.upper()
		dest.write(frag)
	else:
		frag = x[78][0] + x[78][2] + x[78][4]
		frag = frag.upper()
		dest.write(frag)
	
	#Blank (5 spaces)
	blank(5)
	
	#Previous treatment by mental health organization of any kind
	int_test(x,45,1,9)
	
	#Previous treatment within the past year
	int_test(x,44,1,9)
	
	#Previous treatment by this organization
	int_test(x,46,1,9)
	
	#Inpatient code
	int_test(x,47,1,9)
	
	#Residential code
	int_test(x,48,1,9)
	
	#Partial day code
	int_test(x,49,1,9)
	
	#Outpatient code
	int_test(x,50,1,9)
	
	#Case management code
	int_test(x,51,1,9)
	
	#Emergency code
	int_test(x,52,1,9)
	
	#Race code
	if 'White' in x[101]:
		w_to_dest('1')
	elif 'Black' in x[101]:
		w_to_dest('2')
	elif 'Indian' in x[101]:
		w_to_dest('3')
	elif 'Asian' in x[101]:
		w_to_dest('4')
	elif 'Other' in x[101]:
		w_to_dest('5')
	elif 'Declined' in x[101]:
		w_to_dest('8')
	else:
		w_to_dest('9')
	
	#Hispanic origin code
	if 'Mexican' in x[98]:
		w_to_dest('1')
	elif 'Puerto' in x[98]:
		w_to_dest('2')
	elif 'Cuban' in x[98]:
		w_to_dest('3')
	elif 'Other' in x[98]:
		w_to_dest('4')
	elif 'American' in x[98]:
		w_to_dest('5')
	elif 'Not Latin' in x[98]:
		w_to_dest('6')
	elif 'Declined' in x[98]:
		w_to_dest('8')
	else:
		w_to_dest('9')
	
	#Marital status code
	if 'Married' in x[100]:
		w_to_dest('2')
	elif 'Separated' in x[100]:
		w_to_dest('3')
	elif 'Divorced' in x[100]:
		w_to_dest('4')
	elif 'Widowed' in x[100]:
		w_to_dest('5')
	else:
		w_to_dest('9')
		
	#Zip code of residence at admission to this organization
	int_test(x,56,5,'05999')
	
	#Veteran status code
	int_test(x,57,1,9)
	
	#Legal status code
	int_test(x,58,1,9)
	
	#Source of referral code
	int_test(x,59,2,'06')

	#Residential arrangement at intake code
	if len(x[84]) < 1:
		w_to_dest(11)
	else:
		int_test(x,60,2,99)
	
	#Living arrangement at intake code
	int_test(x,61,1,9)
	
	#SSI eligibility at intake code
	int_test(x,62,1,9)
	
	#Discontinuation status code
	int_test(x,63,1,9)
	
	#Referral upon discharge
	int_test(x,64,2,'00')
	
	#Current primary case worker
	blank(5)
	
	#Zip code of current residence
	int_test(x,87,5,'05999')
	
	#Current residential arrangement code
	if len(x[84]) < 1:
		w_to_dest(11)
	else:
		int_test(x,67,2,'99')
	
	new_line()
	
	#Current living arrangement
	int_test(x,69,1,9)
	
	#Current SSI eligibility
	int_test(x,70,1,9)
	
	#Current gross family income
	dest.write('99991')
	
	#Date of most recent demographic data interview
	int_test(x,72,6,'150101')
	
	blank(59)
	
	new_line()
	
	blank(28)
	
	#First name
	if len(x[76]) > 11:
		dest.write(x[76][:11])
	else:
		dest.write(x[76])
		spacer = ' '
		gap = 11 - len(x[76])
		spacer = spacer * gap
		dest.write(spacer)
		
	#Middle Initial
	if len(x[77]) > 0:
		w_to_dest(x[77][0])
	else:
		w_to_dest(' ')
		
	#Last name
	if len(x[78]) > 15:
		dest.write(x[78][:15])
	else:
		dest.write(x[78])
		spacer = ' '
		gap = 15 - len(x[78])
		spacer = spacer * gap
		dest.write(spacer)
		
	#Modifier / Suffix
	if len(x[79]) > 3:
		dest.write(x[79][:3])
	else:
		dest.write(x[79])
		spacer = ' '
		gap = 3 - len(x[79])
		spacer = spacer * gap
		dest.write(spacer)
	
	#Social security number
	ssn = ssn_format(x[96])
	dest.write(ssn)
	
	#Date of death
	int_test(x,81,8,'00000000')
	
	#Social security number suffix
	dest.write(ssn[5:])
	
	new_line()
	
	#Street Address
	string_limiter(x,84,48)
	
	#City
	string_limiter(x,85,15)
	
	#State
	dest.write("VT")
	
	#Zip code
	int_test(x,87,5,'05999')
	
	#Blank (for extra 4 digits that could be in zip code)
	blank(4)
	
	#Town code
	city = x[85].upper()
	if len(str(town_code[city])) < 3:
		spacer = (3 - len(str(town_code[city]))) * '0'
		dest.write(spacer)
		w_to_dest(town_code[city])
	else:
		w_to_dest(town_code[city])
		
	new_line()
	
	blank(27)
	
	#Medicaid billing number
	string_limiter(x,95,9)
	
	#Account number
	blank(12)
	
	#Primary program assignment effective date
	int_test(x,92,8,'20141001')
	
	#Primary program end date
	dest.write('00000000')
	
	#Birth year prefix
	dest.write('19')
	
	new_line()
	
	# -------------------------------------------------------------------------
	# INNER SERVICES LOOP
	# -------------------------------------------------------------------------
	
	for y in services_list:
		if name == y[13]:
			
			#Record Identifier
			dest.write('2')
			
			#Action code
			blank(1)
			
			#Blank (7 spaces)
			blank(7)
			
			#Date of Service
			int_test(y,4,6,'ERR999')
			
			#Blank (4 spaces)
			blank(4)
			
			#Duration of services
			duration = int(y[5])
			duration = duration/60.0
			duration = round_to_quart(duration)
			dest.write(str(duration))
			spacer = ' '
			if len(str(duration).split('.')[1]) < 2:
				dest.write('0')
				gap = 5 - len(str(duration))
				spacer = spacer * gap
				dest.write(spacer)
			else:
				gap = 6 - len(str(duration))
				spacer = spacer * gap
				dest.write(spacer)
			
			#Program of service
			if primary_prog == "1":
				w_to_dest('04')
			elif primary_prog == "2":
				w_to_dest(12)
			else:
				print "Re-run this script with correct reponse to CRT/FFS prompt!"
			
			#Cost center
			dest.write('48')
			
			#Type of service code
			string_limiter(y,8,3)
			
			#Location code
			int_test(y,9,1,9)
			
			#Count
			dest.write('1')
			
			#ADAP Billable (blank)
			blank(1)
			
			#Staff Member ID#
			int_test(y,12,5,'00999')
			
			#Blank (9 spaces)
			blank(9)
			
			#HIV Information Given
			blank(1)
			
			#Account Number
			blank(12)
			
			#Reference Number
			blank(10)
			
			new_line()
	error_log.write('Error count: %s\n' % error_count)
	
dest.close()