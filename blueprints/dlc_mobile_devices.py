from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mysqldb import MySQL, MySQLdb
from app_dlc import mysql
import re
import urllib.parse

dlc_mobile_devices = Blueprint('dlc_mobile_devices', __name__, url_prefix="/mobile_devices")


@dlc_mobile_devices.route('/')
@login_required
def select_mobile_devices():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM mobile_devices")
    select_mobile_devices = cur.fetchall()

    return render_template('dlc_mobile_devices_bs.html', staff=select_mobile_devices)

@dlc_mobile_devices.route('/create_mobile_device', methods=['POST', 'GET'])
@login_required
def create_mobile_device():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qs(my_json)
    res_data = {}

    for lable_k, value_v in res.items():
        res_data[lable_k[8:-1]] = value_v[0]

    if request.method == 'POST':
        #txtuuid = res_data['uuid']
        txtdeviceid = res_data['device_id']
        try:
            txtdescription = res_data['description']
        except:
            txtdescription = 'None'
        try:
            txtserial = res_data['serial']
        except:
            txtserial = 'None'
        try:
            txtactivationcode = res_data['activation_code']
        except:
            txtactivationcode = 'None'

        if txtdeviceid == '':
            msg = 'Please input Device ID'
        else:
            result = cur.execute(
                "INSERT INTO mobile_devices (device_id,description,serial,activation_code) VALUES (%s,%s,%s,%s)",
                [txtdeviceid, txtdescription, txtserial, txtactivationcode])
            mysql.connection.commit()
            cur.close()
            msg = 'New record created successfully'
            data = {'device_id': txtdeviceid}

    return json.dumps({'status': 'ok', 'response': data})


@dlc_mobile_devices.route('/update_mobile_device', methods=["POST", "GET"])
@login_required
def update_mobile_device():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        data_uuid = re.findall('uuid', res[0][0], flags=0)
        data_device_id = re.findall('device_id', res[0][0], flags=0)
        data_description = re.findall('description', res[0][0], flags=0)
        data_serial = re.findall('serial', res[0][0], flags=0)
        data_activation_code = re.findall('activation_code', res[0][0], flags=0)
        data3 = re.findall(r'\d+', res[0][0])
        string = data3[0]
        if data_uuid == ['uuid']:
            txtuuid = res[0][1]
            cur.execute(
                "UPDATE mobile_devices SET uuid = %s  WHERE id = %s ",
                (txtuuid, string))
        elif data_device_id == ['device_id']:
            txtdeviceid = res[0][1]
            cur.execute(
                "UPDATE mobile_devices SET device_id = %s  WHERE id = %s ",
                (txtdeviceid, string))
        elif data_description == ['description']:
            txtdescription = res[0][1]
            cur.execute(
                "UPDATE mobile_devices SET description = %s  WHERE id = %s ",
                (txtdescription, string))
        elif data_serial == ['serial']:
            txtserial = res[0][1]
            cur.execute(
                "UPDATE mobile_devices SET serial = %s  WHERE id = %s ",
                (txtserial, string))
        elif data_activation_code == ['activation_code']:
            txtactivationcode = res[0][1]
            cur.execute(
                "UPDATE mobile_devices SET activation_code = %s  WHERE id = %s ",
                (txtactivationcode, string))
        else:
            string = res[0][1]
            txtuuid = res[1][1]
            txtdeviceid = res[2][1]
            txtdescription = res[3][1]
            txtserial = res[4][1]
            txtactivationcode = res[5][1]
            cur.execute(
                "UPDATE mobile_devices SET uuid =%s ,device_id = %s, description = %s, serial = %s, activation_code = %s WHERE id = %s ",
                [txtuuid, txtdeviceid, txtdescription, txtserial, txtactivationcode,
                 string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record updated successfully'

    return json.dumps({'status': 'ok'})


@dlc_mobile_devices.route('/delete_mobile_device', methods=["POST", "GET"])
@login_required
def delete_mobile_device():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)

    if request.method == 'POST':
        getid = res[0][1]
        cur.execute('DELETE FROM mobile_devices WHERE id = {0}'.format(getid))
        mysql.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'

    return json.dumps({'status': 'ok'})
