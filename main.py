from src.postgres_db import PostgresDB
from src.functions import *
from src.config import config

github_user = "skypro-008"
params = config()
db_name = "repos_stats"

if __name__ == '__main__':
    list_ = get_repos_stats(github_user)

    create_database(db_name, params)
    print("БД создана")

    params.update({"dbname": db_name})
    database = PostgresDB(params)
    database.insert_data(list_)
    print("Таблицы созданы")

    data = database.get_data()
    print("Данные из БД получены")

    database.export_to_json(data)
    print("Экспорт успешно выполнен")

    database.close_connection()
    print("Закрытие соединения с БД")