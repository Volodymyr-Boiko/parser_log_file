#! /usr/bin/python
"""Create database"""


import json
import logging
import psycopg2


logging.basicConfig(level=logging.DEBUG)


class DataBase(object):
    """Creates a new database session and create new cursors"""
    def __init__(self, user, dbname, password=None, port=5432):
        self.user = user
        self.dbname = dbname
        self.port = port
        self.password = password
        self.conn = None
        self.cursor = None
        # self.desc = None

    def connect(self):
        """Connect to an existing database"""
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user)

    def get_cursor(self):
        """Open a cursor to perform database operations"""
        if self.conn is not None:
            self.cursor = self.conn.cursor()

    def descr(self):
        if self.conn is not None:
            desc = self.cursor.description
            return desc

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
            # self.descr()

    def create_table(self, **kwargs):
        """Creates a new table with columns
        Args:
            args: columns' name and columns' type.
        """
        test_str = self.__format_string(**kwargs)
        command = ('CREATE TABLE {} (id serial PRIMARY KEY NOT NULL UNIQUE,'
                   ' {});'.format(self.table_name, test_str))
        try:
            self.execute_cur(command)
            logging.info('Data table created')
        except psycopg2.ProgrammingError:
            logging.error('Data table %s already exist.\n' \
                          'Please insert another table-name' % self.table_name)

    def drop_table(self):
        """Drops data-table"""
        command = 'DROP TABLE {}'.format(self.table_name)
        try:
            self.execute_cur(command)
            logging.info('Data table %s dropped' % self.table_name)
        except psycopg2.ProgrammingError:
            logging.error('Data table %s already dropped' % self.table_name)

    def insert_into_table(self, *columns, **values):
        """Insert new data to the table's columns
        Args:
            columns: columns' name;
            values: values of the columns
        """
        col_string = self.__form_str_insert('column', *columns)
        val_string = self.__form_str_insert('value', **values)
        command = ('INSERT INTO {} '
                   '({}) VALUES ({});').format(self.table_name, col_string,
                                               val_string)
        try:
            self.execute_cur(command)
            logging.info('Data insert correctly')
        except psycopg2.InternalError, psycopg2.ProgrammingError:
            logging.error('Please insert correct name of the '
                          'columns or the keys')

    def get_data_by_id(self, id_val, *columns):
        """Gets data from 'status' column by 'id' number
        Args:
            id_val: id value
            cols: switcher;
            columns: columns' name.
        Return: Value of each column which taken by 'id' value.
        """
        if isinstance(id_val, int):
            command = ('SELECT * FROM {} WHERE '
                       '{}={};'.format(self.table_name, 'id', str(id_val)))
            col = list(columns)
            # col = self.get_descr()
            try:
                self.execute_cur(command)
                lst = json.dumps(self.cursor.fetchone())[1: -1].split(',')
                if 'ul' in lst:
                    logging.warning('Name of the table is %s\n' 'Data, taken by '
                                    '\'id\' value does not exist' %
                                    self.table_name)
                else:
                    result = dict(zip(col, lst))
                    return self.__get_data_from_table(**result)
            except psycopg2.ProgrammingError:
                logging.error('Name of the table is %s\n' \
                              'This column(s) does not exist' % self.table_name)
        else:
            logging.error('\'id\' must be integer')

    def __format_string(self, **kwargs):
        """Creates a part of command
        Args:
            args: columns' name and columns' type.
        Return: string, with columns' name and columns' type
        """
        dct = dict(kwargs)
        string = ''
        for item in dct:
            string += '{} {}, '.format(item, dct[item])
        return string[0: -2]

    def __form_str_insert(self, intent='column', *args, **kwargs):
        """Creates a part of command
        Args:
            intent: switcher;
            args: columns' name;
            kwargs: values of the columns
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

    def __get_data_from_table(self, **kwargs):
        """Creates a part of command
        Args:
            cols: switcher;
            kwargs: columns' value.
        Return: string with the results
        """
        res_str = 'Name of the table is %s\n' % self.table_name
        for item in kwargs:
            res_str += 'value of the {} column is {}\n'.format(item,
                                                               kwargs[item])
        return res_str

    def get_descr(self):
        colnames = [desc[0] for desc in self.descr()]
        return colnames
