import datetime
from flask import request, abort, json
from koperasi_main import *
import connection

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
        res_data['msg'] = 'UTI/SMP' + str(datetime.datetime.today().strftime('%Y%m%d')) + str(jumlah_row + 1)

        q_is_exist = (
            "SELECT id_anggota, nama_anggota FROM `tb_anggota` where `flag_active`='t' order by nama_anggota;")
        curr.execute(q_is_exist)
        rs = curr.fetchall()
        res_data['anggota_arr'] = rs
        db.close()
        return json.dumps(res_data)

def inquiry_setoran():
    res_data = {}
    if request.method == 'GET':
        db = connection.get_db()
        curr = db.cursor()
        sql_inquiry = (
            "select `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, concat('Rp ',format(`nominal`,2)), concat('Rp ', format(`saldo`,2)), `insert_date`, `insert_by` from `tb_setoran` order by cast(replace(`id_transaksi`,'UTI/SMP','') as UNSIGNED)")
        print (sql_inquiry)
        curr.execute(sql_inquiry)
        rs = curr.fetchall()
        res_data['response'] = 'OK'
        res_data['anggota'] = rs
        res_data['len_data'] = len(rs)
        db.close()
        return json.dumps(res_data)

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

        koperasi.logger.info("input :" + str(data))
        db = connection.get_db()
        curr = db.cursor()

        q_is_exist = (
                "select `id_anggota`, `nama_anggota`, `simpanan_wajib`, `simpanan_pokok`, `simpanan_suka`, `simpanan_wajib`  + `simpanan_pokok`  + `simpanan_suka` as `saldo`, `edit_by`, `tanggal_modifikasi` from `db_koperasi`.`tb_anggota` where 1=1 and `id_anggota` = '" + id_anggota + "' and `flag_active` = 't';")
        curr.execute(q_is_exist)
        rs = curr.fetchall()
        simpanan_wajib = str(rs[0][2])
        simpanan_pokok = str(rs[0][3])
        simpanan_suka = str(rs[0][4])
        saldo = str(rs[0][5])
        nama_anggota = rs[0][1]
        if jenis_simpanan == "simpanan_suka":
            simpanan_suka = str(int(simpanan_suka) + int(nominal))
        if jenis_simpanan == "simpanan_pokok":
            simpanan_pokok = str(int(simpanan_pokok) + int(nominal))
        if jenis_simpanan == "simpanan_wajib":
            simpanan_wajib = str(int(simpanan_wajib) + int(nominal))
        lb_setoran = str(int(saldo) + int(nominal))

        print (type(id_anggota))
        print (type(simpanan_suka))
        print (type(simpanan_wajib))
        print (type(simpanan_pokok))
        print (type(saldo))

        q_modify = (
                    "UPDATE `db_koperasi`.`tb_anggota` SET `simpanan_wajib` = '" + simpanan_wajib + "', `simpanan_pokok` = '" + simpanan_pokok + "', `simpanan_suka` = '" + simpanan_suka + "', `edit_by` = '" + edit_by + "', `tanggal_modifikasi` = '" + tanggal_modifikasi + "' WHERE `id_anggota` = '" + id_anggota + "';")
        print (q_modify)
        curr.execute(q_modify)

        q_insert_tb_setoran = (
                    "INSERT INTO `db_koperasi`.`tb_setoran` ( `id_transaksi`, `id_anggota`, `nama_anggota`, `jenis_simpanan`, `nominal`, `saldo`, `insert_date`, `insert_by` ) VALUES ( '" + id_transaksi + "', '" + id_anggota + "', '" + nama_anggota + "', '" + jenis_simpanan + "', '" + nominal + "', '" + lb_setoran + "', '" + tanggal_modifikasi + "', '" + edit_by + "' );")
        print (q_modify)
        curr.execute(q_insert_tb_setoran)
        db.commit()
        res_data['response'] = 'OK'
        res_data['msg'] = 'Saldo Berhasil diUpdate'
    return json.dumps(res_data)