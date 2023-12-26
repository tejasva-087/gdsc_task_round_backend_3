import mysql.connector as sql


class TodoDBConnector:
    __tabl_type__ = [['id', 'int'], ["title", "varchar(30)"], ["description", "varchar(150)"], ["completed", "char(5)"]]

    def __init__(self, host: str, user: str, password: str, database: str, table: str):
        # Assigning variables
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        # Connecting to database
        self.connection = self.__connection__()
        self.cursor = self.connection.cursor()

        # Some necessary tasks
        self.__check_database__()
        self.__check_tables__()

    def __connection__(self):  # Connecting to database
        try:
            connection_obj = sql.connect(host=self.host, user=self.user, password=self.password)
            if connection_obj.is_connected():
                return connection_obj

        except Exception:
            raise ConnectionError("Connection can not be established")

    def __check_database__(self):  # Checking for database
        self.cursor.execute('SHOW DATABASES;')
        data = self.cursor.fetchall()
        if (self.database,) in data:
            self.cursor.execute(f'USE {self.database};')
        else:
            self.cursor.execute(f'CREATE DATABASE {self.database};')
            self.cursor.execute(f'USE {self.database};')

    def __check_tables__(self):
        self.cursor.execute('SHOW TABLES;')
        data = self.cursor.fetchall()
        if (self.table, ) not in data:
            self.cursor.execute(f'''
                CREATE TABLE {self.table}
                (id INT PRIMARY KEY,
                title VARCHAR(30) NOT NULL,
                description VARCHAR(150) NOT NULL,
                completed CHAR(5) NOT NULL);
            ''')
        else:
            self.cursor.execute(f'''DESC {self.table};''')
            data = self.cursor.fetchall()
            if len(data) != 4:
                raise Exception('Table exist but is not fit for storing the content')
            for i in range(len(data)):
                if not(data[i][0] == self.__tabl_type__[i][0] and data[i][1] == self.__tabl_type__[i][1]):
                    raise Exception('Table exist but is not fit for storing the content')

    def get_all_todos(self):
        self.cursor.execute(f'SELECT * FROM {self.table}')
        return self.cursor.fetchall()

    def get_todo_by_id(self, todo_id):
        data = self.get_all_todos()
        for i in data:
            if i[0] == todo_id:
                return i
        else:
            raise Exception("id does not exist")

    def create_todo(self, title, description, completed):
        table_data_len = len(self.get_all_todos())
        self.cursor.execute(f'''
            INSERT INTO {self.table}
            (id, title, description, completed)
            VALUES
            ({table_data_len + 1}, '{title}', '{description}', '{completed}');
        ''')
        self.connection.commit()

    def update_todo(self, todo_id, title, description, completed):
        self.cursor.execute(f'''
            UPDATE {self.table}
            SET title = '{title}', description = '{description}', completed = '{completed}'
            WHERE id = {todo_id};
        ''')
        self.connection.commit()

    def delete_todo(self, todo_id):
        self.cursor.execute(f'''
            DELETE FROM {self.table}
            WHERE id = {todo_id}
        ''')
        self.connection.commit()
