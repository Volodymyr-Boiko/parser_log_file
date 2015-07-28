#! /usr/bin/python
"""Gets list of dicts with unique data"""


import re


REGEX = '([(\d\.)]+) (.*?) (.*?) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
NAMES = ('host', 'indent', 'user', 'time', 'request', 'status', 'size',
         'referrer', 'user agent')


def read_file(file_name, arch=False):
    """Reads log file
    Args:
        file_name: name of the file
    Return: list of the lines from the file
    """
    if not arch:
        return _read_file(file_name).split('\n')
    else:
        return file_name.split('\n')


def make_line_list(file_name, arch=False):
    """Makes list of file's lines in the dict view
    Args:
        file_name: name of the file
    Return: list of dicts
    """
    global REGEX, NAMES
    lst = []
    test_lst = read_file(file_name, arch)
    if '' in test_lst:
        test_lst.remove('')
    for line in test_lst:
        try:
            reg = re.match(REGEX, line).groups()
            test_dict = dict(zip(NAMES, reg))
        except AttributeError:
            NAMES = ('host', 'indent', 'user', 'time', 'request', 'status',
                     'type', 'size', 'referrer', 'user agent')
            REGEX = '([(\d\.)]+) (.*?) (.*?) \[(.*?)\] "(.*?)" (\d+) (.*?) ' \
                    '"(.*?)" "(.*?)" "(.*?)"'
            reg = re.match(REGEX, line).groups()
            test_dict = dict(zip(NAMES, reg))
        lst.append(test_dict)
    return lst


def get_uniq_data(file_name, key1, key2, arch=False):
    """Gets list of dicts with unique data
    Args:
        file_name: name of the file;
        key1: first key;
        key2: second key
    Return: list of dicts with unique users and sites
    """
    test_list = make_line_list(file_name, arch)
    lst = []
    if _check_item(key1, key2):
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
    else:
        return []


def calc_uniq_data(file_name, key1, key2, arch=False):
    """Gets list of dicts with unique data
    Args:
        file_name: name of the file;
        key1: first key;
        key2: second key
    Return: dict with number of unique users and sites
    """
    test_list = get_uniq_data(file_name, key1, key2, arch)
    test_dict = {}
    lst_key1 = []
    lst_key2 = []
    if _check_item(key1, key2):
        for item in test_list:
            lst_key1.append(item.get(key1, 0))
            lst_key2.append(item.get(key2, 0))
        test_dict[key1] = len(lst_key1)
        test_dict[key2] = len(lst_key2)
        return test_dict
    else:
        return {}


def _read_file(file_name):
    """Reads log file
    Args:
        file_name: name of the file
    Return: file as a string
    """
    try:
        with open(file_name, 'r') as file_to_read:
            return file_to_read.read()
    except IOError:
        return ''


def _check_item(key1, key2):
    global NAMES
    if key1 in NAMES and key2 in NAMES:
        return True
    else:
        return False
