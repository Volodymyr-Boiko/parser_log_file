#! /usr/bin/python


from run import get_model
from run import create_table
from run import del_table
from run import insert_data
from run import get_data
from run import update_data
from run import delete_data


def get_cur():
    user = raw_input('Please input user_name: ')
    database = raw_input('Please input a name of the database: ')
    table_name = raw_input('Please input a name of the data table: ')
    return get_model(user, database, table_name)


def main():
    possible_choice = ['create data table', 'drop data table', 'insert data',
                       'get data', 'update data', 'delete data']
    choice = raw_input('Please input your choice: ')
    if choice in possible_choice:
        cur = get_cur()
        if choice == 'create data table':
            num_of_cols = int(raw_input('Please insert a number of columns: '))
            cols = {}
            for item in range(num_of_cols):
                col_name = raw_input('Please insert a column name: ')
                col_type = raw_input('Please insert a column type: ')
                cols[col_name] = col_type
            return create_table(cur, **cols)
        elif choice == 'drop data table':
            return del_table(cur)
        elif choice == 'insert data':
            file_name = raw_input('Please input name of the log file: ')
            key1 = raw_input('Please input the first key: ')
            key2 = raw_input('Please input the second key: ')
            cols = []
            num_of_cols = int(raw_input('Please insert a number of columns: '))
            for item in range(num_of_cols):
                col_name = raw_input('Please insert a {} column '
                                     'name: '.format(item + 1))
                cols.append(col_name)
            uniq = raw_input('Please chose \'data\' or \'calc\': ')
            archive = {'yes': True, 'no': False}
            arch = raw_input('Read from an archive? Please input \'yes\' or '
                             '\'no\' (default \'no\'): ')
            return insert_data(cur, file_name, key1, key2, cols, uniq,
                               archive.get(arch, False))
        elif choice == 'get data':
            id_val = int(raw_input('Please insert the \'id\' value: '))
            return get_data(cur, id_val)
        elif choice == 'update data':
            id_val = int(raw_input('Please insert the \'id\' value: '))
            cols_to_update = raw_input('Please input a column or columns to '
                                       'update: ')
            cols_vals = {}
            for item in cols_to_update.split(', '):
                cols_vals[item] = raw_input('Please input a new value for the '
                                            '\'{}\' column: '.format(item))
            return update_data(cur, id_val, **cols_vals)
        elif choice == 'delete data':
            cols = raw_input('Please input a column or columns to '
                             'delete: ')
            cols_vals = {}
            for item in cols.split(', '):
                cols_vals[item] = raw_input('Please input a value of the '
                                            '\'{}\' column: '.format(item))
            return delete_data(cur, **cols_vals)


if __name__ == '__main__':
    main()

"""дописати можливість відображення всіх варіантів таблиць при запиту про назву
 таблиці, забрати повторення, таке саме зробити для колонок, якщо таблиця існує
 - показати всі колонки"""
