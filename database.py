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

    def create_table(self, *args):
        """Creates a new table with columns
        Args:
            *args: columns' name and columns' type.
        """
        test_str = self.__format_string(*args)
        command = ('CREATE TABLE {} (id serial PRIMARY KEY NOT NULL UNIQUE,'
                   ' {});'.format(self.table_name, test_str))
        try:
            self.execute_cur(command)
            return 'Data table created'
        except psycopg2.ProgrammingError:
            return 'Data table %s already exist.\n' \
                   'Please insert another table-name' % self.table_name

    def insert_into_table(self, *columns, **values):
        """Insert new data to the table's columns
        Args:
            *columns: columns' name;
            **values: values of the columns
        """
        col_string = self.__form_str_insert('column', *columns)
        val_string = self.__form_str_insert('value', **values)
        command = ('INSERT INTO {} '
                   '({}) VALUES ({});').format(self.table_name, col_string,
                                               val_string)
        try:
            self.execute_cur(command)
            return 'Data insert correctly'
        except psycopg2.ProgrammingError:
            return 'Please insert correct name of the columns'

    def get_data_by_id(self, id_val, cols=True, *columns):
        """Gets data from 'status' column by 'id' number
        Args:
            id_val: id value
            cols: switcher;
            *columns: columns' name.
        Return: Value of each column which taken by 'id' value.
        """
        sel_str = self.__form_str_get(cols, *columns)
        command = ('SELECT {} FROM {} WHERE '
                   '{}={};'.format(sel_str, self.table_name, 'id', str(id_val)))
        col = list(columns)
        try:
            self.execute_cur(command)
            lst = json.dumps(self.cursor.fetchone())[1: -1].split(',')
            if 'ul' in lst:
                return 'Name of the table is %s\n' \
                       'Data, taken by \'id\' value does not exist' % \
                       self.table_name
            elif cols:
                result = dict(zip(col, lst))
                return self.__get_data_from_table(cols, **result)
            elif not cols:
                test_lst = []
                for item in lst:
                    test_lst.append(str(lst.index(item) + 1))
                test_dict = dict(zip(test_lst, lst))
                return self.__get_data_from_table(cols, **test_dict)
        except psycopg2.ProgrammingError:
            return 'Name of the table is %s\n' \
                   'This column(s) does not exist' % self.table_name

    def __format_string(self, *args):
        """Creates a part of command
        Args:
            *args: *args: columns' name and columns' type.
        Return: string, with columns' name and columns' type
        """
        lst = list(args)
        lst_pair = []
        string = ''
        for item in range(0, len(lst), 2):
            lst_pair.append(lst[item: item + 2])
        for item in lst_pair:
            test_str = ' '.join(item)
            test_str += ', '
            string += test_str
        return string[0: -2]

    def __form_str_insert(self, intent='column', *args, **kwargs):
        """Creates a part of command
        Args:
            intent: switcher;
            *args: columns' name;
            **kwargs: values of the columns
        Return: string, with columns' name or columns' type
        """
        string = ''
        if intent == 'column':
            for item in args:
                string += '{}, '.format(item)
        elif intent == 'value':
            for name in kwargs:
                string += '\'{}\', '.format(kwargs[name])
        return string[0: -2]

    def __form_str_get(self, cols=True, *columns):
        """Creates a part of command
        Args:
            cols: switcher;
            *columns: columns' name.
        Return: string
        """
        select_str = ''
        if cols:
            for item in columns:
                select_str += '{}, '.format(item)
            return select_str[0: -2]
        else:
            select_str = '*'
            return select_str

    def __get_data_from_table(self, cols=True, **kwargs):
        """Creates a part of command
        Args:
            cols: switcher;
            *kwargs: columns' value.
        Return: string
        """
        res_str = 'Name of the table is %s\n' % self.table_name
        if cols:
            for item in kwargs:
                res_str += 'value of the {} column is {}\n'.format(item,
                                                                   kwargs[item])
        elif not cols:
            for item in kwargs:
                res_str += 'value of the {} column is {}\n'.format(str(item),
                                                                   kwargs[item])
        return res_str
