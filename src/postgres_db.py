import json

import psycopg2


class PostgresDB:
    def __init__(self, params):
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert_data(self, data):
        query = '''DROP TABLE IF EXISTS repositories; 
                   CREATE TABLE repositories 
                   (
                       id int PRIMARY KEY,
                       name varchar(100) NOT NULL,
                       size int,
                       forks_count int,
                       url text,
                       created_at date NOT NULL
                   )
                '''
        self.cur.execute(query)
        for repo in data:
            self.cur.execute('''INSERT INTO repositories(id, name, size, forks_count, url, created_at)
                                VALUES (%s, %s, %s, %s, %s, %s)''',
                             (repo['id'], repo['name'], repo['size'],
                              repo['forks_count'], repo['url'], repo['created_at']))

    @staticmethod
    def export_to_json(data):
        the_list = [{'id': repo[0],
                     'name': repo[1],
                     'size': repo[2],
                     'forks_count': repo[3],
                     'url': repo[4],
                     'created_at': str(repo[5])}
                    for repo in data]
        with open('repositories.json', 'w') as f:
            f.write(json.dumps(the_list, indent=2, ensure_ascii=False))

    def get_data(self):
        self.cur.execute('SELECT * FROM repositories')
        data = self.cur.fetchall()
        return data

    def close_connection(self):
        self.cur.close()
        self.conn.close()