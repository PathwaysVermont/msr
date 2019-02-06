import collections
import icd_code_list
from town_code import town_code

def internal_duplicate_check(profiles_list):
    names = []
    for profile in profiles_list:
        name = "{}, {}".format(profile[78], profile[76])
        names.append(name)
    return [i for i, count in collections.Counter(names).items() if count > 1]

def cross_prog_duplicate_check(crt_profiles_list, ffs_profiles_list):

    crt_names = []
    for profile in crt_profiles_list:
        name = "{}, {}".format(profile[78], profile[76])
        crt_names.append(name)

    ffs_names = []
    for profile in ffs_profiles_list:
        name = "{}, {}".format(profile[78], profile[76])
        ffs_names.append(name)

    cross_prog_duplicates = []
    for ffs_name in ffs_names:
        if ffs_name in crt_names:
            cross_prog_duplicates.append(ffs_name)

    return cross_prog_duplicates

def medicaid_number_check(profiles_list):
    list = []
    for profile in profiles_list:
        if len(profile[95]) < 4:
            list.append("{}, {}".format(profile[78], profile[76]))
    return list

def dx_check(profiles_list):
    list = []
    for profile in profiles_list:
        if len(profile[12]) < 3 or profile[12][0] != 'F' or profile[12] not in icd_code_list.icd_10_list:
            name = "{}, {}".format(profile[78], profile[76])
            list.append(name)
    return list

def town_code_check(crt_profiles, ffs_profiles):
    list = []
    for profile in crt_profiles:
        if profile[85].upper() not in town_code:
            list.append(profile[85])
    for profile in ffs_profiles:
        if profile[85].upper() not in town_code:
            list.append(profile[85])
    return list

def print_check(crtprofile, ffsprofile):

    print("\n")
    print("#########################")
    print("Profile Attribute Testing")
    print("#########################")
    print("\n")
    print("People appearing multiple times:")
    print("Within CRT: {}".format(internal_duplicate_check(crtprofile)))
    print("Within FFS: {}".format(internal_duplicate_check(ffsprofile)))
    print("Across programs: {}".format(cross_prog_duplicate_check(crtprofile, ffsprofile)))
    print("\n")
    print("People Missing a Medicaid Billing Number:")
    print("Within CRT: {}".format(medicaid_number_check(crtprofile)))
    print("Within FFS: {}".format(medicaid_number_check(ffsprofile)))
    print("\n")
    print("People Missing a Dx:")
    print("Within CRT: {}".format(dx_check(crtprofile)))
    print("Within FFS: {}".format(dx_check(ffsprofile)))
    print("\n")
    print("Missing Town Codes")
    print("Towns: {}".format(town_code_check(crtprofile, ffsprofile)))


if __name__ == '__main__':
    import msr_files
    crt_profiles = msr_files.profiles_crop('crtprofile1018.csv','crtservices1018.csv')
    ffs_profiles = msr_files.profiles_crop('ffsprofile1018.csv','ffsservices1018.csv')

    print("\n")
    print("#########################")
    print("Profile Attribute Check")
    print("#########################")
    print("\n")
    print("People appearing multiple times:")
    print("Within CRT: {}".format(internal_duplicate_check(crt_profiles)))
    print("Within FFS: {}".format(internal_duplicate_check(ffs_profiles)))
    print("Across programs: {}".format(cross_prog_duplicate_check(crt_profiles, ffs_profiles)))
    print("\n")
    print("People Missing a Medicaid Billing Number:")
    print("Within CRT: {}".format(medicaid_number_check(crt_profiles)))
    print("Within FFS: {}".format(medicaid_number_check(ffs_profiles)))
    print("\n")
    print("People Missing a Dx:")
    print("Within CRT: {}".format(dx_check(crt_profiles)))
    print("Within FFS: {}".format(dx_check(ffs_profiles)))
