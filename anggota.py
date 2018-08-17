from flask import request, abort, json
import connection
from koperasi import *


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

        koperasi.logger.info("input :" + str(data))
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
        res_data['msg'] = 'UTI/AGT000' + str(jumlah_row + 1)
        db.close()
        return json.dumps(res_data)

def inquiry_anggota(id):
    res_data = {}
    if request.method == 'GET':
        prefix = 'UTI/AGT000'
        id_anggota = prefix + id
        db = connection.get_db()
        curr = db.cursor()
        sql_inquiry = (
            "select `id_anggota`, `nama_anggota`, `ktp`, `alamat`, `telepon`, concat('Rp ',format(`simpanan_wajib`,2)), concat('Rp ',format(`simpanan_pokok`,2)), concat('Rp ',format(`simpanan_suka`,2)),  concat('Rp ',format(`simpanan_wajib`  + `simpanan_pokok` + `simpanan_suka`,2)) as `saldo`, `insert_by`, `edit_by`, `tanggal_registrasi`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1")
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

        koperasi.logger.info("input :" + str(data))
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

        q_modify = (
                    "UPDATE `db_koperasi`.`tb_anggota` SET `nama_anggota` = '" + nama_anggota + "', `alamat` = '" + alamat + "', `telepon` = '" + telepon + "', `edit_by` = '" + edit_by + "', `ktp` = '" + ktp + "', `tanggal_modifikasi` = '" + tanggal_modifikasi + "' WHERE `id_anggota` = '" + id_anggota + "';")
        print (q_modify)
        curr.execute(q_modify)
        db.commit()
        res_data['response'] = 'OK'
        res_data['msg'] = 'Data Anggota Berhasil diUpdate'
    return json.dumps(res_data)

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

        koperasi.logger.info("input :" + str(data))
        db = connection.get_db()
        curr = db.cursor()

        q_modify = (
                    "UPDATE `db_koperasi`.`tb_anggota` set `flag_active` = 'f' WHERE `id_anggota` = '" + id_anggota + "';")
        print (q_modify)
        curr.execute(q_modify)
        db.commit()
        res_data['response'] = 'OK'
        res_data['msg'] = 'Anggota Berhasil Dihapus dari sistem'
    return json.dumps(res_data)