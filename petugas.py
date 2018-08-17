from flask import request, abort, json
from koperasi_main import *
import connection

def register_petugas_get_id():
    res_data = {}
    if request.method == 'GET':
        db = connection.get_db()
        curr = db.cursor()
        q_is_exist = (
            "SELECT id+1 FROM `tb_ms_login` ORDER BY id DESC limit 1;")
        curr.execute(q_is_exist)
        rs = curr.fetchall()
        jumlah_row = rs[0][0]
        res_data['response'] = 'OK'
        res_data['msg'] = "PG" + str(jumlah_row)
        db.close()
        return json.dumps(res_data)

def register():
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
            fullname = data['fullname']
            email = data['email']
            address = data['address']
            jenis_role = data['jenis_role']
            registered_by = data['registered_by']
            id_petugas = data['id_petugas']

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = ("SELECT count(id) as jumlah FROM `tb_ms_login` where username = '"+username+"' or email = '"+email+"';")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            if jumlah_row > 0 :
                res_data['response'] = 'NOK'
                res_data['msg'] = 'User Already Registered'
                return json.dumps(res_data)

            q_insert = ("INSERT INTO `tb_ms_login` (username, password, fullname, email, address, jenis_role, registered_by, id_petugas) values ('"+username+"','"+password+"','"+fullname+"','"+email+"','"+address+"','"+jenis_role+"','"+registered_by+"','"+id_petugas+"');")
            curr.execute(q_insert)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'User Registered'
        return json.dumps(res_data)

    except Exception as e:
        res_data = {}
        app.logger.error('An error occured.')
        app.logger.error(e)
        res_data['ACK'] = 'NOK'
        res_data['msg'] = str(e)
        return json.dumps(res_data)

def inquiry_petugas():
    res_data = {}
    if request.method == 'GET':
        db = connection.get_db()
        curr = db.cursor()
        q_is_exist = (
            "SELECT id_petugas, fullname, email, address, username, jenis_role, registered_by FROM `tb_ms_login` WHERE flagactive = TRUE;")
        curr.execute(q_is_exist)
        rs = curr.fetchall()
        res_data['response'] = 'OK'
        res_data['petugas'] = rs
        res_data['len_data'] = len(rs)
        db.close()
        return json.dumps(res_data)

def modify_petugas():
    res_data = {}
    if request.method == 'GET':
        return api_version
    else:
        if not request.json:
            abort(400)
        data = request.json
        id_petugas = str(data['id_petugas'])
        nama_petugas = str(data['nama_petugas'])
        alamat_petugas = str(data['alamat_petugas'])
        email_petugas = str(data['email_petugas'])
        # edit_by = str(data['edit_by'])
        jenis_role = str(data['jenis_role'])

        db = connection.get_db()
        curr = db.cursor()
        q_modify = (
                    "UPDATE `db_koperasi`.`tb_ms_login` SET `fullname` = '" + nama_petugas + "', `address` = '" + alamat_petugas + "', `email` = '" + email_petugas + "', `jenis_role` = '" + jenis_role + "' WHERE `id_petugas` = '" + id_petugas + "';")
        print (q_modify)
        curr.execute(q_modify)
        db.commit()
        res_data['response'] = 'OK'
        res_data['msg'] = 'Data Petugas Berhasil diUpdate'
    return json.dumps(res_data)

def delete_petugas():
    res_data = {}
    print (request.json)
    if request.method == 'GET':
        return api_version
    else:
        if not request.json:
            abort(400)
        data = request.json
        id_petugas = str(data['id_petugas'])

        app.logger.info("input :" + str(data))
        db = connection.get_db()
        curr = db.cursor()

        q_modify = (
                    "UPDATE `db_koperasi`.`tb_ms_login` set `flagactive` = FALSE WHERE `id_petugas` = '" + id_petugas + "';")
        print (q_modify)
        curr.execute(q_modify)
        db.commit()
        res_data['response'] = 'OK'
        res_data['msg'] = 'Petugas Berhasil Dihapus dari sistem'
    return json.dumps(res_data)