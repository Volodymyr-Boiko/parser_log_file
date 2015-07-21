#! /usr/bin/python
"""Makes archives and reads files that are in the archive"""


import tarfile
from zipfile import ZipFile


class Archives(object):
    """Makes archives and reads files that are in the archive"""
    def __init__(self, type_of_arch):
        # self.arch_file = arch_file
        self.type_of_arch = type_of_arch

    def make_arch(self, arch_file, *files):
        """Write the file(s) to the archive
        Args:
            files: file(s), are need to write to the archive
        """
        if self.type_of_arch == 'zip':
            with ZipFile(arch_file, 'w') as my_zip:
                for file_name in files:
                    my_zip.write(file_name)
                my_zip.close()
        elif self.type_of_arch == 'tar':
            with tarfile.open(arch_file, 'w:gz') as tar:
                for file_name in files:
                    tar.add(file_name)
                tar.close()

    def read_file_from_arch(self, arch_file):
        """Reads files from the archive
        Args:

        Return: dict, where key is the name of the file and value is
                file content
        """
        test_dict = {}
        try:
            if self.type_of_arch == 'zip':
                with ZipFile(arch_file, 'r') as my_zip:
                    for item in self.__get_file_names():
                        test_dict[item] = my_zip.read(item)
                return test_dict
            elif self.type_of_arch == 'tar':
                with tarfile.open(arch_file, 'r:*') as tar:
                    for item in tar:
                        file_ = tar.extractfile(item)
                        test_dict[item.name] = file_.read()
                return test_dict
        except IOError:
            return {}

    def __get_file_names(self, arch_file):
        """Gets names of the files from the archive
        Return: list of the names
        """
        try:
            with ZipFile(arch_file, 'r') as my_zip:
                return my_zip.namelist()
        except IOError:
            return []
