import datetime
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
                        "select `id_anggota`, `nama_anggota`, `ktp`, `alamat`, `telepon`, `simpanan_wajib`, `simpanan_pokok`, `simpanan_suka`,  `simpanan_wajib`  + `simpanan_pokok` + `simpanan_suka` as `saldo`, `insert_by`, `edit_by`, `tanggal_registrasi`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1")
            if (id_anggota == 'UTI/AGT0000'):
                sql_inquiry = sql_inquiry + " and flag_active = 't';"
            else:
                sql_inquiry = sql_inquiry + " and id_anggota = '%s';" % id_anggota
            print (sql_inquiry)
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
            print (q_modify)
            curr.execute(q_modify)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Data Anggota Berhasil diUpdate'
        return json.dumps(res_data)


@app.route('/delete_anggota', methods=["POST","GET"])
def delete_anggota():
        res_data = {}
        print (request.json)
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
            print (q_modify)
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
            res_data['msg'] = 'UTI/SMP'+str(datetime.datetime.today().strftime('%Y%m%d'))+str(jumlah_row+1)

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
            sql_inquiry = ("select `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, `nominal`, `saldo`, `insert_date`, `insert_by` from `tb_setoran` order by cast(replace(`id_transaksi`,'UTI/SETOR000','') as UNSIGNED)")
            print (sql_inquiry)
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
                    "select `id_anggota`, `nama_anggota`, `simpanan_wajib`, `simpanan_pokok`, `simpanan_suka`, `simpanan_wajib`  + `simpanan_pokok`  + `simpanan_suka` as `saldo`, `edit_by`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1 and `id_anggota` = '"+id_anggota+"' and `flag_active` = 't';")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            simpanan_wajib = str(rs[0][2])
            simpanan_pokok = str(rs[0][3])
            simpanan_suka = str(rs[0][4])
            saldo = str(rs[0][5])
            nama_anggota = rs[0][1]
            if jenis_simpanan == "simpanan_suka":
                simpanan_suka = str(int(simpanan_suka) + int(nominal))
            if jenis_simpanan == "simpanan_pokok" :
                simpanan_pokok = str(int(simpanan_pokok) + int(nominal))
            if jenis_simpanan == "simpanan_wajib" :
                simpanan_wajib = str(int(simpanan_wajib)+int(nominal))
            lb_setoran = str(int(saldo) + int(nominal))

            print (type(id_anggota))
            print (type(simpanan_suka))
            print (type(simpanan_wajib))
            print (type(simpanan_pokok))
            print (type(saldo))

            q_modify = ("UPDATE `db_koperasi`.`tb_anggota` SET `simpanan_wajib` = '"+simpanan_wajib+"', `simpanan_pokok` = '"+simpanan_pokok+"', `simpanan_suka` = '"+simpanan_suka+"', `edit_by` = '"+edit_by+"', `tanggal_modifikasi` = '"+tanggal_modifikasi+"' WHERE `id_anggota` = '"+id_anggota+"';")
            print (q_modify)
            curr.execute(q_modify)

            q_insert_tb_setoran = ("INSERT INTO `db_koperasi`.`tb_setoran` ( `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, `nominal`, `saldo`, `insert_date`, `insert_by` ) VALUES ( '"+id_transaksi+"', '"+id_anggota+"', '"+nama_anggota+"', '"+jenis_simpanan+"', '"+nominal+"', '"+lb_setoran+"', '"+tanggal_modifikasi+"', '"+edit_by+"' );")
            print (q_modify)
            curr.execute(q_insert_tb_setoran)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Saldo Berhasil diUpdate'
        return json.dumps(res_data)


# PINJAMAN

@app.route('/get_id_transaksi_pinjaman', methods=["GET",])
def get_idtransaksi_pinjaman():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_kredit) as jumlah FROM `tb_kredit`;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            res_data['response'] = 'OK'
            res_data['msg'] = 'UTI/PNJ'+str(datetime.datetime.today().strftime('%Y%m%d'))+str(jumlah_row+1)

            q_is_exist = (
                "SELECT id_anggota, nama_anggota FROM `tb_anggota` where `flag_active`='t' order by nama_anggota;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['anggota_arr'] = rs
            db.close()
            return json.dumps(res_data)

@app.route('/register_pinjaman', methods=["POST","GET"])
def register_pinjaman():
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            id_transaksi = str(data['id_transaksi'])
            id_anggota = str(data['id_anggota'])
            jumlah_pinjaman = str(data['jumlah_pinjaman'])
            bunga = str(data['bunga_pertahun'])
            tenor = str(data['tenor'])
            angsuran_perbulan = str(data['angsuran_perbulan'])
            flag_active = 't'
            insert_date = str(data['tanggal_setoran'])
            insert_by = str(data['insert_by'])

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()

            q_insert_tb_kredit = ("INSERT INTO `db_koperasi`.`tb_kredit` ( `id_kredit`, `id_anggota`, `jumlah_pinjaman`, `bunga`, `lama_cicilan`, `angsuran`, `flag_active`, `insert_date`, `insert_by` ) VALUES ( '"+id_transaksi+"', '"+id_anggota+"', '"+jumlah_pinjaman+"', '"+bunga+"', '"+tenor+"', '"+angsuran_perbulan+"', '"+flag_active+"', '"+insert_date+"', '"+insert_by+"');")
            print (q_insert_tb_kredit)
            curr.execute(q_insert_tb_kredit)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Pinjaman berhasil diajukan'
        return json.dumps(res_data)

@app.route('/inquiry_pinjaman', methods=["GET",])
def inquiry_pinjaman():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = ("SELECT a.id_kredit, a. id_anggota, b.nama_anggota, b.saldo, a.jumlah_pinjaman, a.bunga, a.lama_cicilan, a.angsuran, a.insert_date, a.insert_by FROM tb_kredit a JOIN ( SELECT id_anggota, nama_anggota, cast( simpanan_wajib AS SIGNED ) + cast( simpanan_suka AS SIGNED ) + cast( simpanan_pokok AS SIGNED ) saldo FROM tb_anggota ) b ON a.id_anggota = b.id_anggota")
            print (sql_inquiry)
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)

# PENGAMBILAN
@app.route('/get_id_transaksi_pengambilan_pinjaman', methods=["GET",])
def get_id_transaksi_pengambilan_pinjaman():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_pengambilan) as jumlah FROM `tb_kredit`;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            res_data['response'] = 'OK'
            res_data['msg'] = 'UTI/PBL'+str(datetime.datetime.today().strftime('%Y%m%d'))+str(jumlah_row+1)

            q_is_exist = (
                "SELECT tb_kredit.id_anggota, tb_anggota.nama_anggota, tb_kredit.jumlah_pinjaman FROM `tb_anggota` join `tb_kredit` on tb_anggota.id_anggota = tb_kredit.id_anggota  where tb_kredit.`flag_active`='t' and tb_kredit.id_pengambilan is NULL order by nama_anggota;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['anggota_arr'] = rs
            db.close()
            return json.dumps(res_data)

@app.route('/get_detail_pinjaman/UTI/<id_anggota>', methods=["GET",])
def get_detail_pinjaman(id_anggota):
        res_data = {}
        if request.method == 'GET':
            id_anggota_ = "UTI/"+id_anggota
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                "SELECT tb_kredit.id_anggota, tb_anggota.nama_anggota, tb_kredit.jumlah_pinjaman, (simpanan_suka+simpanan_pokok+simpanan_wajib) as saldo, id_kredit FROM `tb_anggota` join `tb_kredit` on tb_anggota.id_anggota = tb_kredit.id_anggota  where tb_kredit.`flag_active`='t' and tb_kredit.id_anggota = '"+id_anggota_+"' order by nama_anggota;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['id_anggota'] = rs[0][0]
            res_data['nama_anggota'] = rs[0][1]
            res_data['jumlah_pinjaman'] = rs[0][2]
            res_data['saldo'] = rs[0][3]
            res_data['id_kredit'] = rs[0][4]
            res_data['response'] = 'OK'
            db.close()
            return json.dumps(res_data)

@app.route('/register_pengambilan', methods=["POST","GET"])
def register_pengambilan():
        res_data = {}
        if request.method == 'GET':
            return api_version
        else:
            if not request.json:
                abort(400)
            data = request.json
            print (data)
            id_transaksi_pengambilan = str(data['id_transaksi_pengambilan'])
            id_transaksi_peminjaman = str(data['id_transaksi_peminjaman'])
            id_anggota = str(data['id_anggota'])
            tanggal_pengambilan = str(data['tanggal_pengambilan'])
            insert_by = str(data['insert_by'])

            app.logger.info("input :" + str(data))
            db = connection.get_db()
            curr = db.cursor()

            q_insert_tb_pengambilan = ("INSERT INTO `db_koperasi`.`tb_pengambilan` ( `id_transaksi_pengambilan`, `id_transaksi_peminjaman`, `tanggal_pengambilan`, `id_anggota`, `insert_by`) VALUES ( '"+id_transaksi_pengambilan+"', '"+id_transaksi_peminjaman+"', '"+tanggal_pengambilan+"', '"+id_anggota+"', '"+insert_by+"');")
            print (q_insert_tb_pengambilan)
            curr.execute(q_insert_tb_pengambilan)
            q_update_tb_kredit = ("UPDATE `db_koperasi`.`tb_kredit` SET `id_pengambilan` = '"+id_transaksi_pengambilan+"', `tanggal_pengambilan` = '"+tanggal_pengambilan+"', `update_by` = '"+insert_by+"' WHERE `id_kredit` = '"+id_transaksi_peminjaman+"';")
            print(q_update_tb_kredit)
            curr.execute(q_update_tb_kredit)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Pengambilan berhasil dilakukan'
        return json.dumps(res_data)

@app.route('/inquiry_pengambilan', methods=["GET",])
def inquiry_pengambilan():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = ("select a.`id_transaksi_pengambilan`, a.`id_transaksi_peminjaman`, a.`tanggal_pengambilan`, a.`id_anggota`, b.`nama_anggota`, a.`insert_by` from `db_koperasi`.`tb_pengambilan` a join tb_anggota b on a.id_anggota = b.id_anggota ORDER BY a.tanggal_pengambilan")
            print (sql_inquiry)
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)

if __name__ == '__main__':
    handler = RotatingFileHandler('API_KOPERASI.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    try:
        app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
    except:
        print("Error app")
    # app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)