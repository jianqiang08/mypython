import time
import random


# 本函数返回一个距离当前时间10天内的任一时间（过去时间
def randomtime():
    # 取得当前时间
    millis = int(round(time.time() * 1000))
    # 十天总共这么多毫秒
    timerange = 24*60*60*100
    # 取得一个随机整数
    temp = random.randint(0,timerange)
    # 返回随机时间
    return millis - temp


def randomphonenumber():
    # 设定一个基准手机号
    basic = 13999999998
    # 取得一个随机变量
    temp = random.randint(0,99999998)
    # 返回一个随机号码
    return basic - temp


def randomlocation():
    #设定位置基准
    locationlist = ["乌鲁木齐市", "克拉玛依市", "吐鲁番地区", "哈密地区", "昌吉回族[自]", "博尔塔拉蒙古[自]",
            "巴音郭楞蒙古[自]", "阿克苏地区", "克孜勒苏柯尔克孜[自]", "喀什地区", "和田地区",
            "伊犁哈萨克[自]", "塔城地区", "阿勒泰地区", "石河子市"]
    # 取得随机下标
    temp = random.randint(0, locationlist.__len__())
    # 返回随机位置
    return locationlist[temp]


if __name__ == "__main__":
    dbtable = r'{"create":{"_index":"vpn","_type":"user_imei_increase"}}'
    finalstring = ''

    for x in range(10):
        finalstring = finalstring + dbtable + '\n' + r'{"user_id":"' + str(randomphonenumber()) + '"' +\
                      r',"imei":"' + "SN" + str(randomphonenumber()) + r'","create_timestamp":' +\
                      str(randomtime()) + "}" + '\n'

    f = open('/tmp/pythonimei.json', 'w')
    f.write(finalstring)
    f.close()







