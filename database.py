#! /usr/bin/python
"""Create database"""


import json
import psycopg2


class DataBase(object):
    """Creates a new database session and create new cursors"""
    def __init__(self, user, dbname, password=None, port=5432):
        self.user = user
        self.dbname = dbname
        self.port = port
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to an existing database"""
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user)

    def get_cursor(self):
        """Open a cursor to perform database operations"""
        if self.conn is not None:
            self.cursor = self.conn.cursor()

    def execute_cur(self, command):
        """Execute a command. Make the changes to the database persistent"""
        self.cursor.execute(command)
        self.conn.commit()


class Model(DataBase):
    """Creates a new table and makes some operations"""
    def __init__(self, user, database, table_name, password=None,  schema=None):
        super(Model, self).__init__(user, database, password)
        self.table_name = table_name
        self.schema = schema
        self.__get_conn()

    def __get_conn(self):
        """Checks connection"""
        if self.conn is not None:
            self.connect()
            self.get_cursor()

    # def create_table(self, col1, col2):
    #     """Creates a new table with columns
    #     Args:
    #         col1: first column's name;
    #         col2: second column's name.
    #     """
    #     command = ('CREATE TABLE {} (id serial PRIMARY KEY NOT NULL UNIQUE, '
    #                '{} VARCHAR, '
    #                '{} VARCHAR);'.format(self.table_name, col1, col2))
    #     self.execute_cur(command)

    def create_table(self, *args):
        """Creates a new table with columns
        Args:
            col1: first column's name;
            col2: second column's name.
        """
        test_str = self.__format_string(*args)
        print test_str
        command = ('CREATE TABLE {} (id serial PRIMARY KEY NOT NULL UNIQUE, {});'.format(self.table_name, test_str))
        self.execute_cur(command)

    def insert_into_table(self, col1, val1, col2, val2):
        """Insert new data to the table's columns
        Args:
            col1: first column's name;
            val1: value of the first column;
            col2: second column's name;
            val2: value of the second column.
        """
        command = ('INSERT INTO {} '
                   '({}, {}) VALUES (\'{}\', '
                   '\'{}\');').format(self.table_name, col1, col2, val1, val2)
        self.execute_cur(command)

    def get_data_by_id(self, id_val, col1, col2):
        """Gets data from 'status' column by 'id' number
        Args:
            id_val: id value
            col1: first column's name;
            col2: second column's name.
        Return: Value of each column which taken by 'id' value.
        """
        command = ('SELECT {3}, {1}, {2} FROM {0} '
                   'WHERE {3}={4};'.format(self.table_name, col1, col2, 'id',
                                           str(id_val)))
        try:
            self.execute_cur(command)
            lst = json.dumps(self.cursor.fetchone())[1: -1].split(',')
            if len(lst) == 1:
                return 'There is no data in the table'
            else:
                return 'Name of the table is %s\n' \
                       'id value is %s\n' \
                       '%s value is %s\n' \
                       '%s value is %s' \
                       % (self.table_name, lst[0], col1, lst[1], col2, lst[2])
        except psycopg2.ProgrammingError:
            return 'Name of the table is %s\n' \
                   'Some of column name does not exist' % self.table_name

    def __format_string(self, *kwargs):
        lst = list(kwargs)
        lst_1 = []
        str_ = ''
        for item in range(0, len(lst), 2):
            lst_1.append(lst[item: item + 2])
        for item in lst_1:
            test_str = ' '.join(item)
            test_str += ','
            str_ += test_str
        lll = str_.split(',')
        lll.remove('')
        return ', '.join(lll)


# sub1 = "python string!"
# sub2 = "an arg"
#
# a = "i am a %s" % sub1
# b = "i am a {0}".format(sub1)
#
# c = "with %(kwarg)s!" % {'kwarg':sub2}
# d = "with {kwarg}!".format(kwarg=sub2)
#
# print a
# print b
# print c
# print d
#
# def ff(qqq='qqq', a='111'):
#     return '{} {}'.format(qqq, a)
#
# print ff()
#
# def format_string(**kwargs):
#     string = ''
#     for item in kwargs:
#         string += '{} '.format(kwargs.get(item))
#     return string
#
# print format_string(col1='user', type1='vboiko', col2='site', type2='tsn.ua')
#
def format_string(*kwargs):
    lst = list(kwargs)
    lst_1 = []
    str_ = ''
    for item in range(0, len(lst), 2):
        lst_1.append(lst[item: item + 2])
    for item in lst_1:
        test_str = ' '.join(item)
        test_str += ','
        str_ += test_str
    lll = str_.split(',')
    lll.remove('')
    return ', '.join(lll)

# print format_string('user', 'vboiko', 'site', 'tsn.ua', 'uniq', '2')
