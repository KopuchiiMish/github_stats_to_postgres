import psycopg2
import requests


def get_repos_stats(user):
    response = requests.get(f"https://api.github.com/users/{user}/repos").json()
    the_list = [{'id': repo['id'],
                 'name': repo['name'],
                 'size': repo['size'],
                 'forks_count': repo['forks_count'],
                 'url': repo['html_url'],
                 'created_at': repo['created_at']}
                for repo in response]
    return the_list


def create_database(db_name, params):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(dbname='postgres', **params)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
    finally:
        cursor.close()
        connection.close()