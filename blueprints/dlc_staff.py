from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mysqldb import MySQL, MySQLdb
from app_dlc import mysql
import re
import urllib.parse

dlc_staff = Blueprint('dlc_staff', __name__, url_prefix="/staff")


@dlc_staff.route('/')
@login_required
def select_staff():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM staff")
    select_staff = cur.fetchall()
    cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur1.execute("SELECT * FROM driving_licenses")
    select_driving_licenses = cur1.fetchall()
    return render_template('dlc_md_staff_bs.html', staff=select_staff)


import uuid


@dlc_staff.route('/create_staff', methods=['POST', 'GET'])
@login_required
def create_staff():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qs(my_json)
    res_data = {}
    # print(res)
    print(my_bytes_value)
    txtuuid = uuid.uuid4()
    for lable_k, value_v in res.items():
        res_data[lable_k[21:-1]] = value_v[0]

    if request.method == 'POST':
        txtfirstname = res_data['first_name']
        txtlastname = res_data['last_name']
        txtemail = res_data['email']
        try:
            txtaddress = res_data['address']
        except:
            txtaddress = 'None'
        try:
            txtzipcode = res_data['zip_code']
        except:
            txtzipcode = 'None'
        try:
            txtcity = res_data['city']
        except:
            txtcity = 'None'
        try:
            txtcountry = res_data['country']
        except:
            txtcountry = 'None'
        try:
            txtphone = res_data['phone']
        except:
            txtphone = 'None'
        try:
            txtdateentry = res_data['date_entry']
        except:
            txtdateentry = 'None'
        try:
            txtdateexit = res_data['date_exit']
        except:
            txtdateexit = 'None'

        if txtfirstname == '':
            msg = 'Please Input first name'
        elif txtlastname == '':
            msg = 'Please Input last name'
        elif txtemail == '':
            msg = 'Please Input email'
        else:
            result = cur.execute(
                "INSERT INTO staff (uuid,first_name,last_name,email,address,zip_code,city,country,"
                "phone,date_entry,date_exit) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [txtuuid, txtfirstname, txtlastname, txtemail, txtaddress, txtzipcode, txtcity, txtcountry, txtphone,
                 txtdateentry, txtdateexit])
            mysql.connection.commit()
            cur.close()
            msg = 'New record created successfully'
            data = {'first_name': txtfirstname, 'last_name': txtlastname, 'email': txtemail}

    return json.dumps({'status': 'ok', 'response': data})


@dlc_staff.route('/update_staff', methods=["POST", "GET"])
@login_required
def update_staff():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        data_uuid = re.findall('uuid', res[0][0], flags=0)
        data_first_name = re.findall('first_name', res[0][0], flags=0)
        data_last_name = re.findall('last_name', res[0][0], flags=0)
        data_email = re.findall('email', res[0][0], flags=0)
        data_address = re.findall('address', res[0][0], flags=0)
        data_zip_code = re.findall('zip_code', res[0][0], flags=0)
        data_city = re.findall('city', res[0][0], flags=0)
        data_country = re.findall('country', res[0][0], flags=0)
        data_phone = re.findall('phone', res[0][0], flags=0)
        data_date_entry = re.findall('date_entry', res[0][0], flags=0)
        data_date_exit = re.findall('date_exit', res[0][0], flags=0)
        data3 = re.findall(r'\d+', res[0][0])
        string = data3[0]
        if data_uuid == ['uuid']:
            txtuuid = res[0][1]
            cur.execute(
                "UPDATE staff SET uuid = %s  WHERE id = %s ",
                (txtuuid, string))
        elif data_first_name == ['first_name']:
            txtfirstname = res[0][1]
            cur.execute(
                "UPDATE staff SET first_name = %s  WHERE id = %s ",
                (txtfirstname, string))
        elif data_last_name == ['last_name']:
            txtlastname = res[0][1]
            cur.execute(
                "UPDATE staff SET last_name = %s  WHERE id = %s ",
                (txtlastname, string))
        elif data_email == ['email']:
            txtemail = res[0][1]
            cur.execute(
                "UPDATE staff SET email = %s  WHERE id = %s ",
                (txtemail, string))
        elif data_zip_code == ['zip_code']:
            txtzipcode = res[0][1]
            cur.execute(
                "UPDATE staff SET zip_code = %s  WHERE id = %s ",
                (txtzipcode, string))
        elif data_address == ['address']:
            txtaddress = res[0][1]
            cur.execute(
                "UPDATE staff SET address = %s  WHERE id = %s ",
                (txtaddress, string))
        elif data_city == ['city']:
            txtcity = res[0][1]
            cur.execute(
                "UPDATE staff SET city = %s  WHERE id = %s ",
                (txtcity, string))
        elif data_country == ['country']:
            txtcountry = res[0][1]
            cur.execute(
                "UPDATE staff SET country = %s  WHERE id = %s ",
                (txtcountry, string))
        elif data_phone == ['phone']:
            txtphone = res[0][1]
            cur.execute(
                "UPDATE staff SET phone = %s  WHERE id = %s ",
                (txtphone, string))
        elif data_date_entry == ['date_entry']:
            txtdateentry = res[0][1]
            cur.execute(
                "UPDATE staff SET date_entry = NULLIF(%s,'None')  WHERE id = %s ",
                (txtdateentry, string))
        elif data_date_exit == ['date_exit']:
            txtdateexit = res[0][1]
            cur.execute(
                "UPDATE staff SET date_exit = NULLIF(%s,'None')  WHERE id = %s ",
                (txtdateexit, string))
        else:
            string = res[0][1]
            txtuuid = res[1][1]
            txtfirstname = res[2][1]
            txtlastname = res[3][1]
            txtemail = res[4][1]
            txtaddress = res[5][1]
            txtzipcode = res[6][1]
            txtcity = res[7][1]
            txtcountry = res[8][1]
            txtphone = res[9][1]
            txtdateentry = res[10][1]
            txtdateexit = res[11][1]
            cur.execute(
                "UPDATE staff SET uuid =%s ,first_name = %s, last_name = %s, email = %s,address = %s,zip_code = %s,"
                "city = %s,country = %s,phone = %s,"
                "date_entry = NULLIF(%s,'None'),date_exit = NULLIF(%s,'None') WHERE id = %s ",
                [txtuuid, txtfirstname, txtlastname, txtemail, txtaddress, txtzipcode, txtcity,
                 txtcountry, txtphone, txtdateentry, txtdateexit, string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record successfully Updated'

    return json.dumps({'status': 'ok'})


@dlc_staff.route('/delete_staff', methods=["POST", "GET"])
@login_required
def delete_staff():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        getid = res[0][1]
        cur.execute('DELETE FROM staff WHERE id = {0}'.format(getid))
        mysql.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'

    return json.dumps({'status': 'ok'})
