import hashlib

from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
import logging
from logging.handlers import RotatingFileHandler

import connection
from petugas import *
import login
from anggota import *
import setoran
import pinjaman
import pengambilan
import pembayaran

koperasi = Flask(__name__)
CORS(koperasi)
cors = CORS(koperasi, resorces={r'/d/*': {"origins": '*'}})


# PETUGAS
@koperasi.route('/register_petugas_get_id', methods=["GET", ])
def register_petugas_get_id():
    return petugas.register_petugas_get_id()

@koperasi.route('/register_petugas', methods=["POST", "GET"])
def register():
    return petugas.register()

@koperasi.route('/inquiry_petugas', methods=["GET", ])
def inquiry_petugas():
    return petugas.inquiry_petugas()

@koperasi.route('/modify_petugas', methods=["POST", "GET"])
def modify_petugas():
    return petugas.modify_petugas()

@koperasi.route('/delete_petugas', methods=["POST", "GET"])
def delete_petugas():
    return petugas.delete_petugas()

# LOGIN
@koperasi.route('/login', methods=["POST", "GET"])
def login():
    # return login.login_petugas()

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
            if (data['signature'] != hashlib.md5(username + password).hexdigest()):
                res_data['response'] = 'NOK'
                res_data['msg'] = 'Invalid Signature!'
                print(data['signature'])
                print(hashlib.md5(username + password).hexdigest())
                return jsonify(res_data)

            koperasi.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT fullname, username, jenis_role FROM `tb_ms_login` where username = '" + username + "' and password = '" + password + "';")
            koperasi.logger.info(q_is_exist)
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            if len(rs) < 1:
                res_data['response'] = 'NOK'
                res_data['msg'] = 'Username atau password salah, Mohon cek kembali!!!'
                return jsonify(res_data)

            fullname = rs[0][0]
            username = rs[0][1]
            jenis_role = rs[0][2]
            if (fullname != None or username != None):
                res_data['response'] = 'OK'
                res_data['msg'] = 'Success Login!!'
                res_data['fullname'] = fullname
                res_data['jenis_role'] = jenis_role
                koperasi.logger.info(res_data)
                return jsonify(res_data)

    except Exception as e:
        res_data = {}
        koperasi.logger.error('An error occured.')
        koperasi.logger.error(e)
        res_data['ACK'] = 'NOK'
        res_data['msg'] = str(e)
        return jsonify(res_data)

# ANGGOTA
@koperasi.route('/register_anggota', methods=["POST", "GET"])
def register_anggota():
    return anggota.register_anggota()

@koperasi.route('/register_anggota_get_id', methods=["GET", ])
def register_anggot_get_id():
    return anggota.register_anggota()

@koperasi.route('/inquiry_anggota/<id>', methods=["GET", ])
def inquiry_anggota(id):
    return anggota.inquiry_anggota(id)

@koperasi.route('/modify_anggota', methods=["POST", "GET"])
def modify_anggota():
    return anggota.modify_anggota()

@koperasi.route('/delete_anggota', methods=["POST", "GET"])
def delete_anggota():
    return anggota.delete_anggota()

# SETORAN
@koperasi.route('/get_id_transaksi_setoran', methods=["GET", ])
def get_idtransaksi_setoran():
    return setoran.get_idtransaksi_setoran()

@koperasi.route('/inquiry_setoran', methods=["GET", ])
def inquiry_setoran():
    return setoran.inquiry_setoran()

@koperasi.route('/modify_setoran', methods=["POST", "GET"])
def modify_setoran():
    return setoran.modify_setoran()

# PINJAMAN
@koperasi.route('/get_id_transaksi_pinjaman', methods=["GET", ])
def get_idtransaksi_pinjaman():
    return pinjaman.get_idtransaksi_pinjaman()

@koperasi.route('/register_pinjaman', methods=["POST", "GET"])
def register_pinjaman():
    return pinjaman.register_pinjaman()

@koperasi.route('/inquiry_pinjaman', methods=["GET", ])
def inquiry_pinjaman():
    return pinjaman.inquiry_pinjaman()

# PENGAMBILAN
@koperasi.route('/get_id_transaksi_pengambilan_pinjaman', methods=["GET", ])
def get_id_transaksi_pengambilan_pinjaman():
    return pengambilan.get_id_transaksi_pengambilan_pinjaman()

@koperasi.route('/get_detail_pinjaman/UTI/<id_anggota>', methods=["GET", ])
def get_detail_pinjaman(id_anggota):
    return pengambilan.get_detail_pinjaman(id_anggota)

@koperasi.route('/register_pengambilan', methods=["POST", "GET"])
def register_pengambilan():
    return pengambilan.register_pengambilan()

@koperasi.route('/inquiry_pengambilan', methods=["GET", ])
def inquiry_pengambilan():
    return pengambilan.inquiry_pengambilan()


# PEMBAYARAN_CICILAN
@koperasi.route('/get_id_transaksi_pembayaran', methods=["GET", ])
def get_id_transaksi_pembayaran():
    return pembayaran.get_id_transaksi_pembayaran()

if __name__ == '__main__':
    handler = RotatingFileHandler('/var/log/api-koperasi/API_KOPERASI.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    koperasi.logger.addHandler(handler)
    koperasi.run(host='172.21.151.159', port=5000, threaded=True, debug=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)