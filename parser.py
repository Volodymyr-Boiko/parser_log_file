#! /usr/bin/python
"""Gets list of dicts with unique data"""


import re


regex = '([(\d\.)]+) (.*?) (.*?) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
names = ('host', 'indent', 'user', 'time', 'request', 'status', 'size',
         'referrer', 'user agent')


def read_file(file_name):
    """Reads log file
    Args:
        file_name: name of the file
    Return: list of the lines from the file
    """
    with open(file_name, 'r') as file_to_read:
        return file_to_read.read().split('\n')


def make_line_list(file_name):
    """Makes list of file's lines in the dict view
    Args:
        file_name: name of the file
    Return: list of dicts
    """
    global regex, names
    lst = []
    test_lst = read_file(file_name)
    if '' in test_lst:
        test_lst.remove('')
    for line in test_lst:
        try:
            reg = re.match(regex, line).groups()
            test_dict = dict(zip(names, reg))
        except AttributeError:
            names = ('host', 'indent', 'user', 'time', 'request', 'status',
                     'type', 'size', 'referrer', 'user agent')
            regex = '([(\d\.)]+) (.*?) (.*?) \[(.*?)\] "(.*?)" (\d+) (.*?) ' \
                    '"(.*?)" "(.*?)" "(.*?)"'
            reg = re.match(regex, line).groups()
            test_dict = dict(zip(names, reg))
        lst.append(test_dict)
    return lst


def get_uniq_data(file_name, key1, key2):
    """Gets list of dicts with unique data
    Args:
        file_name: name of the file;
        key1: first key;
        key2: second key
    Return: list of dicts with unique users and sites
    """
    test_list = make_line_list(file_name)
    lst = []
    for item in test_list:
        lst.append({key1: item.get(key1, ''), key2: item.get(key2, '')})
    collection = set()
    new_lst = []
    for item in lst:
        tup = tuple(item.items())
        if tup not in collection:
            collection.add(tup)
            new_lst.append(item)
    return new_lst


def calc_uniq_data(file_name, key1, key2):
    """Gets list of dicts with unique data
    Args:
        file_name: name of the file;
        key1: first key;
        key2: second key
    Return: dict with number of unique users and sites
    """
    test_list = get_uniq_data(file_name, key1, key2)
    test_dict = {}
    lst_key1 = []
    lst_key2 = []
    for item in test_list:
        lst_key1.append(item.get(key1))
        lst_key2.append(item.get(key2))
    test_dict['user'] = len(lst_key1)
    test_dict['indent'] = len(lst_key2)
    return test_dict
