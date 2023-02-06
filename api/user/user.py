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
                       "message": "해당 유저가 존재하지 않음"
                   }, 400

        elif result[1] != password:
            database.close()
            return {
                       "message": "아이디나 비밀번호가 일치하지 않음"
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
                       "message": "이미 있는 유저"
                   }, 400

        cursor.execute(f"INSERT INTO user VALUES('{id}', '{password}', '{nickname}');")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "유저 생성 성공"
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
                       "message": "아이디나 비밀번호 불일치"
                   }, 400
        if result[2] == nickname:
            database.close()
            return {
                       "is_success": False,
                       "message": "현재 닉네임과 같음"
                   }, 400

        cursor.execute(f"UPDATE user SET nickname = '{nickname}' WHERE id = '{id}' and pw = '{password}';")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "유저 닉네임 변경 성공"
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
                       "message": "아이디나 비밀번호 불일치"
                   }, 400

        cursor.execute(f"DELETE FROM user WHERE id = '{id}' and pw = '{password}';")
        database.commit()
        database.close()
        return {
                   "is_success": True,
                   "message": "유저 삭제 성공"
               }, 200
