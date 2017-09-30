# -*- coding: UTF-8 -*-

import json
import os
import re
import sys
from datetime import datetime

from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest, AddDomainRecordRequest
from aliyunsdkcore import client
'''

下载
https://develop.aliyun.com/sdk/java?spm=5176.doc29772.416540.246.rjauTQ
解压安装
sudo python setup.py install
#安装alidns python DSK
pip install aliyun-python-sdk-alidns
https://help.aliyun.com/document_detail/29772.html?spm=5176.doc29774.6.612.oNWaU3

crontab -e
定时10分钟执行
*/10 * * * * /usr/bin/python2 /home/t7.py
crontab -l
先创建记下record id

'''
# 请填写你的Access Key ID
access_key_id = "yourid"

# 请填写你的Access Key Secret
access_Key_secret = "your"

# 请填写你的账号ID
account_id = "0000"

# 如果选择yes，则运行程序后仅现实域名信息，并不会更新记录，用于获取解析记录ID。
# 如果选择NO，则运行程序后不显示域名信息，仅更新记录
i_dont_know_record_id = 'no'

# 请填写你的一级域名
rc_domain = 'xxx.xxx'

# 请填写你的解析记录
rc_rr = 'www'

# 请填写你的记录类型，DDNS请填写A，表示A记录
rc_type = 'A'

# 请填写解析记录ID
rc_record_id = 'yourid '
rc_record_RequestId = 'D4'
# 请填写解析有效生存时间TTL，单位：秒
rc_ttl = '600'

# 请填写返还内容格式，json，xml
rc_format = 'json'


def my_ip():
    get_ip_method = os.popen('curl -s ip.cn')
    get_ip_responses = get_ip_method.readlines()[0]
    get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    get_ip_value = get_ip_pattern.findall(get_ip_responses)[0]
    return get_ip_value


def check_records(dns_domain):
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format(rc_format)
    result = clt.do_action(request)
    print result
    return result


def old_ip():
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    #print result, "-------"
    request.set_RecordId(rc_record_id)
    request.set_accept_format(rc_format)
    #print result, "-------"
    result = clt.do_action(request)
    #print result, "-------"
    result = json.JSONDecoder().decode(result)
    print result
    result = result['Value']
    return result


def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    print dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(dns_ttl)
    request.set_accept_format(dns_format)
    print request,"---"
    result = clt.do_action(request)
    print result
    return result

def create_dns(rc_domain, dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_DomainName(rc_domain)
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    #request.set_RecordId(dns_record_id)
    #request.set_TTL(dns_ttl)
    #request.set_accept_format(dns_format)
    print request
    result = clt.do_action(request)
    print result
    result = json.JSONDecoder().decode(result)
    print result
    print result['RequestId'], result['RecordId']
    return result

def write_to_file():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #current_script_path = sys.argv[0]
    #print current_script_path
    # 绝对路径获取
    current_script_path = os.path.abspath(sys.argv[0])
    current_script_path = os.path.dirname(current_script_path)
    log_file = current_script_path + '/' + 'aliyun_ddns_log.txt'
    #print log_file
    write = open(log_file, 'a')
    write.write(time_now + ' ' + str(rc_value)  + ' ' + str(rc_record_id)+ '\n')
    write.close()
    return


if __name__ == '__main__':
    current_script_path = sys.argv[0]
    print current_script_path,"---"
    rc_value = my_ip()
    print rc_value
    #create_dns(rc_domain, rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format)

    rc_value_old = old_ip()
    print rc_value, rc_value_old

    if i_dont_know_record_id == 'yes':
        check_records(rc_domain)
    elif i_dont_know_record_id == 'no':
        #rc_value ='58.100.92.135'
        if rc_value_old == rc_value:
            print 'The specified value of parameter Value is the same as old'
        else:
            update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format)
            write_to_file()
