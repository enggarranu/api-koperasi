from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import petugas
import login
import anggota
import setoran
import pinjaman
import pengambilan
import pembayaran

app = Flask(__name__)
CORS(app)
api_version = "API_KOPERASI Ver 2017.9 By Eng | (c) Copyrights Enggar 2017"

# PETUGAS
@app.route('/register_petugas_get_id', methods=["GET",])
def register_petugas_get_id():
    return petugas.register_petugas_get_id()

@app.route('/register_petugas', methods=["POST","GET"])
def register():
    return petugas.register()

@app.route('/inquiry_petugas', methods=["GET",])
def inquiry_petugas():
    return petugas.inquiry_petugas()

@app.route('/modify_petugas', methods=["POST","GET"])
def modify_petugas():
    return petugas.modify_petugas()

@app.route('/delete_petugas', methods=["POST","GET"])
def delete_petugas():
    return petugas.delete_petugas()

# LOGIN
@app.route('/login', methods=["POST","GET"])
def login():
    return login.login()

# ANGGOTA
@app.route('/register_anggota', methods=["POST","GET"])
def register_anggota():
    return anggota.register_anggota()

@app.route('/register_anggota_get_id', methods=["GET",])
def register_anggot_get_id():
    return anggota.register_anggota()

@app.route('/inquiry_anggota/<id>', methods=["GET",])
def inquiry_anggota(id):
    return anggota.inquiry_anggota(id)

@app.route('/modify_anggota', methods=["POST","GET"])
def modify_anggota():
    return anggota.modify_anggota()

@app.route('/delete_anggota', methods=["POST","GET"])
def delete_anggota():
    return anggota.delete_anggota()

# SETORAN
@app.route('/get_id_transaksi_setoran', methods=["GET",])
def get_idtransaksi_setoran():
    return setoran.get_idtransaksi_setoran()

@app.route('/inquiry_setoran', methods=["GET",])
def inquiry_setoran():
    return setoran.inquiry_setoran()

@app.route('/modify_setoran', methods=["POST","GET"])
def modify_setoran():
    return setoran.modify_setoran()

# PINJAMAN
@app.route('/get_id_transaksi_pinjaman', methods=["GET",])
def get_idtransaksi_pinjaman():
    return pinjaman.get_idtransaksi_pinjaman()

@app.route('/register_pinjaman', methods=["POST","GET"])
def register_pinjaman():
    return pinjaman.register_pinjaman()

@app.route('/inquiry_pinjaman', methods=["GET",])
def inquiry_pinjaman():
    return pinjaman.inquiry_pinjaman()

# PENGAMBILAN
@app.route('/get_id_transaksi_pengambilan_pinjaman', methods=["GET",])
def get_id_transaksi_pengambilan_pinjaman():
    return pengambilan.get_id_transaksi_pengambilan_pinjaman()

@app.route('/get_detail_pinjaman/UTI/<id_anggota>', methods=["GET",])
def get_detail_pinjaman(id_anggota):
    return pengambilan.get_detail_pinjaman(id_anggota)

@app.route('/register_pengambilan', methods=["POST","GET"])
def register_pengambilan():
    return pengambilan.register_pengambilan()

@app.route('/inquiry_pengambilan', methods=["GET",])
def inquiry_pengambilan():
    return pengambilan.inquiry_pengambilan()


# PEMBAYARAN_CICILAN
@app.route('/get_id_transaksi_pembayaran', methods=["GET",])
def get_id_transaksi_pembayaran():
    return pembayaran.get_id_transaksi_pembayaran()

if __name__ == '__main__':
    handler = RotatingFileHandler('/var/log/api-koperasi/API_KOPERASI.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='172.21.151.159', port=5000, threaded=True, debug=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)