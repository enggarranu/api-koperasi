import hashlib
from flask import request, abort, json
import connection
from koperasi_main import *

def login_petugas():
    try:
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            username = data['username']
            password = data['password']
            print (data)
            if (data['signature'] != hashlib.md5(username+password).hexdigest()):
                res_data['response'] = 'NOK'
                res_data['msg'] = 'Invalid Signature!'
                print(data['signature'])
                print(hashlib.md5(username+password).hexdigest())
                return json.dumps(res_data)

            koperasi.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = ("SELECT fullname, username, jenis_role FROM `tb_ms_login` where username = '"+username+"' and password = '"+password+"';")
            koperasi.logger.info(q_is_exist)
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            if len(rs) < 1:
                res_data['response'] = 'NOK'
                res_data['msg'] = 'Username atau password salah, Mohon cek kembali!!!'
                return json.dumps(res_data)

            fullname = rs[0][0]
            username = rs[0][1]
            jenis_role = rs[0][2]
            if (fullname != None or username != None) :
                res_data['response'] = 'OK'
                res_data['msg'] = 'Success Login!!'
                res_data['fullname'] = fullname
                res_data['jenis_role'] =jenis_role
                koperasi.logger.info(res_data)
                return json.dumps(res_data)

    except Exception as e:
        res_data = {}
        koperasi.logger.error('An error occured.')
        koperasi.logger.error(e)
        res_data['ACK'] = 'NOK'
        res_data['msg'] = str(e)
        return json.dumps(res_data)