import os, sys
import writer.file_writer as file_writer
import writer.msr_files as msr_files

def test_msr():
    pass

def make_msr():
    pass

if __name__ == '__main__':
    month = raw_input("What month is this reporting on? (01-12) > ")
    year = raw_input("What year is this reporting on? (use last two digits of year, e.g. 19) > ")

    base_path = sys.path[0]
    print(base_path)

    crt_prof_file = os.path.join(base_path, 'input_files', "crtprofile{}{}.csv".format(month, year))
    crt_serv_file = os.path.join(base_path, 'input_files', "crtservices{}{}.csv".format(month, year))
    ffs_prof_file = os.path.join(base_path, 'input_files', "ffsprofile{}{}.csv".format(month, year))
    ffs_serv_file = os.path.join(base_path, 'input_files', "ffsservices{}{}.csv".format(month, year))

    crt_profile = msr_files.profiles_crop(crt_prof_file, crt_serv_file)
    crt_services = msr_files.services_crop(crt_serv_file)
    ffs_profile = msr_files.profiles_crop(ffs_prof_file, ffs_serv_file)
    ffs_services = msr_files.services_crop(ffs_serv_file)

    begindate = "{}{}01".format(year, month)
    enddate = "{}{}{}".format(year, month, file_writer.month_last_day[month])

    output_file_name = "PW{}{}ms.dat".format(year, month)
    filepath = os.path.join(sys.path[0], 'output_files', output_file_name)
    output_file = open(filepath, 'w')

    file_writer.msr_file(crt_profile, crt_services, "1", begindate, enddate, output_file)
    file_writer.msr_file(ffs_profile, ffs_services, "2", begindate, begindate, output_file)

    output_file.close()
