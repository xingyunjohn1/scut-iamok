#!/usr/bin/python3
# crontab expression:
# 0 9-10 * * * /usr/bin/python3 /root/iamok/autok.py >> /tmp/iamok.log 2>&1

from Des import *
import requests
import urllib
from bs4 import BeautifulSoup
import json,sys,time

username = ""
password = ""

def logger(log):
	print (time.strftime("[%Y-%m-%d %H:%M:%S]: ", time.localtime()) + log)

def strenc(data, firstkey, secondkey, thirdkey):
	bts_data = extend_to_16bits(data)  # 将data长度扩展成64位的倍数
	bts_firstkey = extend_to_16bits(firstkey)  # 将 first_key 长度扩展成64位的倍数
	bts_secondkey = extend_to_16bits(secondkey)  # 将 second_key 长度扩展成64位的倍数
	bts_thirdkey = extend_to_16bits(thirdkey)
	i = 0
	bts_result = []
	while i < len(bts_data):
		bts_temp = bts_data[i:i + 8]  # 将data分成每64位一段，分段加密
		j, k, l = 0, 0, 0
		while j < len(bts_firstkey):
			des_k = des(bts_firstkey[j: j + 8], ECB)  # 分别取出 first_key 的64位作为密钥
			bts_temp = list(des_k.encrypt(bts_temp))
			j += 8
		while k < len(bts_secondkey):
			des_k = des(bts_secondkey[k:k + 8], ECB)  # 分别取出 second_key 的64位作为密钥
			bts_temp = list(des_k.encrypt(bts_temp))
			k += 8
		while l < len(bts_thirdkey):
			des_k = des(bts_thirdkey[l:l+8], ECB)
			bts_temp = list(des_k.encrypt(bts_temp))
			l += 8
		bts_result.extend(bts_temp)
		i += 8
	str_result = ''
	for each in bts_result:
		str_result += '%02X' % each  # 分别加密data的各段，串联成字符串
	return str_result

def extend_to_16bits(data):  # 将字符串的每个字符前插入 0，变成16位，并在后面补0，使其长度是64位整数倍
	bts = data.encode()
	filled_bts = []
	for each in bts:
		filled_bts.extend([0, each])  # 每个字符前插入 0
	while len(filled_bts) % 8 != 0:  # 长度扩展到8的倍数
		filled_bts.append(0)  # 不是8的倍数，后面添加0，便于DES加密时分组
	return filled_bts

headers = {
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

post_data = {
    "rsa": "",
    "ul": "",
    "pl": "",
    "lt": "",
    "execution": "",
    "_eventId": "submit"
}

if len(username) == 0 or len(password) == 0:
	print ("please specify username and password!")
	sys.exit(1)

s = requests.session()
s.headers.update(headers)
req = s.get("https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fiamok.scut.edu.cn%2Fcas%2Flogin")
soup = BeautifulSoup(req.text,'lxml')

lt = soup.find(id='loginForm').find_all('input')[6].attrs['value']
post_data['ul'] = len(username)
post_data['pl'] = len(password)
post_data['lt'] = lt
post_data['rsa'] = strenc(username + password + lt ,'1','2','3')
post_data['execution'] = soup.find(id='loginForm').find_all('input')[7].attrs['value']

req = s.post("https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fiamok.scut.edu.cn%2Fcas%2Flogin", data=post_data)
req = s.get("https://enroll.scut.edu.cn/door/health/h5/get")

req_json = json.loads(req.text)
download_json = req_json['data']['healthRptInfor']['updateSql']
format_json = "{\"" + download_json.replace("=", "\": \"").replace("\"'", "\"").replace(",", "\",\"").replace("'\",", "\",").replace("'", "\"") + "}"
format_dic = json.loads(format_json)
#print(format_dic)
del format_dic['sCollegeCode']
format_dic['sDegreeCode'] = '本科生'
format_dic['iSex'] = '男'
del format_dic['sDegreeName']
del format_dic['sCampusCode']
del format_dic['sMajorCode']
del format_dic['sClassCode']
del format_dic['iFromType']

try:
	del format_dic['iRctKeyLeave']
except:
	print("?KeyError: 'iRctKeyLeave'")
try:
	del format_dic['iRctOutLeave']
except:
	print("?KeyError: 'iRctOutLeave'")

del format_dic['dRptTime']
format_dic['dRptDate'] = time.strftime("%Y-%m-%d", time.localtime())
dVaccin1Date = format_dic['dVaccin1Date']
dVaccin2Date = format_dic['dVaccin2Date']
format_dic['sPersonCode'] = username
format_dic['iRptState'] = 0

list = ['dRptDate',
'sPersonName',
'sPersonCode',
'sPhone',
'sParentPhone',
'iIsGangAoTai',
'iIsOversea',
'sHomeProvName',
'sHomeProvCode',
'sHomeCityName',
'sHomeCityCode',
'sHomeCountyName',
'sHomeCountyCode',
'sHomeAddr',
'iSelfState',
'iFamilyState',
'sNowProvName',
'sNowProvCode',
'sNowCityName',
'sNowCityCode',
'sNowCountyName',
'sNowCountyCode',
'sNowAddr',
'iNowGoRisks',
'iRctRisks',
'iRctKey',
'iRctOut',
'iRctTouchKeyMan',
'iRctTouchBackMan',
'iRctTouchDoubtMan',
'iVaccinState',
'iHealthCodeState',
'iRptState',
'sVaccinFactoryName',
'sVaccinFactoryCode',
'iVaccinType',
'dVaccin1Date',
'sDegreeCode',
'iSex',
'sCollegeName',
'sCampusName',
'sDormBuild',
'sDormRoom',
'sMajorName',
'sClassName',
'iInSchool',
'dVaccin2Date']

upload_data = ''
for key in list:
	format_dic[key] = urllib.parse.quote(str(format_dic[key]))
	if format_dic[key] == "dRptDate":
		format_dic[key] = time.strftime("%Y-%m-%d", time.localtime())
	elif format_dic[key] == "dVaccin1Date":
		format_dic[key] = dVaccin1Date
	elif format_dic[key] == "dVaccin2Date":
		format_dic[key] == dVaccin2Date
	upload_data = "{}&{}={}".format(upload_data, key, format_dic[key])

if req_json['code'] == 1:
	req = s.post("https://enroll.scut.edu.cn/door/health/h5/add?{}".format(upload_data[1:]))
	req_json = json.loads(req.text)
	if req_json['code'] == 1:
		logger ("iamok!")
	else:
		logger (req.text)
		logger ("submitRecordPerDay error!")
else:
	logger (req.text)
	logger ("getRecordPerDay error!")

