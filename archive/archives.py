#! /usr/bin/python


import tarfile
from zipfile import ZipFile


# class ZipTransfer(object):
#
#     def __init__(self, zip_file, *files):
#         self.zip_file = zip_file
#         self.files = files
#
#     def make_zip(self):
#         with ZipFile(self.zip_file, 'w') as my_zip:
#             for file_name in self.files:
#                 my_zip.write(file_name)
#             my_zip.close()
#
#     def read_file_from_zip(self):
#         test_dict = {}
#         try:
#             with ZipFile(self.zip_file, 'r') as my_zip:
#                 for item in self.__get_file_names():
#                     test_dict[item] = my_zip.read(item)
#             return test_dict
#         except IOError:
#             return {}
#
#     def __get_file_names(self):
#         try:
#             with ZipFile(self.zip_file, 'r') as my_zip:
#                 return my_zip.namelist()
#         except IOError:
#             return []

class Archives(object):
    def __init__(self, arch_file, *files):
        self.arch_file = arch_file
        self.files = files

    def make_arch(self):
        if self.arch_file.endswith('zip'):
            with ZipFile(self.arch_file, 'w') as my_zip:
                for file_name in self.files:
                    my_zip.write(file_name)
                my_zip.close()
        elif self.arch_file.endswith('tar'):
            with tarfile.open(self.arch_file, 'w:gz') as tar:
                for file_name in self.files:
                    tar.add(file_name)
                tar.close()

    def read_file_from_zip(self):
        test_dict = {}
        try:
            with ZipFile(self.arch_file, 'r') as my_zip:
                for item in self.__get_file_names():
                    test_dict[item] = my_zip.read(item)
            return test_dict
        except IOError:
            return {}

    def __get_file_names(self):
        try:
            with ZipFile(self.arch_file, 'r') as my_zip:
                return my_zip.namelist()
        except IOError:
            return []


def create_arch(tar_file, *files):
    with tarfile.open(tar_file, 'w:gz') as tar:
        for file_name in files:
            tar.add(file_name)
        tar.close()


def get_name_tar(tar_file):
    tar = tarfile.open(tar_file, 'r')
    return tar.getnames()


def read_file(tar_file):
    with tarfile.open(tar_file, 'r') as tar:
        return tar.extractall()


if __name__ == '__main__':
    create_arch('access.tar', 'access.log', '__init__.py')
    print get_name_tar('access.tar')
    print read_file('access.tar')
