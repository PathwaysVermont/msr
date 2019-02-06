from town_code import *
from icd_code_list import *

# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
#
# Defining useful functions that will be worked with in our "main" function
# -----------------------------------------------------------------------------
month_last_day = {
	'01':'31',
	'02':'28',
	'03':'31',
	'04':'30',
	'05':'31',
	'06':'30',
	'07':'31',
	'08':'31',
	'09':'30',
	'10':'31',
	'11':'30',
	'12':'31',
}

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

def blank(x, dest):
	y = " " * x
	dest.write(y)

def int_test(k,l,m,n, dest):
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

def string_limiter(k,l,m, dest):
	#k is the group of data being tested: profiles (x) or services (y)
	#l is the index number
	#m is the max length of string
	if len(k[l]) > 0:
		if len(k[l]) > m:
			dest.write(k[l][:m])
		else:
			dest.write(k[l])
			spacer = ' '
			gap = m - len(k[l])
			spacer = spacer * gap
			dest.write(spacer)
	else:
		spacer = ' ' * m
		dest.write(spacer)
		error_logger(k,l)

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

def gender_parser(x, dest):
	try:
		if x[0].lower() == 'm':
			w_to_dest(1, dest)
		elif x[0].lower() == 'f':
			w_to_dest(2, dest)
		else:
			w_to_dest(9, dest)
			return '9'
	except:
		w_to_dest(9, dest)
		return '9'

def w_to_dest(x, dest):
	dest.write(str(x))

def new_line(dest):
	dest.write('\n')

# -----------------------------------------------------------------------------
# FUDGING :O
# -----------------------------------------------------------------------------
def error_init(x):
	pass

def error_logger(x,y):
	pass
# -----------------------------------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------------------------------

def msr_file(profile_list, services_list, primary_prog, begindate, enddate, output_file):
    for x in profile_list:
        name = "%s, %s" % (x[78],x[76])
    	#print(name)

    	error_init(name)
    	error_count = 0

    	#MSR Record Identifier
    	w_to_dest(1, output_file)

    	#Client ID
    	int_test(x,1,9,123456789, output_file)

    	#MSR Provider ID
    	w_to_dest(50, output_file)

    	#Primary Program Assignment Code
    	if primary_prog == "1":
    		w_to_dest('04', output_file)
    	elif primary_prog == "2":
    		w_to_dest('12', output_file)
    	else:
    		print "Re-run this script with correct reponse to CRT/FFS prompt!"

    	#Date of Birth
    	try:
    		if len(dob_format(x[97])) == 6:
    			w_to_dest(dob_format(x[97]), output_file)
    		else:
    			w_to_dest('ERR004', output_file)
    			error_logger(x,97)
    	except IndexError:
    			print("Error caught!")
    			w_to_dest('ERR004', output_file)

    	#MSR Gender Code
    	gender = gender_parser(x[99], output_file)
    	if gender == '9':
    		error_logger(x,99)

    	#Gross annual family income at intake
    	w_to_dest(99991, output_file)

    	#Client Payment Responsibility
    	w_to_dest('01', output_file)

    	#Individuals on Income Code
    	int_test(x,8,1,9, output_file)

    	#Primary Payer Code
    	w_to_dest('01', output_file) #Medicaid

    	#Secondary Payer Code
    	w_to_dest('00', output_file) #none

    	#Third Payer Code
    	w_to_dest('00', output_file) #none

    	#DSM-IV Axis I Primary Dx
    	#prime_dx = x[102].split(',')
    	#prime_dx = prime_dx[0]
    	#if '.' in prime_dx:
    	#	prime_dx = prime_dx.split('.')
    	#	prime_dx = prime_dx[0] + prime_dx[1]
    	#	w_to_dest(prime_dx)
    	#	spacer = ' ' * (5 - len(prime_dx))
    	#	w_to_dest(spacer)
    	#elif len(prime_dx) > 2:
    	#	w_to_dest(prime_dx)
    	#	spacer = ' ' * (5 - len(prime_dx))
    	#	w_to_dest(spacer)
    	#else:
    	#	w_to_dest('ERR12')
    	#	error_logger(x,102)
    	w_to_dest('     ', output_file)

    	#Marital/Family Problem Code
    	int_test(x,13,1,9, output_file)

    	#Social/Interpersonal Problem Code
    	int_test(x,14,1,9, output_file)

    	#Coping Problem Code
    	int_test(x,15,1,9, output_file)

    	#Medical Somatic Problem Code
    	int_test(x,16,1,9, output_file)

    	#Depression or Mood Disorder Code
    	int_test(x,17,1,9, output_file)

    	#Attempt, threat or danger of suicide Code
    	int_test(x,18,1,9, output_file)

    	#Alcohol Code
    	int_test(x,19,1,9, output_file)

    	#Drugs Code
    	int_test(x,20,1,9, output_file)

    	#Eating Disorder Code
    	int_test(x,21,1,9, output_file)

    	#Thought Disorder Code
    	int_test(x,22,1,9, output_file)

    	#Involvement with Criminal Justice code
    	int_test(x,23,1,9, output_file)

    	#Abuse/assault/rape Victim Code
    	int_test(x,24,1,9, output_file)

    	#Runaway behavior code
    	int_test(x,25,1,9, output_file)

    	#Condition on termination code
    	int_test(x,26,1,0, output_file)

    	#MSR Begin date of report
    	w_to_dest(begindate, output_file)

    	#MSR End date of report
    	w_to_dest(enddate, output_file)

    	#C&E Recipient type
    	w_to_dest('00', output_file)

    	#Date of 'Income at Intake'
    	int_test(x,30,4,'1410', output_file) #NEED TO FIX DEFAULT DATE

    	#Date case opened
    	int_test(x,31,6,'141001', output_file) #NEED TO FIX DEFAULT DATE

    	#ICD-9
    	w_to_dest('N', output_file)

    	#ICD-10
    	w_to_dest('Y', output_file)

    	new_line(output_file)

    	#Date case closed
    	int_test(x,33,6,'000000', output_file)

    	#DSM-IV Axis I Secondary Dx
    	# prime_dx = x[102].split(',')
    	# if len(prime_dx) > 1:
    		# prime_dx = prime_dx[1].lstrip()
    		# if '.' in prime_dx:
    			# prime_dx = prime_dx.split('.')
    			# prime_dx = prime_dx[0] + prime_dx[1]
    			# w_to_dest(prime_dx)
    			# spacer = ' ' * (5 - len(prime_dx))
    			# w_to_dest(spacer)
    		# elif len(prime_dx) > 2:
    			# w_to_dest(prime_dx)
    			# spacer = ' ' * (5 - len(prime_dx))
    			# w_to_dest(spacer)
    		# else:
    			# w_to_dest('     ')
    	# else:
    		# w_to_dest('     ')
    	w_to_dest('     ', output_file)

    	#DSM-IV Axis II Primary Dx
    	w_to_dest('     ', output_file)

    	#DSM-IV Axis II Secondary Dx
    	w_to_dest('     ', output_file)

    	#Blank (3 spaces)
    	blank(3, output_file)

    	#Current level of functioning (GAF)
    	int_test(x,38,2,'00', output_file)

    	#Blank (3 spaces)
    	blank(3, output_file)

    	#Level of functioning at admission (GAF)
    	int_test(x,40,2,'00', output_file)

    	#Blank space
    	blank(1, output_file)

    	#Name fragment
    	if len(x[78]) < 5:
    		frag = x[78][0] + x[78][2] + ' '
    		frag = frag.upper()
    		output_file.write(frag)
    	else:
    		frag = x[78][0] + x[78][2] + x[78][4]
    		frag = frag.upper()
    		output_file.write(frag)

    	#Blank (5 spaces)
    	blank(5, output_file)

    	#Previous treatment by mental health organization of any kind
    	int_test(x,45,1,9, output_file)

    	#Previous treatment within the past year
    	int_test(x,44,1,9, output_file)

    	#Previous treatment by this organization
    	int_test(x,46,1,9, output_file)

    	#Inpatient code
    	int_test(x,47,1,9, output_file)

    	#Residential code
    	int_test(x,48,1,9, output_file)

    	#Partial day code
    	int_test(x,49,1,9, output_file)

    	#Outpatient code
    	int_test(x,50,1,9, output_file)

    	#Case management code
    	int_test(x,51,1,9, output_file)

    	#Emergency code
    	int_test(x,52,1,9, output_file)

    	#Race code
    	if 'White' in x[101]:
    		w_to_dest('1', output_file)
    	elif 'Black' in x[101]:
    		w_to_dest('2', output_file)
    	elif 'Indian' in x[101]:
    		w_to_dest('3', output_file)
    	elif 'Asian' in x[101]:
    		w_to_dest('4', output_file)
    	elif 'Other' in x[101]:
    		w_to_dest('5', output_file)
    	elif 'Declined' in x[101]:
    		w_to_dest('8', output_file)
    	else:
    		w_to_dest('9', output_file)

    	#Hispanic origin code
    	if 'Mexican' in x[98]:
    		w_to_dest('1', output_file)
    	elif 'Puerto' in x[98]:
    		w_to_dest('2', output_file)
    	elif 'Cuban' in x[98]:
    		w_to_dest('3', output_file)
    	elif 'Other' in x[98]:
    		w_to_dest('4', output_file)
    	elif 'American' in x[98]:
    		w_to_dest('5', output_file)
    	elif 'Not Latin' in x[98]:
    		w_to_dest('6', output_file)
    	elif 'Declined' in x[98]:
    		w_to_dest('8', output_file)
    	else:
    		w_to_dest('9', output_file)

    	#Marital status code
    	if 'Married' in x[100]:
    		w_to_dest('2', output_file)
    	elif 'Separated' in x[100]:
    		w_to_dest('3', output_file)
    	elif 'Divorced' in x[100]:
    		w_to_dest('4', output_file)
    	elif 'Widowed' in x[100]:
    		w_to_dest('5', output_file)
    	else:
    		w_to_dest('9', output_file)

    	#Zip code of residence at admission to this organization
    	int_test(x,56,5,'05999', output_file)

    	#Veteran status code
    	int_test(x,57,1,9, output_file)

    	#Legal status code
    	int_test(x,58,1,9, output_file)

    	#Source of referral code
    	int_test(x,59,2,'06', output_file)

    	#Residential arrangement at intake code
    	if len(x[84]) < 1:
    		w_to_dest(11, output_file)
    	else:
    		int_test(x,60,2,99, output_file)

    	#Living arrangement at intake code
    	int_test(x,61,1,9, output_file)

    	#SSI eligibility at intake code
    	int_test(x,62,1,9, output_file)

    	#Discontinuation status code
    	int_test(x,63,1,9, output_file)

    	#Referral upon discharge
    	int_test(x,64,2,'00', output_file)

    	#Current primary case worker
    	blank(5, output_file)

    	#Zip code of current residence
    	int_test(x,87,5,'05999', output_file)

    	#Current residential arrangement code
    	if len(x[84]) < 1:
    		w_to_dest(11, output_file)
    	else:
    		int_test(x,67,2,'99', output_file)

    	new_line(output_file)

    	#Current living arrangement
    	int_test(x,69,1,9, output_file)

    	#Current SSI eligibility
    	int_test(x,70,1,9, output_file)

    	#Current gross family income
    	output_file.write('99991')

    	#Date of most recent demographic data interview
    	int_test(x,72,6,'150101', output_file)

    	blank(59, output_file)

    	new_line(output_file)

    	blank(28, output_file)

    	#First name
    	if len(x[76]) > 11:
    		output_file.write(x[76][:11])
    	else:
    		output_file.write(x[76])
    		spacer = ' '
    		gap = 11 - len(x[76])
    		spacer = spacer * gap
    		output_file.write(spacer)

    	#Middle Initial
    	if len(x[77]) > 0:
    		w_to_dest(x[77][0], output_file)
    	else:
    		w_to_dest(' ', output_file)

    	#Last name
    	if len(x[78]) > 15:
    		output_file.write(x[78][:15])
    	else:
    		output_file.write(x[78])
    		spacer = ' '
    		gap = 15 - len(x[78])
    		spacer = spacer * gap
    		output_file.write(spacer)

    	#Modifier / Suffix
    	if len(x[79]) > 3:
    		output_file.write(x[79][:3])
    	else:
    		output_file.write(x[79])
    		spacer = ' '
    		gap = 3 - len(x[79])
    		spacer = spacer * gap
    		output_file.write(spacer)

    	#Social security number
    	ssn = ssn_format(x[96])
    	output_file.write(ssn)

    	#Date of death
    	int_test(x,81,8,'00000000', output_file)

    	#Social security number suffix
    	output_file.write(ssn[5:])

    	new_line(output_file)

    	#Street Address
    	string_limiter(x,84,48, output_file)

    	#City
    	string_limiter(x,85,15, output_file)

    	#State
    	output_file.write("VT")

    	#Zip code
    	int_test(x,87,5,'05999', output_file)

    	#Blank (for extra 4 digits that could be in zip code)
    	blank(4, output_file)

    	#Town code
    	city = x[85].upper()
    	if len(str(town_code[city])) < 3:
    		spacer = (3 - len(str(town_code[city]))) * '0'
    		output_file.write(spacer)
    		w_to_dest(town_code[city], output_file)
    	else:
    		w_to_dest(town_code[city], output_file)

    	new_line(output_file)

    	blank(27, output_file)

    	#Medicaid billing number
    	string_limiter(x,95,9, output_file)

    	#Account number
    	blank(12, output_file)

    	#Primary program assignment effective date
    	int_test(x,92,8,'20141001', output_file)

    	#Primary program end date
    	output_file.write('00000000')

    	#Birth year prefix
    	output_file.write('19')

    	#Dx ICD-10 Primary
    	prime_dx = x[12]
    	if '.' in prime_dx:
    		prime_dx = prime_dx.split('.')
    		prime_dx = prime_dx[0] + prime_dx[1]
    	if len(prime_dx) > 2:
    		if prime_dx not in icd_10_list:
    			prime_dx = '%s0' % prime_dx
    		w_to_dest(prime_dx, output_file)
    		spacer = ' ' * (7 - len(prime_dx))
    		w_to_dest(spacer, output_file)
    	else:
    		w_to_dest('       ', output_file)
    		error_logger(x,12)

    	#Dx ICD-10 Secondary
    	w_to_dest('       ', output_file)

    	#Dx ICD-10 Tertiary
    	w_to_dest('       ', output_file)

    	#Dx ICD-10 Quaternary
    	w_to_dest('       ', output_file)

    	new_line(output_file)

    	# -------------------------------------------------------------------------
    	# INNER SERVICES LOOP
    	# -------------------------------------------------------------------------
    	serv_count = 0

    	for y in services_list:
    		if name == y[13]:
    			serv_count += 1

    			#Record Identifier
    			output_file.write('2')

    			#Action code
    			blank(1, output_file)

    			#Blank (7 spaces)
    			blank(7, output_file)

    			#Date of Service
    			int_test(y,4,6,'ERR999', output_file)

    			#Blank (4 spaces)
    			blank(4, output_file)

    			#Duration of services
    			duration = int(y[5])
    			duration = duration/60.0
    			duration = round_to_quart(duration)
    			output_file.write(str(duration))
    			spacer = ' '
    			if len(str(duration).split('.')[1]) < 2:
    				output_file.write('0')
    				gap = 5 - len(str(duration))
    				spacer = spacer * gap
    				output_file.write(spacer)
    			else:
    				gap = 6 - len(str(duration))
    				spacer = spacer * gap
    				output_file.write(spacer)

    			#Program of service
    			if primary_prog == "1":
    				w_to_dest('04', output_file)
    			elif primary_prog == "2":
    				w_to_dest(12, output_file)
    			else:
    				print "Re-run this script with correct reponse to CRT/FFS prompt!"

    			#Cost center
    			output_file.write('48')

    			#Type of service code
    			serv_type = y[8]
    			if len(serv_type) == 3 and serv_type != 'N/A':
    				output_file.write(serv_type)
    			else:
    				output_file.write('A01')

    			#Location code
    			int_test(y,9,1,1, output_file)

    			#Count
    			output_file.write('1')

    			#ADAP Billable (blank)
    			blank(1, output_file)

    			#Staff Member ID#
    			int_test(y,12,5,'00999', output_file)

    			#Blank (9 spaces)
    			blank(9, output_file)

    			#HIV Information Given
    			blank(1, output_file)

    			#Account Number
    			blank(12, output_file)

    			#Reference Number
    			blank(10, output_file)

    			#Dx ICD-10 Primary
    			prime_dx = x[12]
    			if '.' in prime_dx:
    				prime_dx = prime_dx.split('.')
    				prime_dx = prime_dx[0] + prime_dx[1]
    			if len(prime_dx) > 2:
    				if prime_dx not in icd_10_list:
    					prime_dx = '%s0' % prime_dx
    				w_to_dest(prime_dx, output_file)
    				spacer = ' ' * (7 - len(prime_dx))
    				w_to_dest(spacer, output_file)
    			else:
    				w_to_dest('       ', output_file)
    				error_logger(y,9)

    			new_line(output_file)
