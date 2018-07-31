import csv

# -----------------------------------------------------------------------------
# INITIAL INPUT & FILES
#
# Preparing and initializing external files we're working with and getting the
# initial information about the data set we'll be running.
# -----------------------------------------------------------------------------

# FOR TESTING PURPOSES --------------------------------------------------------
# Comment out following lines if using for production
#file1 = 'ffsprofile10.csv' #profile file
#file2 = 'ffsservices10.csv' #services file
#begindate = '010101' #Begin Date of report (YYMMDD)
#enddate = '010101' #End Date of report (YYMMDD)
#primary_prog = '2' #If CRT, enter 1. If FFS, enter 2
# -----------------------------------------------------------------------------

# PRODUCTION FILE ARGUMENT ----------------------------------------------------
# Comment out the following line if testing
#script, begindate, enddate, file1, file2, primary_prog = argv
# -----------------------------------------------------------------------------

prime_program = ''
if primary_prog == '1':
    prime_program = 'CRT'
else:
    prime_program = 'FFS'

pre_profiles = open(file1)
pre_services = open(file2)

profiles = csv.reader(pre_profiles, delimiter = ';')
services = csv.reader(pre_services, delimiter = ';')

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
    if len(services_list_uncropped[x][5]) > 0 and services_list_uncropped[x][5] != '0':
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
