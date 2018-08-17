import datetime
from flask import request, json
import connection
from koperasi import *

def get_id_transaksi_pembayaran():
        res_data = {}
        if request.method == 'GET':
            db = connection.get_db()
            curr = db.cursor()
            q_is_exist = (
                        "SELECT count(id_pembayaran) as jumlah FROM `tb_pembayaran`;")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            jumlah_row = rs[0][0]
            res_data['response'] = 'OK'
            res_data['msg'] = 'UTI/ANS'+str(datetime.datetime.today().strftime('%Y%m%d'))+str(jumlah_row+1)

            q_is_exist = ("SELECT\n" +
"	ta.id_anggota, ta.nama_anggota, kr.id_kredit, id_pengambilan\n" +
"FROM\n" +
"	`tb_kredit` kr\n" +
"	LEFT JOIN tb_pembayaran pb ON kr.id_kredit = pb.id_kredit\n" +
"	JOIN tb_anggota ta on ta.id_anggota = kr.id_anggota\n" +
"WHERE\n" +
"	kr.id_pengambilan IS NOT NULL")
            curr.execute(q_is_exist)
            rs = curr.fetchall()
            res_data['anggota_arr'] = rs
            db.close()
            return json.dumps(res_data)