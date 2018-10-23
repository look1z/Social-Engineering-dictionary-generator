# -*- coding: UTF-8 -*-
# by look1z

import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "hn:b:c:m:d:p:N:")

# 默认参数
name = None
birthday = None
IDC = None
mail = None
domain = None
phone_number = None
qq_number = None
name_ab = None

# help菜单
def usage():
    print ("help")

for options, value in opts:
    # help菜单
    if options == "-h":
        usage()
        sys.exit()

    # 姓名 -n (每个字之间用“.”分开)li.ming   wang.yu.chen
    elif options == "-n":
        name = value

    # 生日 -b 如19941016
    elif options == "-b":
        if len(value) == 8:
            birthday = value
        else:
            raise RuntimeError('the len of birthday is not 8')

    # 身份证 -c
    elif options == "-c":
        if len(value) == 18:
            IDC = value
        else:
            raise RuntimeError('the len of birthday is not 18')

    # 邮箱 -m xxxx@xx.com
    elif options == "-m":
        mail = value

    # 域名 如www.baidu.com
    elif options == "-d":
        domain = value

    # 手机号 如13933893931
    elif options == "-p":
        phone_number = str(value)

    # qq号 -q 如381769096
    elif options == "-q":
        qq_number = value

    # 目标常用id 如look1z
    elif options == "-i":
        id = value

    # # 省
    # elif options == "-":
    #     province = value
    #
    # # 城市
    # elif options == "-":
    #     city = value

    # 企业名(中文，中文简称，英文，英文简称)


number_value_1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

number_value_2 = ["00", "01", "02", "03", "04", "05", "06", "07",
                  "10", "11", "12", "13", "20", "22", "30", "33",
                  "08", "09", "40", "44", "50", "55", "60",
                  "66", "70", "77", "80", "88", "90", "99"]

number_value_3 = ["000", "001", "101", "110", "111", "121", "123",
                  "212", "222", "250", "333", "444", "520", "555",
                  "666", "777", "888", "999"]

number_value_4 = ["000000", "111111", "110120", "123321",
                  "123456", "123123",
                  "222222", "333333", "666666", "654321",
                  "888888", "999999", "1314",   "5201314",
                  "123456789", "123123123", "666666666",
                  "888888888", "999999999", "000000000"]


weak_password = [ "a", "qwerty", "qwert", "ab", "abc", "qazwsx",
                 "1q2w3e4r", "abcd", "qwer", "qwe",
                 "aa", "woaini", "asdf", "iloveyou",
                 "zxc", ]

if name:
    name_a = ''
    name_list = name.split('.') # 字 列表
    for i in name_list:
        name_a += i[0] # 简称
    name_ab = [name_a, name_list[0]]
    name = name.replace('.', '')
    print name_list,name_ab


# 通过身份证号提取生日
if IDC and (birthday is None):
    birthday = IDC[6:14]

if birthday:
    birthday_list = [birthday, birthday[0:4], birthday[2:], birthday[4:]]

if domain:
    # www.baidu.com www.xxxx.edu.cn
    domain_split = domain.split('.')
    if len(domain_split) < 4:
        domain_list = [domain, domain_split[1], domain_split[1]+'.'+domain_split[2],
                       domain_split[0]+domain_split[1]+domain_split[2],
                       domain_split[1]+domain_split[2]]
    elif len(domain_split) == 4:
        domain_list = [domain, domain_split[1], domain_split[1] + '.' + domain_split[2] + '.' + domain_split[3],
                       domain_split[0] + domain_split[1] + domain_split[2]+ domain_split[3],
                       domain_split[1] + domain_split[2] + domain_split[3]]
    else:
        raise RuntimeError('domain is right?')


def write_dict(dict_list, file_name):
    # 写入接口
    with open(file_name,"ab+") as f:
        for i in dict_list:
            # 过滤掉过段的口令
            if len(i) > 5:
                f.write(i+'\n')


def name_and_weak(name,name_ab):
    # 姓名与弱口令字段、常用数字组合
    dict_list = list()
    dict_list.append(name)
    for weak in weak_password:
        dict_list.append(name + weak)
        for i in name_ab:
            dict_list.append(i + weak)

    for number in number_value_1:
        dict_list.append(name + number)

    for number in number_value_2:
        dict_list.append(name + number)

    for number in number_value_3:
        dict_list.append(name + number)

    for number in number_value_4:
        for i in name_ab:
            dict_list.append(i + number)

    write_dict(dict_list=dict_list, file_name=filename)


def birthday_and_weak(birthday):
    # 生日与弱口令字段组合
    dict_list = list()
    # 几种常见的生日组合
    dict_list.append([birthday, birthday[2:], birthday[4:]+birthday[:4]])
    for birth in birthday:
        for weak in weak_password:
            dict_list.append(birth + weak)
            dict_list.append(weak + birth)

    write_dict(dict_list=dict_list, file_name=filename)


def name_and_birthday(name, name_ab, birthday):
    # 名称与生日组合
    dict_list = list()
    for birth in birthday:
        # 全称+生日
        dict_list.append(name + birth)
        # 简称+生日
        for i in name_ab:
            dict_list.append(i + birth)

        for weak in weak_password:

            # 简称与生日与弱口令
            for i in name_ab:
                dict_list.append(i + birth + weak)

    write_dict(dict_list=dict_list, file_name=filename)


def IDC_and_weak(idc_number):
    dict_list = list()
    dict_list.append([idc_number[12:], idc_number, ])
    write_dict(dict_list=dict_list, file_name=filename)


def IDC_and_name(idc_number, name, name_ab):
    # 身份证与名称组合
    dict_list = list()
    dict_list.append([name+idc_number[14:], idc_number[14:]+name])
    for i in name_ab:
        dict_list.append([idc_number[14:]+i, i+idc_number[14:]])

    write_dict(dict_list=dict_list, file_name=filename)


def phone_number_and_weak(phone_number):
    # 手机号与弱口令组合
    dict_list = list()
    dict_list.append([phone_number, phone_number[3:], ])
    for i in weak_password:
        dict_list.append(phone_number+i)
        dict_list.append(phone_number[7:]+i)
    write_dict(dict_list=dict_list, file_name=filename)


def phone_number_and_name(phone_number, name, name_ab):
    # 手机号与名称组合
    dict_list = list()
    phone_number_list = [phone_number, phone_number[7:], phone_number[3:]]
    for i in phone_number_list:
        dict_list.append([i+name, name+i])
        for j in name_ab:
            dict_list.append([i + j, j + i])

    write_dict(dict_list=dict_list, file_name=filename)



if __name__ == "__main__":

    print name,birthday,mail,IDC,domain,number_value_2, name_ab

    filename = raw_input('file=')
    if name:
        name_and_weak(name=name, name_ab=name_ab)
    if birthday:
        birthday_and_weak(birthday)
        if name:
            name_and_birthday(name=name, name_ab=name_ab, birthday=birthday_list)
    if IDC:
        IDC_and_weak(idc_number=IDC)
        if name:
            IDC_and_name(idc_number=IDC, name=name, name_ab=name_ab)

    if phone_number:
        phone_number_and_weak(phone_number)
        if name:
            phone_number_and_name(phone_number,name,name_ab)







