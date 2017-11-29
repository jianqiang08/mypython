import time, json
import random
import copy
from elasticsearch import Elasticsearch

#一天换算下来的毫秒数, 用户计算同一个用户每天用一次不同的VPN
ONEDAY = 24 * 60 * 60* 1000

VPNS = [{"app_num":"6.0.9.89","app_package":"de.mobileconcepts.cyberghost","app_name":"CyberGhostVPN","vpn_ip_address":"6.0.9.89","risk_grades": "0","app_channel": "cn.com.shouji.market","channel_name":"手机乐园","app_type": "true"},
{"app_num":"1.0.4.2","app_package":"com.free.openinternet.vpn.proxy.unblock.websites","app_name":"VPNUnlimitedFree","vpn_ip_address":"91.134.240.216","risk_grades": "0","app_channel": "com.idiantech.kuaihuwifi","channel_name":"快虎市场","app_type": "true"},
{"app_num":"1.0.5.3","app_package":"com.lausny.ocvpn","app_name":"一键VPN","vpn_ip_address":"117.7.143.219","risk_grades": "0","app_channel": "com.idiantech.kuaihuwifi","channel_name":"快虎市场","app_type": "true"},
{"app_num":"5.3.3","app_package":"free.vpn.unblock.proxy.vpnmaster","app_name":"VPNMaster","vpn_ip_address":"159.203.246.115","risk_grades": "0","app_channel": "com.uucun106326.android.cms","channel_name":"安热市场","app_type": "true"},
{"app_num":"1.6.6","app_package":"net.invisible","app_name":"Invisible","vpn_ip_address":"144.217.51.71","risk_grades": "0","app_channel": "com.uucun106326.android.cms","channel_name":"安热市场","app_type": "true"},
{"app_num":"2.2.4","app_package":"com.in.hammervpn","app_name":"HammerVPN","vpn_ip_address":"46.4.42.38","risk_grades": "0","app_channel": "com.hiapk.marketpho","channel_name":"安卓市场","app_type": "true"},
{"app_num":"3.7.6 (20170824.235459)","app_package":"org.getlantern.lantern","app_name":"蓝灯","vpn_ip_address":"45.77.69.47","risk_grades": "0","app_channel": "com.hiapk.marketpho","channel_name":"安卓市场","app_type": "true"},
{"app_num":"38.0.0.2.66","app_package":"com.onavo.spaceship","app_name":"ProtectFreeVPN","vpn_ip_address":"185.89.219.203","risk_grades": "0","app_channel": "com.infinit.wostore.ui","channel_name":"沃商店","app_type": "true"},
{"app_num":"2.1.8","app_package":"com.in.webtunnel","app_name":"WebTunnel","vpn_ip_address":"217.23.15.55","risk_grades": "0","app_channel": "com.infinit.wostore.ui","channel_name":"沃商店","app_type": "true"},
{"app_num":"1.6","app_package":"com.ipshield.app","app_name":"VPNshield","vpn_ip_address":"108.61.250.242","risk_grades": "0","app_channel": "com.yingyonghui.market","channel_name":"应用汇","app_type": "true"},
{"app_num":"1.0.0.4","app_package":"com.free.proxyvpn.unblock.websites","app_name":"FreeVPN","vpn_ip_address":"164.132.102.194","risk_grades": "0","app_channel": "com.yingyonghui.market","channel_name":"应用汇","app_type": "true"},
{"app_num":"1.9.1","app_package":"free.vpn.unblock.proxy.turbovpn","app_name":"TurboVPN","vpn_ip_address":"178.62.59.77","risk_grades": "0","app_channel": "com.dongji.market","channel_name":"动机市场","app_type": "true"},
{"app_num":"1.4.1","app_package":"org.internetvpn.mobileapp","app_name":"InternetVPN","vpn_ip_address":"104.27.140.191","risk_grades": "0","app_channel": "com.dongji.market","channel_name":"动机市场","app_type": "true"},
{"app_num":"1.1.17","app_package":"net.openvpn.openvpn","app_name":"OpenVPN","vpn_ip_address":"54.76.135.1","risk_grades": "0","app_channel": "com.dangbeimarket","channel_name":"当贝市场","app_type": "true"},
{"app_num":"1.0.57","app_package":"me.seed4.app.android","app_name":"Seed4Me","vpn_ip_address":"103.242.110.79","risk_grades": "0","app_channel": "com.dangbeimarket","channel_name":"当贝市场","app_type": "true"},
{"app_num":"164","app_package":"com.psiphon3","app_name":"赛风","vpn_ip_address":"173.230.151.70","risk_grades": "0","app_channel": "com.dangbeimarket","channel_name":"当贝市场","app_type": "true"},
{"app_num":"4.2","app_package":"com.chengcheng.FreeVPN","app_name":"SuperVPN","vpn_ip_address":"47.88.78.154","risk_grades": "0","app_channel": "com.dangbeimarket","channel_name":"当贝市场","app_type": "true"},
{"app_num":"1.17","app_package":"xsky.txvpn","app_name":"天行VPN","vpn_ip_address":"106.186.112.102","risk_grades": "0","app_channel": "com.dangbeimarket","channel_name":"当贝市场","app_type": "true"}]


# 返回一个随机VPN
def get_vpn(vpns):
    a= random.randint(0, (len(vpns)-1))
    #print(vpns[a])
    return vpns[a]


# define a class for UserInfo Tab，
class UserInfo(object):
    def __init__(self, user_id, username, address, phone_location, base_location, location_code):
        self.user_id =user_id
        self.phone = self.user_id
        self.user_name = username
        self.address = address
        self.imei = 'SN' + user_id
        self.phone_location = phone_location
        self.base_location = base_location
        self.location_code = location_code
        # 设置时间为当前时间，具体使用的时候要根据起始时间
        self.create_timestamp = int(round(time.time() * 1000))
        #print(self.create_timestamp)

    def correcttimestamp(self,n):
        #计算一天的毫秒数
        temp = ONEDAY * (n-1)

        self.create_timestamp = self.create_timestamp - temp

        #print(self.create_timestamp)
        #print('in correct')

    def create_string(self):
        temp = r'{"create":{"_index":"vpn","_type":"user_info"}}' + '\n'

        temp = temp + r'{"user_id":"' + self.user_id + r'","phone":"' + self.phone +  \
                r'","user_name":"' + self.user_name + r'","address":"' + self.address +  \
                r'","imei":"' + self.imei + r'","phone_locaton":"' + self.phone_location + \
                r'","base_station":"' + self.base_location + r'","location_code":"' + self.location_code + \
                r'","create_timestamp":' + str(self.create_timestamp) + '}\n'

        return  temp

# 传入一个随机获取的VPN变量 app_name, app_type, risk_grades, app_channel, channel_name
class AppInfo(object):
    def __init__(self, userinfo, user_ip_address, vpn):
        self.user_id = userinfo.user_id
        self.user_ip_address = user_ip_address
        self.app_name = vpn["app_name"]
        self.app_type = vpn["app_type"]
        self.app_package = vpn["app_package"]

        #self.install_date = "2017-11-14"
        # 时间取用户第一次VPN上网前5分钟
        self.create_timestamp = userinfo.create_timestamp
        #print(self.create_timestamp)
        self.install_date = time.strftime('%Y-%m-%d', time.localtime(float(self.create_timestamp) /1000))
        #print(self.install_date)
        self.risk_grades = vpn["risk_grades"]
        self.app_num = vpn['app_num']
        self.app_channel = vpn["app_channel"]
        self.channel_name = vpn["channel_name"]
        self.sub_location_code = userinfo.location_code
        self.location_code = userinfo.location_code
        self.imei = userinfo.imei

    def create_string(self):
        temp = r'{"create":{"_index":"vpn","_type":"app_info"}}' + '\n' + r'{"user_id": "' + self.user_id + \
            r'","user_ip_address": "' + self.user_ip_address + r'","app_name": "' + self.app_name + \
            r'","app_type": ' + self.app_type + r',"app_package": "' + self.app_package + \
            r'","install_date": "' + self.install_date + r'","create_timestamp": ' + str(self.create_timestamp) + \
            r',"risk_grades": "' + self.risk_grades + r'","app_channel": "' + self.app_channel + \
            r'","app_num": "' + self.app_num + r'","channel_name":"' + self.channel_name + \
            r'","sub_location_code":"' + self.sub_location_code + r'","location_code":"' + self.location_code + \
            r'","imei":"' + self.imei + '"}\n'
        return  temp


class UsedVPN(object):
    def __init__(self, userinfo, appinfo, vpn):
        #安装VPN10分钟之后开始使用VPN
        self.start_time = appinfo.create_timestamp
        #上网时间1个小时
        self.end_time = self.start_time + 60*60*1000
        self.data_time = time.strftime('%Y-%m-%d',time.localtime(self.start_time/1000))
        #self.data_time = '2017-11-14'
        self.data_timestamp = self.start_time
        self.user_id = userinfo.user_id
        self.phone_location = userinfo.phone_location
        self.sub_locaiton_code = appinfo.sub_location_code
        self.location_code = appinfo.location_code
        self.sub_locaiton_name = self.phone_location
        self.location_name = self.phone_location
        self.vpn_name = appinfo.app_name
        self.vpn_package = appinfo.app_package
        self.vpn_num = appinfo.app_num
        #需要再次确认#####
        self.relation_id = 'a9b69dc3d1dc42fea85766d27902d6c9'
        self.total_flow = 120480000
        self.total_time = self.end_time - self.start_time
        self.user_ip_address = appinfo.user_ip_address
        self.user_location = userinfo.address
        self.user_points = "87.36,145.67"
        self.user_port = '80'
        self.vpn_channel = appinfo.channel_name
        self.vpn_country = '日本'
        self.vpn_country_code = 'Japan'
        self.vpn_ip_address = vpn["vpn_ip_address"]
        self.vpn_points = "139.73,35.71"
        self.vpn_port = '5000'

    def change_relation_id(self):
        all_char = 'abcdefjhijklmnopkqrstuvwxyz1234567'
        ran1 = random.randint(1, 20)
        ran2 = random.randint(1, 20)
        self.relation_id = self.relation_id.replace(self.relation_id[ran2], all_char[ran1])


    def create_string(self):
        temp = r'{"create":{"_index":"vpn","_type":"used_vpn"}}' + '\n' + \
        r'{"end_time":' + str(self.end_time) + r',"start_time":' + str(self.start_time) + \
            r',"data_time":"' + self.data_time + r'","data_timestamp":' + str(self.data_timestamp) + \
            r',"user_id":"' + self.user_id + r'","phone_location":"' + self.phone_location + \
            r'","sub_location_code":"' + self.sub_locaiton_code + r'","location_code":"' + self.location_code + \
            r'","sub_location_name":"' + self.sub_locaiton_name + r'","location_name":"' + self.location_name + \
            r'","vpn_name":"' + self.vpn_name + r'","vpn_package":"' + self.vpn_package + \
            r'","vpn_num":"' + self.vpn_num + r'","relation_id":"' + self.relation_id + \
            r'","total_flow":' + str(self.total_flow) + r',"total_time":' + str(self.total_time) + \
            r',"user_ip_address":"' + self.user_ip_address + r'","user_location":"' + self.user_location + \
            r'","user_points":"' + self.user_points + r'","user_port":"' + self.user_port + \
            r'","vpn_channel":"' + self.vpn_channel + r'","vpn_country":"' + self.vpn_country + \
            r'","vpn_country_code":"' + self.vpn_country_code + r'","vpn_ip_address":"' + self.vpn_ip_address + \
            r'","vpn_points":"' + self.vpn_points + r'","vpn_port":"' + self.vpn_port + r'"}' + '\n'

        return temp


class  Person(object):
    def __init__(self, userinfo, appinfo, n, vpn):
        self.userinfo = userinfo
        self.appinfo = appinfo
        self.usedvpn = UsedVPN(self.userinfo, self.appinfo, vpn)
        self.n = n
        # define two lists for app and used vpn to print
        self.total_appinfo = [self.appinfo, ]
        self.total_usedvpn = [self.usedvpn, ]

    # 根据传进来的数字，补全total_appinfo 和total_used_VPN
    def create_total(self):
        for x in range(1, self.n ):
            temp = copy.deepcopy(self.appinfo)
            temp.create_timestamp += x* ONEDAY
            temp.install_date = time.strftime('%Y-%m-%d',time.localtime(temp.create_timestamp/1000))
            # 需要随机获取一个VPN，并传入
            vpn=get_vpn(VPNS)

            temp.app_name = vpn['app_name']
            temp.app_type = vpn["app_type"]
            temp.risk_grades = vpn["risk_grades"]

            temp.app_num = vpn['app_num']
            temp.app_channel = vpn["app_channel"]
            temp.channel_name = vpn["channel_name"]
            temp.app_package = vpn['app_package']

            self.total_appinfo.append(temp)
            self.total_usedvpn.append(UsedVPN(self.userinfo, temp, vpn))

        for x in self.total_usedvpn:
            x.change_relation_id()


    def generate_string_userinfo(self):
        return  self.userinfo.create_string()


    def generate_string_appinfo(self):
        temp = ''
        n = 0
        while n <len(self.total_appinfo):
            temp = temp + self.total_appinfo[n].create_string()
            n = n +1
        return temp


    def generate_string_usedvpn(self):
        temp = ''
        n = 0
        while n <len(self.total_usedvpn):
            temp = temp + self.total_usedvpn[n].create_string()
            n = n +1
        return temp


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
                if filename == 'app_info.json':
                    es.index(index="vpn", doc_type="app_info", body=d)


if __name__ =='__main__':
    get_vpn(VPNS)