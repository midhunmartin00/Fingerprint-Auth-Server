from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from string import ascii_lowercase
from random import choice



MOD_SIZE = 256
table_name = "fingertable"
FEATURE_COLS = 640

engine = create_engine('sqlite:///./cloud.db')


NUM = 4


def get_random_string():
    return ''.join(choice(ascii_lowercase) for i in range(MOD_SIZE))

for i in range(NUM):
    enc_user_roll_num = get_random_string()
    enc_sum_of_sqr = get_random_string()
    insert_query = 'INSERT INTO %s VALUES ("%s", "%s"' % (table_name, enc_user_roll_num, enc_sum_of_sqr)
    enc_features = [get_random_string() for i in range(FEATURE_COLS)]
    for feature in enc_features:
        insert_query+= ', "' + feature + '"'
    insert_query += ')'
    result = engine.execute(insert_query)
