import hashlib

import psycopg2
from flask import Flask, request, abort, json
from flask_cors import CORS
import connection
import MySQLdb
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)
api_version = "API_KOPERASI Ver 2017.9 By Eng | (c) Copyrights Enggar 2017"

# ANGGOTA
@app.route('/register', methods=["POST","GET"])
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
            city = data['city']
            country = data['country']

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

            q_insert = ("INSERT INTO `tb_ms_login` (username, password, fullname, email, address, city, country) values ('"+username+"','"+password+"','"+fullname+"','"+email+"','"+address+"','"+city+"','"+country+"');")
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

@app.route('/login', methods=["POST","GET"])
def login():
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

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = ("SELECT fullname, username FROM `tb_ms_login` where username = '"+username+"' and password = '"+password+"';")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            if len(rs) < 1:
                res_data['response'] = 'NOK'
                res_data['msg'] = 'Username atau password salah, Mohon cek kembali!!!'
                return json.dumps(res_data)
            fullname = rs[0][0]
            username = rs[0][1]
            if (fullname != None or username != None) :
                res_data['response'] = 'OK'
                res_data['msg'] = 'Success Login!!'
                res_data['fullname'] = fullname
                print(res_data)
                return json.dumps(res_data)
    except Exception as e:
        res_data = {}
        app.logger.error('An error occured.')
        app.logger.error(e)
        res_data['ACK'] = 'NOK'
        res_data['msg'] = str(e)
        return json.dumps(res_data)

@app.route('/register_anggota', methods=["POST","GET"])
def register_anggota():
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            id_anggota = data['id_anggota']
            nama = data['nama_anggota']
            ktp = data['ktp']
            alamat = data['alamat']
            telepon = data['telepon']
            petugas = data['insert_by']
            tanggal_registrasi = data['tanggal_registrasi']

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_anggota) as jumlah FROM `tb_anggota` where ktp = '" + ktp + "';")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            if jumlah_row > 0:
                res_data['response'] = 'NOK'
                res_data['msg'] = 'KTP Anggota Telah Terdaftar'
                return json.dumps(res_data)

            q_insert = (
                        "INSERT INTO `tb_anggota` (tanggal_registrasi, id_anggota, nama_anggota, ktp, alamat, telepon, insert_by, flag_active) values ('" + tanggal_registrasi + "','" + id_anggota + "','" + nama + "','" + ktp + "','" + alamat + "','" + telepon + "','" + petugas + "','t');")
            curr.execute(q_insert)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Anggota berhasil didaftarkan'
        return json.dumps(res_data)

@app.route('/register_anggota_get_id', methods=["GET",])
def register_anggot_get_id():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_anggota) as jumlah FROM `tb_anggota`;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            res_data['response'] = 'OK'
            res_data['msg'] = 'UTI/AGT000'+str(jumlah_row+1)
            db.close()
            return json.dumps(res_data)

@app.route('/inquiry_anggota/<id>', methods=["GET",])
def inquiry_anggota(id):
        res_data = {}
        if request.method == 'GET':
            prefix = 'UTI/AGT000'
            id_anggota = prefix + id
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = (
                        "select `id_anggota`, `nama_anggota`, `ktp`, `alamat`, `telepon`, `simpanan_wajib`, `simpanan_pokok`, `simpanan_suka`, `saldo`, `insert_by`, `edit_by`, `tanggal_registrasi`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1")
            if (id_anggota == 'UTI/AGT0000'):
                sql_inquiry = sql_inquiry + " and flag_active = 't';"
            else:
                sql_inquiry = sql_inquiry + " and id_anggota = '%s';" % id_anggota
            print sql_inquiry
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)


@app.route('/modify_anggota', methods=["POST","GET"])
def modify_anggota():
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            id_anggota = str(data['id_anggota'])
            nama_anggota = str(data['nama_anggota'])
            ktp = str(data['ktp'])
            alamat = str(data['alamat'])
            telepon = str(data['telepon'])
            edit_by = str(data['edit_by'])
            tanggal_modifikasi = str(data['tanggal_modifikasi'])
            old_ktp = str(data['ktp_old'])

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            if ktp != old_ktp:
                q_is_exist = (
                        "SELECT count(id_anggota) as jumlah FROM `tb_anggota` where ktp = '" + ktp + "' and flag_active = 't';")
                curr.execute(q_is_exist)
                rs = curr.fetchall()
                jumlah_row = rs[0][0]
                if jumlah_row > 0:
                    res_data['response'] = 'NOK'
                    res_data['msg'] = 'KTP Anggota Telah Terdaftar'
                    return json.dumps(res_data)

            q_modify = ("UPDATE `db_koperasi`.`tb_anggota` SET `nama_anggota` = '"+nama_anggota+"', `alamat` = '"+alamat+"', `telepon` = '"+telepon+"', `edit_by` = '"+edit_by+"', `ktp` = '"+ktp+"', `tanggal_modifikasi` = '"+tanggal_modifikasi+"' WHERE `id_anggota` = '"+id_anggota+"';")
            print q_modify
            curr.execute(q_modify)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Data Anggota Berhasil diUpdate'
        return json.dumps(res_data)


@app.route('/delete_anggota', methods=["POST","GET"])
def delete_anggota():
        res_data = {}
        print request.json
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            id_anggota = str(data['id_anggota'])

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()

            q_modify = ("UPDATE `db_koperasi`.`tb_anggota` set `flag_active` = 'f' WHERE `id_anggota` = '"+id_anggota+"';")
            print q_modify
            curr.execute(q_modify)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Anggota Berhasil Dihapus dari sistem'
        return json.dumps(res_data)




# SETORAN

@app.route('/get_id_transaksi_setoran', methods=["GET",])
def get_idtransaksi_setoran():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_anggota) as jumlah FROM `tb_setoran`;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            res_data['response'] = 'OK'
            res_data['msg'] = 'UTI/SETOR000'+str(jumlah_row+1)

            q_is_exist = (
                "SELECT id_anggota, nama_anggota FROM `tb_anggota` where `flag_active`='t' order by nama_anggota;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['anggota_arr'] = rs
            db.close()
            return json.dumps(res_data)


@app.route('/inquiry_setoran', methods=["GET",])
def inquiry_setoran():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = ("select `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, `nominal`, `saldo`, `insert_date`, `insert_by` from `tb_setoran` order by `id_transaksi`")
            print sql_inquiry
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)

@app.route('/modify_setoran', methods=["POST","GET"])
def modify_setoran():
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            id_transaksi = str(data['id_transaksi'])
            id_anggota = str(data['id_anggota'])
            jenis_simpanan = str(data['jenis_simpanan'])
            nominal = str(data['nominal'])
            edit_by = str(data['insert_by'])
            tanggal_modifikasi = str(data['tanggal_setoran'])


            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()

            q_is_exist = (
                    "select `id_anggota`, `nama_anggota`, `simpanan_wajib`, `simpanan_pokok`, `simpanan_suka`, `saldo`, `edit_by`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1 and `id_anggota` = '"+id_anggota+"' and `flag_active` = 't';")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            simpanan_wajib = rs[0][2]
            simpanan_pokok = rs[0][3]
            simpanan_suka = rs[0][4]
            saldo = rs[0][5]
            nama_anggota = rs[0][1]
            lb_setoran = ""
            if jenis_simpanan == "simpanan_suka":
                lb_setoran = simpanan_suka = str(int(simpanan_suka) + int(nominal))
            if jenis_simpanan == "simpanan_pokok" :
                lb_setoran = simpanan_pokok = str(int(simpanan_pokok) + int(nominal))
            if jenis_simpanan == "simpanan_wajib" :
                lb_setoran = simpanan_wajib = str(int(simpanan_wajib)+int(nominal))
            if jenis_simpanan == "saldo" :
                lb_setoran = saldo = str(int(saldo) + int(nominal))

            q_modify = ("UPDATE `db_koperasi`.`tb_anggota` SET `simpanan_wajib` = '"+simpanan_wajib+"', `simpanan_pokok` = '"+simpanan_pokok+"', `simpanan_suka` = '"+simpanan_suka+"', `saldo` = '"+saldo+"', `edit_by` = '"+edit_by+"', `tanggal_modifikasi` = '"+tanggal_modifikasi+"' WHERE `id_anggota` = '"+id_anggota+"';")
            print q_modify
            curr.execute(q_modify)

            q_insert_tb_setoran = ("INSERT INTO `db_koperasi`.`tb_setoran` ( `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, `nominal`, `saldo`, `insert_date`, `insert_by` ) VALUES ( '"+id_transaksi+"', '"+id_anggota+"', '"+nama_anggota+"', '"+jenis_simpanan+"', '"+nominal+"', '"+lb_setoran+"', '"+tanggal_modifikasi+"', '"+edit_by+"' );")
            print q_modify
            curr.execute(q_insert_tb_setoran)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Saldo Berhasil diUpdate'
        return json.dumps(res_data)

if __name__ == '__main__':
    handler = RotatingFileHandler('API_KOPERASI.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)