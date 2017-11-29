# -*- coding:utf-8 -*-
'''
通过运行本脚本，可以自动把user_info.json, start_used_vpn.json, used_vpn.json的时间设定到未来
5分钟，并自动插入数据库。
需要保持这三个文件和python脚本在一个文件夹下面，并且不能改变文件的结构

如果需要增加插入数量，请在文件里面copy/paste,并修改user_id, phone, imei, relation_id

'''


import time
import json
from elasticsearch import Elasticsearch

# 把目录下面的三个文件时间改为5分钟后
def forward_five_mins(filename):

    with open(filename, 'r', encoding='utf-8') as f:
        global lines
        lines = f.readlines()

        n =0 # 用于循环中实现不同用户的时间有差异，目前的实现是1秒

        for x in lines:
            if lines.index(x) % 2 == 1:
                d = json.loads(x)
                set_time  = round(time.time() * 1000) + 5*60*1000
                set_date = time.strftime("%Y-%m-%d", time.localtime())

                if d.get('create_timestamp') :
                    d["create_timestamp"] = str(set_time + n*1000)

                if d.get("data_time"):
                    d["date_time"] = set_date

                if d.get("start_time"):
                    d["start_time"] = str(set_time + n*1000)

                if d.get("data_timestamp"):
                    d["data_timestamp"] = str(set_time + n*1000)

                if d.get("end_time"):
                    d["end_time"] = str(set_time + 60*60*1000)

                lines[lines.index(x)]= json.dumps(d, ensure_ascii=False) + '\n'

                n = n + 1

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(''.join(lines))


# 把三个文件的数据插入ES库
def insert_data(filename):
    es = Elasticsearch('172.16.37.40:9200')
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for x in lines:
            if lines.index(x) % 2 == 1:
                d= json.loads(x)
                if filename =='user_info.json':
                    es.index(index="vpn", doc_type="user_info", body=d)
                if filename =='start_used_vpn.json':
                    es.index(index="vpn", doc_type="start_used_vpn", body=d)
                if filename == 'used_vpn.json':
                    es.index(index="vpn", doc_type="used_vpn", body=d)


if __name__ == '__main__':
    forward_five_mins('user_info.json')
    forward_five_mins('start_used_vpn.json')
    forward_five_mins('used_vpn.json')

    insert_data('user_info.json')
    insert_data('start_used_vpn.json')
    insert_data('used_vpn.json')