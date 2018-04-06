import msr_in
import collections
import icd_code_list

# Check for duplicated names, both inter- and intra- program
# Check for address/homelessness conflict
# Check for a Medicaid Billing number
# Check ICD Dx (formatting, not DSM, etc.)

#TO-DO: aggregate output under each individuals name, program

crt_names = []
for x in msr_in.crt_profile:
    name = "%s, %s" % (x[78], x[76])
    crt_names.append(name)

ffs_names = []
for x in msr_in.ffs_profile:
    name = "%s, %s" % (x[78], x[76])
    ffs_names.append(name)

# List comprehensions that count lists for duplicates and return them to a list
crt_duplicates = [i for i, count in collections.Counter(crt_names).items() if count > 1]
ffs_duplicates = [i for i, count in collections.Counter(ffs_names).items() if count > 1]

# Checks names in FFS against CRT to check for duplicates
cross_duplicates = []
for x in ffs_names:
    if x in crt_names:
        cross_duplicates.append(x)

# Check to see if client has address and correct homeless status
crt_homeless_address_conflict = []
ffs_homeless_address_conflict = []

def homeless_address_check(x):
    list = []
    for y in x:
        name = "%s, %s" % (y[78], y[76])
        if len(y[84]) < 1 and (y[60] != '11' or y[67] != '11'):
            list.append(name)
    return list

crt_homeless_address_conflict = homeless_address_check(msr_in.crt_profile)
ffs_homeless_address_conflict = homeless_address_check(msr_in.ffs_profile)

# Check to see that client has Medicaid Billing Number recorded properly
crt_medicaid_number = []
ffs_medicaid_number = []

def medicaid_check(x):
    list = []
    for y in x:
        name = "%s, %s" % (y[78], y[76])
        if len(y[95]) < 4:
            list.append(name)
    return list

crt_medicaid_number = medicaid_check(msr_in.crt_profile)
ffs_medicaid_number = medicaid_check(msr_in.ffs_profile)

# Check to see if an ICD 10 Dx is present, rather than DSM IV
def dx_check(x):
    list = []
    for y in x:
        name = "%s, %s" % (y[78], y[76])
        if len(y[12]) < 3 or y[12][0] != 'F' or y[12] not in icd_code_list.icd_10_list:
            list.append(name)
    return list

crt_dx_list = dx_check(msr_in.crt_profile)
ffs_dx_list = dx_check(msr_in.ffs_profile)

# Output Errors to text file for human consumption
output_file = 'Critical_Errors_%s.txt' % msr_in.month

header = 'MSR Data with Critical Errors\n\n'
dupes = (
    'CRT Duplicate Names: %s\n'
    'FFS Duplicate Names: %s\n'
    'Cross Program Duplicate Names: %s\n\n'
    ) % (crt_duplicates, ffs_duplicates, cross_duplicates)
address_conflicts = (
    'CRT Homeless/Address Conflicts: %s\n'
    'FFS Homeless/Address Conflicts: %s\n\n'
    ) % (crt_homeless_address_conflict, ffs_homeless_address_conflict)
medicaid_conflicts = (
    'CRT Medicaid Billing Number Errors: %s\n'
    'FFS Medicaid Billing Number Errors: %s\n\n'
    ) % (crt_medicaid_number, ffs_medicaid_number)
icd10_check = (
    'CRT Dx Error: %s\n'
    'FFS Dx Error: %s\n\n'
    ) % (crt_dx_list, ffs_dx_list)

with open(output_file, 'w') as output:
    output.write(header)
    output.write(dupes)
    output.write(address_conflicts)
    output.write(medicaid_conflicts)
    output.write(icd10_check)
