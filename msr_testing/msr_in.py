import csv

month = '02'

crt_profile_file = 'crtprofile%s18.csv' % month
crt_services_file = 'crtservices%s18.csv' % month
ffs_profile_file = 'ffsprofile%s18.csv' % month
ffs_services_file = 'ffsservices%s18.csv' % month

def ease(x):
# Creates an easy to use list of entries from a csv file
    with open(x) as f:
        list = []
        data = csv.reader(f, delimiter=';')
        for x in data:
            list.append(x)
    return list

def services_crop(services_raw):
# Removes services from list that have no duration
    services_list = []
    for x in range(len(services_raw)):
        if len(services_raw[x][5]) > 0 and services_raw[x][5] != '0':
            services_list.append(services_raw[x])
    return services_list

def services_names(services_crop):
    s_names = []
    for x in services_crop:
        s_names.append(x[13])
    return s_names

def profiles_crop(profile_raw, services_cropped):
# Creates list that has removed profiles without any services associated with it
    profile_list = []
    names = services_names(services_cropped)
    for x in profile_raw:
        name = "%s, %s" % (x[78], x[76])
        if name in names:
            profile_list.append(x)
    return profile_list

crt_services = services_crop(ease(crt_services_file))
crt_profile = profiles_crop(ease(crt_profile_file), crt_services)
ffs_services = services_crop(ease(ffs_services_file))
ffs_profile = profiles_crop(ease(ffs_profile_file), ffs_services)
