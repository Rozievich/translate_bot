import os
import psycopg2

con = psycopg2.connect(
    user='postgres',
    database='postgres',
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cur = con.cursor()


def create_table():
    query_user = '''
    CREATE TABLE IF NOT EXISTS users(
        id serial primary key,
        user_id varchar(80) not null,
        name varchar(100) not null,
        username varchar(50),
        time timestamp default now()
    )
    '''
    query_admin = '''
    CREATE TABLE IF NOT EXISTS admins(
        id serial primary key,
        user_id varchar(80) not null,
        time timestamp default now()
    )
    '''
    cur.execute(query_user)
    cur.execute(query_admin)
    con.commit()
