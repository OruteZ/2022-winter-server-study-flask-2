import configparser
import pymysql

from flask import request
from flask_restx import Resource, Namespace

user = Namespace('user')

# config 파일 접근
config = configparser.ConfigParser()
config.read("config/config.ini")


def connect():
    # config 정보를 이용해서 mysql database 접근
    database = pymysql.connect(
        host=config['DATABASE']['HOST'],
        user=config['DATABASE']['USER'],
        passwd=config['DATABASE']['PASSWORD'],
        db=config['DATABASE']['DB'],
        port=int(config['DATABASE']['PORT']),
        charset=config['DATABASE']['CHARSET']
    )
    return database


@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        database = connect()
        cursor = database.cursor()

        id = request.args.get("id")
        password = request.args.get("password")

        cnt = cursor.execute(f"SELECT * FROM user WHERE id = '{id}'")
        result = cursor.fetchone()

        if cnt == 0:
            database.close()
            return {
                       "message": "User Not Found"
                   }, 400

        elif result[1] != password:
            database.close()
            return {
                       "message": "Password incorrect"
                   }, 400

        else:
            database.close()
            return {
                       "nickname": result[2]
                   }, 200

    def post(self):
        # POST method 구현 부분
        database = connect()
        cursor = database.cursor()

        req = request.json
        id = req["id"]
        password = req["password"]
        nickname = req["nickname"]

        cnt = cursor.execute(f"SELECT * FROM user WHERE id = '{id}';")
        if cnt > 0:
            database.close()
            return {
                       "is_success": False,
                       "message": "User already exist"
                   }, 400

        cursor.execute(f"INSERT INTO user VALUES('{id}', '{password}', '{nickname}');")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "creating user success"
               }, 200

    def put(self):
        # PUT method 구현 부분
        database = connect()
        cursor = database.cursor()

        id = request.json["id"]
        password = request.json["password"]
        nickname = request.json["nickname"]

        cnt = cursor.execute(f"SELECT * FROM user WHERE id = '{id}' and pw = '{password}';")
        result = cursor.fetchone()
        if cnt == 0:
            database.close()
            return {
                       "is_success": False,
                       "message": "ID or PW incorrect"
                   }, 400
        if result[2] == nickname:
            database.close()
            return {
                       "is_success": False,
                       "message": "Nickname is not changed"
                   }, 400

        cursor.execute(f"UPDATE user SET nickname = '{nickname}' WHERE id = '{id}' and pw = '{password}';")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "Successful change"
               }, 200

    def delete(self):
        # DELETE method 구현 부분
        database = connect()
        cursor = database.cursor()

        id = request.json['id']
        password = request.json['password']

        cnt = cursor.execute(f"SELECT * FROM user WHERE id = '{id}' and pw = '{password}';")
        if cnt == 0:
            database.close()
            return {
                       "is_success": False,
                       "message": "ID or PW incorrect"
                   }, 400

        cursor.execute(f"DELETE FROM user WHERE id = '{id}' and pw = '{password}';")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "Deleted User successful"
               }, 200
