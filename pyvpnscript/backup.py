
import time
import copy
import random

#一天换算下来的毫秒数, 用户计算同一个用户每天用一次不同的VPN
ONEDAY = 24 * 60 * 60* 1000
#5分钟换算下来的毫秒数，
FIVEMIN = 5 * 60 * 1000


# 初始化数据，顶一个人有关的各项基本数据
one_person = {'user_id': '13988880001', 'user_name':'伊利亚',
              'address': '哈密地区', 'phone_location':'哈密地区',
              'app_type': 'true',
              'base_location':'哈密酒店', 'location_code':'652200',
              'user_ip_address':'124.118.12.1', 'app_name':'TurboVPN',
              'risk_grades': '1', 'app_channel':'dangbei market', 'channel_name':'当贝市场'
              }


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
        temp = ONEDAY * n
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


class AppInfo(object):
    def __init__(self, userinfo, user_ip_address, app_name, app_type, risk_grades, app_channel, channel_name):
        self.user_id = userinfo.user_id
        self.user_ip_address = user_ip_address
        self.app_name = app_name
        self.app_type = app_type
        self.app_package = self.app_name + '.proxy.com'

        #self.install_date = "2017-11-14"
        # 时间取用户第一次VPN上网前5分钟
        self.create_timestamp = userinfo.create_timestamp - 5*60*1000
        #print(self.create_timestamp)
        self.install_date = time.strftime('%Y-%m-%d', time.localtime(float(self.create_timestamp) /1000))
        #print(self.install_date)
        self.risk_grades = risk_grades
        self.app_num = '6.2'
        self.app_channel = app_channel
        self.channel_name = channel_name
        self.sub_location_code = userinfo.location_code
        self.location_code = userinfo.location_code
        self.imei = userinfo.imei

    def create_string(self):
        temp = r'{"create":{"_index":"vpn","_type":"app_info"}}' + '\n' + r'{"user_id": "' + self.user_id + \
            r'","user_ip_address": "' + self.user_ip_address + r'","app_name": "' + self.app_name + \
            r'","app_type": ' + self.app_type + r',"app_package": "' + self.app_package + \
            r'","install_date": "' + self.install_date + r'","create_timestamp":' + str(self.create_timestamp) + \
            r',"risk_grades": "' + self.risk_grades + r'","app_channel": "' + self.app_channel + \
            r'","app_num": "' + self.app_num + r'","channel_name":"' + self.channel_name + \
            r'","sub_location_code":"' + self.sub_location_code + r'","location_code":"' + self.location_code + \
            r'","imei":"' + self.imei + '"}\n'
        return  temp


class UsedVPN(object):
    def __init__(self, userinfo, appinfo):
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
        self.total_flow = 1204800000
        self.total_time = 60*60*1000
        self.user_ip_address = appinfo.user_ip_address
        self.user_location = userinfo.address
        self.user_points = "87.36,145.67"
        self.user_port = '80'
        self.vpn_channel = appinfo.channel_name
        self.vpn_country = '日本'
        self.vpn_country_code = 'Japan'
        self.vpn_ip_address = "160.16.230.28"
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


# 根据一个初始化数据，生成一个mydata对象, m 多少个VPN， n多少次访问记录
def init_mydata(person, n):
    my_userinfo = UserInfo(person['user_id'], person['user_name'], person['address'],
                       person['phone_location'], person['base_location'], person['location_code'])

    my_userinfo.correcttimestamp(n)

    my_appinfo = AppInfo(my_userinfo, person['user_ip_address'], person['app_name'], person['app_type'],
                        person['risk_grades'], person['app_channel'], person['channel_name'])


    return MyData(my_userinfo,my_appinfo, n )



class  MyData(object):
    def __init__(self, userinfo, appinfo, u_num):
        self.userinfo = userinfo
        self.appinfo = appinfo
        self.usedvpn = UsedVPN(self.userinfo, self.appinfo)
        self.u_num = u_num
        # define two lists for app and used vpn to print
        self.total_appinfo = [self.appinfo, ]
        self.total_usedvpn = [self.usedvpn, ]

    # 根据传进来的数字，补全total_appinfo 和total_used_VPN
    def create_total(self):
        for x in range(1, self.u_num +1):
            temp = copy.deepcopy(self.appinfo)
            temp.app_name = temp.app_name + ('%s' % x)
            temp.app_package = temp.app_package + ('%s' % x)
            temp.create_timestamp += x* ONEDAY
            temp.install_date = time.strftime('%Y-%m-%d',time.localtime(temp.create_timestamp/1000))
            #temp.install_date = '2017-11-14'
            #print(temp.app_num)
            #temp.app_num = str("%.1f" % (float(temp.app_num) + 0.1 * x))

            temp.app_num = str("%.1f" % (float(temp.app_num) + 0.1 * x))
            temp.channel_name = temp.channel_name + ('%s' % x)
            self.total_appinfo.append(temp)
            self.total_usedvpn.append(UsedVPN(self.userinfo, temp))
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

    def generate_string_used_vpn(self):
        temp = ''
        n = 0
        while n <len(self.total_usedvpn):
            temp = temp + self.total_usedvpn[n].create_string()
            n = n +1
        return temp



def write_to_file(userinfo, appinfo, usedvpn):
    with open ('d:\\userinfo_tmp.json', 'w', encoding='utf-8') as f:
        f.write(userinfo)

    with open('d:\\app_tmp.json', 'w', encoding='utf-8') as f:
        f.write(appinfo)

    with open('d:\\used_tmp.json', 'w', encoding='utf-8') as f:
        f.write(usedvpn)



#根据一个初始化数据，生成任意多个初始化数据
def gen_basic_data(n):
    pass


if __name__ == '__main__':
    data = init_mydata(one_person, 10)
    data.create_total()
    write_to_file(data.generate_string_userinfo(), data.generate_string_appinfo(), data.generate_string_used_vpn())




