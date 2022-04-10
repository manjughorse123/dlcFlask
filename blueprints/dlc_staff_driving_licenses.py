from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mysqldb import MySQL, MySQLdb
from app_dlc import mysql
import re
import urllib.parse

dlc_staff_driving_licenses = Blueprint('dlc_staff_driving_licenses', __name__, url_prefix="/staff_driving_licenses")


# @dlc_staff_driving_licenses.route('/')
# @login_required
# def select_staff_driving_licenses():
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     result = cur.execute("SELECT * FROM staff")
#     select_staff = cur.fetchall()
#     cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     result = cur1.execute("SELECT * FROM driving_licenses")
#     select_driving_licenses = cur1.fetchall()
#
#     return render_template('dlc_md_staff_driving_licenses_bs.html', staff=select_staff)

@dlc_staff_driving_licenses.route('/')
@login_required
def select_staff_driving_licenses():
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # result = cur.execute("SELECT * FROM staff")
    # select_staff = cur.fetchall()
    cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur1.execute("SELECT * FROM driving_licenses")
    select_driving_licenses = cur1.fetchall()

    return render_template('dlc_md_staff_driving_licenses_bs.html', staff_li=select_driving_licenses)


@dlc_staff_driving_licenses.route('/select_driving_licenses', methods=['GET', 'POST'])
@login_required
def select_driving_licenses():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        staff_id = request.form.get('staff_id')
        result = cur.execute('SELECT * FROM driving_licenses WHERE staff_id = {0}'.format(staff_id))
        select_driving_licenses = cur.fetchall()
        render_template('dlc_md_staff_driving_licenses_bs.html', staff_licencec=select_driving_licenses)
        # return jsonify(select_driving_licenses)
    except:
        return jsonify({"status": "ok"})


@dlc_staff_driving_licenses.route('/create_driving_licenses', methods=['POST', 'GET'])
@login_required
def create_driving_licenses():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qs(my_json)
    res_data = {}

    for lable_k, value_v in res.items():
        res_data[lable_k[8:-1]] = value_v[0]

    if request.method == 'POST':
        txtstaff_id = res_data['staff_id']
        try:
            txtlicense_nr = res_data['license_nr']
        except:
            txtlicense_nr = 'None'
        try:
            txtrfid = res_data['rfid']
        except:
            txtrfid = 'None'
        try:
            txtcheck_interval = res_data['check_interval']
        except:
            txtcheck_interval = 0
        try:
            txtauthority = res_data['authority']
        except:
            txtauthority = 'None'
        try:
            txtdate_issue = res_data['date_issue']
        except:
            txtdate_issue = 'None'
        try:
            txtdate_valid = res_data['date_valid']
        except:
            txtdate_valid = 'None'
        try:
            txtenlisted = res_data['enlisted']
        except:
            txtenlisted = 0
        else:
            result = cur.execute(
                "INSERT INTO driving_licenses (staff_id,license_nr,rfid,check_interval,authority,date_issue,date_valid,enlisted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                [txtstaff_id, txtlicense_nr, txtrfid, txtcheck_interval, txtauthority, txtdate_issue,
                 txtdate_valid, txtenlisted])
            mysql.connection.commit()
            cur.close()
            msg = 'New record created successfully'

    return json.dumps({'status': 'ok'})


@dlc_staff_driving_licenses.route('/update_driving_licenses', methods=["POST", "GET"])
@login_required
def update_driving_licenses():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)
    print(res)

    if request.method == 'POST':
        string = res[0][1]
        txtuuid = res[1][1]
        txtstaff_id = res[2][1]
        txtlicense_nr = res[3][1]
        txtrfid = res[4][1]
        txtcheck_interval = res[5][1]
        txtauthority = res[6][1]
        txtdate_issue = res[7][1]
        txtdate_valid = res[8][1]
        txtenlisted = res[9][1]
        txtlast_user_id = res[10][1]
        txtlast_access = res[11][1]
        cur.execute(
            "UPDATE staff SET uuid =%s ,staff_id = %s, license_nr = %s,rfid = %s,check_interval = %s,authority = %s,date_issue = %s,date_valid = %s,enlisted = %s,last_user_id=%s,last_access=%s WHERE id = %s ",
            [txtuuid, txtstaff_id, txtlicense_nr, txtrfid, txtcheck_interval, txtauthority, txtdate_issue,
             txtdate_valid, txtenlisted, txtlast_user_id, txtlast_access, string])
        mysql.connection.commit()
        cur.close()
        msg = 'Record successfully Updated'

    return json.dumps({'status': 'ok'})


@dlc_staff_driving_licenses.route('/delete_driving_licenses', methods=["POST", "GET"])
@login_required
def delete_driving_licenses():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_bytes_value = request.get_data()
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    res = urllib.parse.parse_qsl(my_json)
    print(my_bytes_value)

    if request.method == 'POST':
        getid = res[0][1]
        cur.execute('DELETE FROM driving_licenses WHERE id = {0}'.format(getid))
        mysql.connection.commit()
        cur.close()
        msg = 'Record deleted successfully'

    return json.dumps({'status': 'ok'})
