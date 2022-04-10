from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.security import generate_password_hash
from app_dlc import mysql
import re
import urllib.parse

dlc_user_logins = Blueprint('dlc_user_logins', __name__, url_prefix="/user_logins")


@dlc_user_logins.route('/')
@login_required
def select_user_logins():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM user_logins")
    select_user_logins = cur.fetchall()

    return render_template('dlc_user_logins_bs.html', staff=select_user_logins)

@dlc_user_logins.route('/create_user_login', methods=['POST', 'GET'])
@login_required
def create_user_login():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qs(my_json)
    res_data = {}

    for lable_k, value_v in res.items():
        res_data[lable_k[8:-1]] = value_v[0]

    if request.method == 'POST':
        txtname = res_data['name']
        txtemail = res_data['email']
        txtpassword = res_data['password']
        txtpassword_hash = generate_password_hash(txtpassword)
        try:
            txtstaffid = res_data['staff_id']
        except:
            txtstaffid = 'None'

        if txtname == '':
            msg = 'Please input Name'
        elif txtemail == '':
            msg = 'Please input Email'
        elif txtpassword == '':
            msg = 'Please input Password'
        else:
            result = cur.execute(
                "INSERT INTO user_logins (name,email,password,staff_id) VALUES (%s,%s,%s,NULLIF(%s,'None'))",
                [txtname, txtemail, txtpassword_hash, txtstaffid])
            mysql.connection.commit()
            cur.close()
            msg = 'New record created successfully'
            data = {'name': txtname}

    return json.dumps({'status': 'ok', 'response': data})


@dlc_user_logins.route('/update_user_login', methods=["POST", "GET"])
@login_required
def update_user_login():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        data_name = re.findall('name', res[0][0], flags=0)
        data_email = re.findall('email', res[0][0], flags=0)
        data_password = re.findall('password', res[0][0], flags=0)
        data_staff_id = re.findall('staff_id', res[0][0], flags=0)
        data3 = re.findall(r'\d+', res[0][0])
        string = data3[0]
        if data_name == ['name']:
            txtname = res[0][1]
            cur.execute(
                "UPDATE user_logins SET name = %s  WHERE id = %s ",
                (txtname, string))
        elif data_email == ['email']:
            txtemail = res[0][1]
            cur.execute(
                "UPDATE user_logins SET email = %s  WHERE id = %s ",
                (txtemail, string))
        elif data_password == ['password']:
            txtpassword = res[0][1]
            txtpassword_hash = generate_password_hash(txtpassword)
            cur.execute(
                "UPDATE user_logins SET password = %s  WHERE id = %s ",
                (txtpassword_hash, string))
        elif data_staff_id == ['staff_id']:
            txtstaffId = res[0][1]
            cur.execute(
                "UPDATE user_logins SET staff_id = NULLIF(%s,'None')  WHERE id = %s ",
                (txtstaffId, string))
        else:
            string = res[0][1]
            txtname = res[1][1]
            txtemail = res[2][1]
            txtpassword = res[3][1]
            txtpassword_hash = generate_password_hash(txtpassword)
            txtstaffId = res[4][1]
            cur.execute(
                "UPDATE user_logins SET name =%s ,email = %s, password = %s, staff_id = NULLIF(%s,'None') WHERE id = %s ",
                [txtname, txtemail, txtpassword_hash, txtstaffId, string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record updated successfully'

    return json.dumps({'status': 'ok'})


@dlc_user_logins.route('/delete_user_login', methods=["POST", "GET"])
@login_required
def delete_user_login():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        getid = res[0][1]
        cur.execute('DELETE FROM user_logins WHERE id = {0}'.format(getid))
        mysql.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'

    return json.dumps({'status': 'ok'})
