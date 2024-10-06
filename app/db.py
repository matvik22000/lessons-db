import hashlib
import os.path
from contextlib import contextmanager
from os import walk

import mariadb

from environ import *

default_conf = dict(
    user=get_db_user(),
    password=get_db_password(),
    host=get_db_host(),
    port=get_db_port(),
    database=get_default_db_name(),
    autocommit=True
)


def _check_conf():
    if not all((default_conf['password'],)):
        raise Exception(f"Bad config: {default_conf}")


_check_conf()


@contextmanager
def as_user(username=None, pwd=None, db=None):
    conf = default_conf.copy()
    if username and pwd:
        conf['user'] = username
        conf['password'] = pwd
    if db:
        conf['database'] = db
    with mariadb.connect(
            **conf
    ) as conn:
        yield conn


def _execute_from_path(cur, path: str):
    with open(path, encoding='utf-8') as script:
        for cmd in script.read().split(";"):
            cur.execute(cmd)


def collect_tables():
    path = get_db_scripts_dir()
    files = next(walk(path), (None, None, []))[2]

    def parse_table_name(name: str):
        table_name = name.split('_')[1].removesuffix('.sql')
        return table_name, os.path.join(path, name)

    return tuple(sorted(map(parse_table_name,
                            filter(lambda name: name.startswith('init_'), files))))


def recreate_table(username, password, table_name: str):
    filename = f'init_{table_name}.sql'
    path = os.path.join(get_db_scripts_dir(), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'{path} {filename}')
    with as_user(username, password, get_db_name(username)) as conn:
        _execute_from_path(conn.cursor(), path)


def init_tables(username: str, password: str):
    tables = collect_tables()
    print(f"creating {len(tables)} for user {username}:{password}")
    with as_user(username, password, get_db_name(username)) as conn:
        for _, path in tables:
            _execute_from_path(conn.cursor(), path)


def create_user(username: str, password: str):
    with as_user() as conn:
        cur = conn.cursor()
        cur.execute("""call add_user(%s, %s)""", (username, password))
        cur.execute("""insert into users (username, pwd) values (%s, %s)""",
                    (username, hashlib.md5(password.encode()).hexdigest())
                    )
    init_tables(username, password)


def check_password(username: str, password: str):
    with as_user() as conn:
        cur = conn.cursor()
        cur.execute("""select count(*) from users where username = %s and pwd = %s""", (
            (username, hashlib.md5(password.encode()).hexdigest())
        ))
        res = cur.fetchall()
        return res[0][0] != 0


def get_users():
    with as_user() as conn:
        cur = conn.cursor()
        cur.execute("""select user from mysql.user""")
        return tuple(map(lambda el: el[0], cur.fetchall()))


def check_user_exists(username: str):
    return username in get_users()


def get_db_name(username: str):
    return username + "_db"


if __name__ == '__main__':
    print(collect_tables())
