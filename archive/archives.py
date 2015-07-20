#! /usr/bin/python


import tarfile
from zipfile import ZipFile


class ZipTransfer(object):

    def __init__(self, zip_file, *files):
        self.zip_file = zip_file
        self.files = files

    def make_zip(self):
        with ZipFile(self.zip_file, 'w') as my_zip:
            for file_name in self.files:
                my_zip.write(file_name)
            my_zip.close()

    def read_file_from_zip(self):
        test_dict = {}
        try:
            with ZipFile(self.zip_file, 'r') as my_zip:
                for item in self.__get_file_names():
                    test_dict[item] = my_zip.read(item)
            return test_dict
        except IOError:
            return {}

    def __get_file_names(self):
        try:
            with ZipFile(self.zip_file, 'r') as my_zip:
                return my_zip.namelist()
        except IOError:
            return []


def create_arch(tar_file, file_name):
    return tarfile.open(tar_file, 'w|', file_name)


if __name__ == '__main__':
    # zip_creator = ZipTransfer('file.zip', 'README.md', 'access.log')
    # zip_creator.make_zip()
    # print zip_creator.read_file_from_zip()
    create_arch('access.gzip', 'access.log')
