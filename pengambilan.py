import datetime
from flask import request, abort, json
from koperasi import *
import connection

# PENGAMBILAN
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

def get_detail_pinjaman(id_anggota):
        res_data = {}
        if request.method == 'GET':
            id_anggota_ = "UTI/"+id_anggota
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                "SELECT tb_kredit.id_anggota, tb_anggota.nama_anggota, concat('Rp ', format(tb_kredit.jumlah_pinjaman,2)), concat('Rp ', format((simpanan_suka+simpanan_pokok+simpanan_wajib),2)) as saldo, id_kredit FROM `tb_anggota` join `tb_kredit` on tb_anggota.id_anggota = tb_kredit.id_anggota  where tb_kredit.`flag_active`='t' and tb_kredit.id_anggota = '"+id_anggota_+"' order by nama_anggota;")
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

            koperasi.logger.info("input :" + str(data))
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

def inquiry_pengambilan():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = ("select a.`id_transaksi_pengambilan`, a.`id_transaksi_peminjaman`, a.`tanggal_pengambilan`, a.`id_anggota`, b.`nama_anggota`,concat('Rp ',format(c.`jumlah_pinjaman`,2)), a.`insert_by` from `db_koperasi`.`tb_pengambilan` a join tb_anggota b on a.id_anggota = b.id_anggota join tb_kredit c on a.`id_transaksi_peminjaman` = c.id_kredit ORDER BY a.tanggal_pengambilan")
            print (sql_inquiry)
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)