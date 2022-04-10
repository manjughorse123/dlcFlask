from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_mysqldb import MySQL, MySQLdb
from flask_restful import Api, Resource, reqparse
from app_dlc import mysql
import re
import urllib.parse

# Blueprint Configuration
auth = Blueprint('dlc_api', __name__)

# RESTful API
class api_dlc(Resource):
    def get(self):
        # Write method to fetch data
        return {'message' : 'Not yet implemented. Get successfully.'}, 200

    def post(self):
        # Write method to write data
        parser = reqparse.RequestParser()
        parser.add_argument('rfid', required=True)
        parser.add_argument('date', required=True)
        parser.add_argument('time', required=True)
        parser.add_argument('device_id', required=True)
        args = parser.parse_args()

        print(f"RFID:   {args['rfid']}")
        print(f"Date:   {args['date']}")
        print(f"Time:   {args['time']}")
        print(f"Device: {args['device_id']}")

        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql_sp = (f"CALL `sp_insert_driving_licenses_checks`"
                      f"('{args['date']} {args['time']}', '{args['rfid']}', '{args['device_id']}', "
                      f"@driver_id, @driver_lastname, @driver_firstname, @driver_interval, @ret);")
            sql_select = "SELECT @ret, @driver_id, @driver_lastname, @driver_firstname, @driver_interval;"
            result = cur.execute(sql_sp)
            result = cur.execute(sql_select)
            rows = cur.fetchall()
            mysql.connection.commit()
            print(rows[0])
            return {'row': rows[0]}, 201
        except Exception as e:
            return {'exception': str(e)}, 400
