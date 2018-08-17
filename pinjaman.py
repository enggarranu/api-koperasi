import datetime
from flask import request, abort, json
from app import *
import connection

# PINJAMAN
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

            q_is_exist = ("SELECT tb_anggota.id_anggota, tb_anggota.nama_anggota FROM `tb_anggota` where tb_anggota.`flag_active`='t' and tb_anggota.id_anggota not in (select id_anggota from tb_kredit) order by nama_anggota;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['anggota_arr'] = rs
            db.close()
            return json.dumps(res_data)

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


            q_check_tb_kredit =()

            q_insert_tb_kredit = ("INSERT INTO `db_koperasi`.`tb_kredit` ( `id_kredit`, `id_anggota`, `jumlah_pinjaman`, `bunga`, `lama_cicilan`, `angsuran`, `flag_active`, `insert_date`, `insert_by` ) VALUES ( '"+id_transaksi+"', '"+id_anggota+"', '"+jumlah_pinjaman+"', '"+bunga+"', '"+tenor+"', '"+angsuran_perbulan+"', '"+flag_active+"', '"+insert_date+"', '"+insert_by+"');")
            print (q_insert_tb_kredit)
            curr.execute(q_insert_tb_kredit)
            db.commit()
            res_data['response'] = 'OK'
            res_data['msg'] = 'Pinjaman berhasil diajukan'
        return json.dumps(res_data)

def inquiry_pinjaman():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            sql_inquiry = ("SELECT a.id_kredit, a. id_anggota, b.nama_anggota, concat('Rp ', format(b.saldo,2)), concat('Rp ', format(a.jumlah_pinjaman,2)), concat(a.bunga, '%'), concat(a.lama_cicilan, ' Bulan'), concat('Rp ', format(a.angsuran,2)), a.insert_date, a.insert_by FROM tb_kredit a JOIN ( SELECT id_anggota, nama_anggota, cast( simpanan_wajib AS SIGNED ) + cast( simpanan_suka AS SIGNED ) + cast( simpanan_pokok AS SIGNED ) saldo FROM tb_anggota ) b ON a.id_anggota = b.id_anggota")
            print (sql_inquiry)
            curr.execute(sql_inquiry)
            rs = curr.fetchall()
            res_data['response'] = 'OK'
            res_data['anggota'] = rs
            res_data['len_data'] = len(rs)
            db.close()
            return json.dumps(res_data)