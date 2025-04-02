import duckdb
import pandas as pd
import os

def create_tables(database_path='my.db', tables_sql_path='queries/create_tables.sql'):
    """
    Функция для создания таблиц в базе данных DuckDB.

    Она подключается к базе данных, считывает SQL-скрипт для создания таблиц из файла и выполняет его.

    Параметры:
    database_path (str): Путь к базе данных.
    tables_sql_path (str): Путь к SQL файлу с командой создания таблиц.
    """
    con = duckdb.connect(database=database_path)

    with open(tables_sql_path, 'r') as f:
        create_tables_sql = f.read()

    con.execute(create_tables_sql)
    con.close()
    print("Таблицы успешно созданы.")

def load_data(database_path='my.db', source_folder='source'):
    """
    Функция для загрузки данных в базу данных DuckDB.

    Данные загружаются из CSV файлов в DataFrame и затем вставляются в соответствующие таблицы базы данных.
    Для таблицы 'screenings' происходит дополнительная обработка данных (форматирование даты и времени,
    фильтрация по корректным theater_id).

    Параметры:
    database_path (str): Путь к базе данных.
    source_folder (str): Папка, где хранятся исходные CSV файлы.
    """
    con = duckdb.connect(database=database_path)
    
    data_files = {
        'genres': 'genres.csv',
        'movies': 'movies.csv',
        'theaters': 'theaters.csv',
        'screenings': 'screenings.csv',
    }

    for table_name, file_name in data_files.items():
        file_path = os.path.join(source_folder, file_name)
        df = pd.read_csv(file_path)

        if table_name == 'screenings':
            df['screening_date'] = pd.to_datetime(df['screening_date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
            df['screening_time'] = pd.to_datetime(df['screening_time'], format='%H:%M').dt.strftime('%H:%M')

            valid_theater_ids = con.execute("SELECT theater_id FROM theaters").fetchall()
            valid_theater_ids = {row[0] for row in valid_theater_ids}
            df = df[df['theater_id'].isin(valid_theater_ids)]  

        con.register('df', df)
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        print(f"Данные загружены в таблицу '{table_name}' из файла '{file_name}'.")

    con.close()

def create_views(database_path='my.db', views_sql_path='queries/create_views.sql'):
    """
    Функция для создания представлений (views) в базе данных DuckDB.

    Она подключается к базе данных и выполняет SQL-скрипт для создания представлений.

    Параметры:
    database_path (str): Путь к базе данных.
    views_sql_path (str): Путь к SQL файлу с командой создания представлений.
    """

    con = duckdb.connect(database=database_path)

    with open(views_sql_path, 'r') as f:
        create_views_sql = f.read()

    con.execute(create_views_sql)
    con.close()
    print("Представления успешно созданы.")


if __name__ == '__main__':
    create_tables()
    load_data()
    create_views()
