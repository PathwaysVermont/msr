import csv

def csv_array(csv_file):
# Creates a two-dimensional array of entries from a csv file
    with open(csv_file) as f:
        array = []
        data = csv.reader(f, delimiter=';')
        for x in data:
            array.append(x)
    return array

def services_crop(services_csv):
# Removes services from list that have no duration

    services_raw = csv_array(services_csv)
    services_list = []

    for x in range(len(services_raw)):
        if len(services_raw[x][5]) > 0 and services_raw[x][5] != '0':
            services_list.append(services_raw[x])
    return services_list

def services_names(services):
# Create a list of names present in services list for culling profiles
    s_names = []
    for service in services:
        s_names.append(service[13])
    return s_names

def profiles_crop(profiles_csv, services_csv):
# Creates list that has removed profiles without any services associated with it

    profiles_array = csv_array(profiles_csv)
    profiles_list = []
    names = services_names(services_crop(services_csv))

    for x in profiles_array:
        name = "%s, %s" % (x[78], x[76])
        if name in names:
            profiles_list.append(x)
    return profiles_list
