import os
from typing import Callable

REQUIRED = []
OPTIONAL = []


def optional(var, default=None, tp: Callable = str):
    OPTIONAL.append(var)
    return lambda: tp(os.environ.get(var) or default)


def required(var, tp=str):
    REQUIRED.append(var)
    return lambda: tp(os.environ.get(var))


get_db_password = required('DB_PASSWORD')
get_db_host = required('DB_HOST')
get_external_db_host = required('EXTERNAL_DB_HOST')
get_default_db_name = optional('DB_NAME', 'lesson')
get_db_port = optional('DB_PORT', 3306, tp=int)
get_db_user = optional('DB_USER', 'root')
get_db_scripts_dir = optional('DB_SCRIPTS_FOLDER', 'scripts')

not_presented = []
for var in REQUIRED:
    if var not in os.environ:
        not_presented.append(var)

if not_presented:
    raise Exception(f'In environ not presented required values: {not_presented}')
