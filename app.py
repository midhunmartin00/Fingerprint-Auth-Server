import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib.parse

MOD_SIZE = 256
table_name = "fingertable"
FEATURE_COLS = 640

engine = create_engine('sqlite:///./cloud.db', echo = True)


app = Flask(__name__)


@app.route('/validate', methods=['POST'])
def validate():
    user_roll_num = request.get_json()['encr_regno']
    user_roll_num = urllib.parse.quote(user_roll_num)
    result = engine.execute('SELECT * FROM %s WHERE enc_roll = "%s"' % (table_name, user_roll_num))
    row = result.first()
    if not row:
        return "Invalid Roll Number", 404
    
    
    details = dict(row.items())
    response = {}
    response['encr_fp_list'] = list()
    for col_name,value in details.items():
        if col_name== 'enc_roll':
            response['encr_regno'] = urllib.parse.unquote(value)
        elif col_name =='enc_sum_of_sqr':
            response['encr_fp_sqr'] = urllib.parse.unquote(value)
        else:
            ## Then it must be part of feature vector
            response['encr_fp_list'].append(urllib.parse.unquote(value))
            
    return jsonify(response)


@app.route('/enroll', methods=['POST'])
def enroll():
    body = request.get_json()
    enc_user_roll_num = urllib.parse.quote(body['encr_regno'])
    enc_features = body['encr_fp_list']
    enc_sum_of_sqr = urllib.parse.quote(body['encr_fp_sqr'])

    if len(enc_features)!=640:
        return "Feature count wrong", 400

    insert_query = 'INSERT INTO %s VALUES ("%s", "%s"' % (table_name, enc_user_roll_num, enc_sum_of_sqr)
    for feature in enc_features:
        insert_query+= ', "' + urllib.parse.quote(feature) + '"'
    insert_query += ')'

    result = engine.execute(insert_query)
    return "Success",200




if __name__ == '__main__':
    app.run(host="0.0.0.0")
