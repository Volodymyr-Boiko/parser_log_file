#! /usr/bin/python


import tarfile
from zipfile import ZipFile


class Archives(object):
    def __init__(self, arch_file, type_of_arch):
        self.arch_file = arch_file
        self.type_of_arch = type_of_arch

    def make_arch(self, *files):
        if self.type_of_arch == 'zip_file':
            with ZipFile(self.arch_file, 'w') as my_zip:
                for file_name in files:
                    my_zip.write(file_name)
                my_zip.close()
        else:
            with tarfile.open(self.arch_file, 'w:gz') as tar:
                for file_name in files:
                    tar.add(file_name)
                tar.close()

    def read_file_from_arch(self):
        test_dict = {}
        try:
            if self.type_of_arch == 'zip_file':
                with ZipFile(self.arch_file, 'r') as my_zip:
                    for item in self.__get_file_names():
                        test_dict[item] = my_zip.read(item)
                return test_dict
            else:
                with tarfile.open(self.arch_file, 'r:*') as tar:
                    for item in tar:
                        file_ = tar.extractfile(item)
                        test_dict[item.name] = file_.read()
                return test_dict
        except IOError:
            return {}

    def __get_file_names(self):
        try:
            with ZipFile(self.arch_file, 'r') as my_zip:
                return my_zip.namelist()
        except IOError:
            return []
