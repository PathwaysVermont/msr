import os, sys
import writer.file_writer as file_writer
import writer.msr_files as msr_files
import writer.profile_check as profile_check

def exclude(profile_list, services_list, prog):
    for profile in profile_list:
        name = "{}, {}".format(profile[78], profile[76])
        if name in profile_check.dx_check(profile_list):
            profile_list.remove(profile)
            service_count = 0
            service_time = 0
            for service in services_list:
                if name == service[13]:
                    service_count += 1
                    service_time += int(service[5])
            print("{} ({}): no Dx - {} services, {} minutes".format(name, prog, service_count, service_time))
        if name in profile_check.medicaid_number_check(profile_list):
            profile_list.remove(profile)
            service_count = 0
            service_time = 0
            for service in services_list:
                if name == service[13]:
                    service_count += 1
                    service_time += int(service[5])
            print("{} ({}): no medicaid number - {} services, {} minutes".format(name, prog, service_count, service_time))

def make_msr(crt_profile, ffs_profile, crt_services, ffs_services, month, year):
    begindate = "{}{}01".format(year, month)
    enddate = "{}{}{}".format(year, month, file_writer.month_last_day[month])

    print("\n")
    print("Service Recipient Records Removed:")
    exclude(crt_profile, crt_services, "CRT")
    exclude(ffs_profile, ffs_services, "FFS")

    output_file_name = "PW{}{}ms.dat".format(year, month)
    filepath = os.path.join(sys.path[0], 'output_files', output_file_name)
    output_file = open(filepath, 'w')

    file_writer.msr_file(crt_profile, crt_services, "1", begindate, enddate, output_file)
    file_writer.msr_file(ffs_profile, ffs_services, "2", begindate, begindate, output_file)

    output_file.close()
    print("\nMSR file has been written. You can find it in {}".format(os.path.join(sys.path[0], 'output_files')))

def test_msr():
    pass

if __name__ == '__main__':
    test_or_run = int(raw_input("Run MSR File Writer(1) or Profile Checker (2)? > "))

    month = raw_input("What MONTH is this reporting on? (01-12) > ")
    year = raw_input("What YEAR is this reporting on? (use last two digits of year, e.g. 19) > ")

    base_path = sys.path[0]

    crt_prof_file = os.path.join(base_path, 'input_files', "crtprofile{}{}.csv".format(month, year))
    crt_serv_file = os.path.join(base_path, 'input_files', "crtservices{}{}.csv".format(month, year))
    ffs_prof_file = os.path.join(base_path, 'input_files', "ffsprofile{}{}.csv".format(month, year))
    ffs_serv_file = os.path.join(base_path, 'input_files', "ffsservices{}{}.csv".format(month, year))

    crt_profile = msr_files.profiles_crop(crt_prof_file, crt_serv_file)
    crt_services = msr_files.services_crop(crt_serv_file)
    ffs_profile = msr_files.profiles_crop(ffs_prof_file, ffs_serv_file)
    ffs_services = msr_files.services_crop(ffs_serv_file)

    # begindate = "{}{}01".format(year, month)
    # enddate = "{}{}{}".format(year, month, file_writer.month_last_day[month])

    if test_or_run == 1:
        make_msr(crt_profile, ffs_profile, crt_services, ffs_services, month, year)

    elif test_or_run == 2:
        profile_check.print_check(crt_profile, ffs_profile)

    else:
        print("Run this again. You didn't choose a valid option (1 or 2).")
