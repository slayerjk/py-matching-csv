"""
Main applications functions
"""
from csv import DictReader, DictWriter


def parse_csv(file) -> list:
    """
    Parsing csv file and return data(list of csv.DictReader)
    :param file: csv file path
    :return: list
    """
    with open(file, 'r', encoding='utf-8') as in_f:
        reader = DictReader(in_f, delimiter=',')
        result = [line for line in reader]
    return result


def matching_data(old: list, new: list) -> (list, list, list):
    """
    Match old and new data and return two lists
    new_hosts and excluded_hosts
    :param old: old data(list)
    :param new: new data(list)
    :return: list, list
    """
    changed_hosts = []

    new_hosts = []
    for d_new in new:
        counter = 0
        for d_old in old:
            if d_new['IP'] in d_old['IP']:
                counter += 1
                break
            else:
                if d_new['Name'] == d_old['Name']:
                    changed_hosts.append(d_new)
                    counter += 1
                    break
                else:
                    continue
        if counter == 0:
            new_hosts.append(d_new)

    excluded_hosts = []
    for d_old in old:
        counter = 0
        for d_new in new:
            if d_old['IP'] in d_new['IP']:
                counter += 1
                break
            else:
                if d_new['Name'] == d_old['Name']:
                    if d_new not in changed_hosts:
                        changed_hosts.append(d_new)
                    counter += 1
                    break
                else:
                    continue
        if counter == 0:
            # print(d_old)
            excluded_hosts.append(d_old)
    return new_hosts, excluded_hosts, changed_hosts


def write_csv(data: list, file_path: str):
    """
    Write matched data to csv file
    :param data: list of dicts
    :param file_path: path of file to write in
    :return: None
    """
    csv_columns = data[0].keys()
    with open(file_path, 'w', encoding='utf-8', newline='') as f_in:
        writer = DictWriter(f_in, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()
        writer.writerows(data)
