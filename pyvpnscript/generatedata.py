
import time
import copy
from dbtypes import UserInfo, AppInfo, Person, get_vpn, VPNS, insert_data
import  os


# 初始化数据，手工设定一个人有关的各项基本数据
one_person = {'user_id': '13997880001', 'user_name':'伊利亚',
              'address': '哈密地区', 'phone_location':'哈密地区',
              'base_location':'哈密酒店', 'location_code':'652200',
              'user_ip_address':'124.118.12.1'}


# 存储区域内VPN上网用户的访问记录和APP 信息，用于进一步生成字符串
location_datas = []

# 设定一个地区使用VPN的人数， m代表人数， n代表一个人的访问次数
def init_for_location(one_person, m=1, n=1):
    location_persons = []
    location_persons.append(one_person)
    for x in range(1, m):
        temp = copy.deepcopy(one_person)
        temp['user_id'] = str(int(temp['user_id']) + x )
        temp['user_name'] = temp['user_name'] + ('%s' % x)
        location_persons.append(temp)

    for person in location_persons:
        temp = init_data(person, n)
        temp.create_total()
        location_datas.append(temp)
        # 不同人员的访问时间错开0.1秒，可以修改代码让不同的人的时间不同
        time.sleep(0.1)

#print(location_mydatas)

# 根据已知初始化数据，生成一个mydata对象, 每天使用一次不同的VPN访问网络， n代表使用天数。
def init_data(person, n=1):
    my_userinfo = UserInfo(person['user_id'], person['user_name'], person['address'],
                        person['phone_location'], person['base_location'], person['location_code'])

    my_userinfo.correcttimestamp(n)
    vpn =get_vpn(VPNS)

    my_appinfo = AppInfo(my_userinfo, person['user_ip_address'], vpn)

    return Person(my_userinfo, my_appinfo, n, vpn)



def write_to_file(userinfo, appinfo, usedvpn):
    with open ('user_info.json', 'w', encoding='utf-8') as f:
        f.write(userinfo)

    with open('app_info.json', 'w', encoding='utf-8') as f:
        f.write(appinfo)

    with open('used_vpn.json', 'w', encoding='utf-8') as f:
        f.write(usedvpn)


if __name__ == '__main__':
    init_for_location(one_person, 20, 10)
    userinfo=appinfo=usedvpn =''
    for x in location_datas:
        userinfo = userinfo + x.generate_string_userinfo()
        appinfo = appinfo + x.generate_string_appinfo()
        usedvpn = usedvpn + x.generate_string_usedvpn()

    write_to_file(userinfo, appinfo, usedvpn)

    insert_data('user_info.json')
    insert_data('app_info.json')
    insert_data('used_vpn.json')

