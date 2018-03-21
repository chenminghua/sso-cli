#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import io
import sys
import argparse
import demjson

import requests
from bs4 import BeautifulSoup, Comment

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

SESSION = requests.Session()

USER_DICT = {}

VERSION = "VERSION 0.0.1"


def getUsers():
    #login
    loginUrl = 'http://10.3.12.30:8880/sso/admin'
    username = 'admin'
    password = '****'
    #登录时需要POST的数据
    data = {'username':username, 
            'password':password}
    SESSION.post(loginUrl, data = data)

    #find users
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

    #登录后才能访问的网页
    url = 'http://10.3.12.30:8880/sso/adminUser/userList'

    #设置请求头
    #在发送get请求时带上请求头和cookies
    resp = SESSION.get(url, headers = HEADERS)     
    respHtml = resp.content.decode('utf-8')
    #print(respHtml)
    soup = BeautifulSoup(respHtml, 'html.parser')
    #print (soup.find_all("tr", class_="gradeA"))

    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            USER_DICT[tds[2].contents[0]] = {
                'id': tds[0].contents[0],
                'name': tds[1].contents[0],
                'email': tds[2].contents[0],
                'status': tds[3].label.string,
            }

#添加用户
def addUser(email, name):
    if not email or not name:
        print ("请输入员工姓名以及邮箱！")
        return
    
    userId = USER_DICT[email]['id']
    resetUrl = 'http://10.3.12.30:8880/sso/adminUser/resetPassWD/' + userId
    restPwdResp = SESSION.get(resetUrl, headers = HEADERS)

    jo = demjson.decode(restPwdResp.text)
    result = jo['success']
    if result == 'true':
        print ('Done...')
    else:
        print ('Ohh, something wrong, please go to website to check it!')
    return

#重置用户密码
def resetPassWd(email):
    getUsers()
    if not email:
        print ("请输入email，员工姓名可能存在重复！")
        return
    
    userId = USER_DICT[email]['id']
    resetUrl = 'http://10.3.12.30:8880/sso/adminUser/resetPassWD/' + userId
    restPwdResp = SESSION.get(resetUrl, headers = HEADERS)

    jo = demjson.decode(restPwdResp.text)
    result = jo['success']
    if result == 'true':
        print ('Done...')
    else:
        print ('Ohh, something wrong, please go to website to check it!')
    return

#删除用户
def delUser(email):
    getUsers()
    if not email:
        print ("请输入email，员工姓名可能存在重复！")
        return
    
    userId = USER_DICT[email]['id']
    resetUrl = 'http://10.3.12.30:8880/sso/adminUser/setState/' + userId + '-1'
    restPwdResp = SESSION.get(resetUrl, headers = HEADERS)

    jo = demjson.decode(restPwdResp.text)
    result = jo['success']
    if result == 'true':
        print ('Done...！')
    else:
        print ('Ohh, something wrong, please go to website to check it!')
    return

#删除用户
def activeUser(email):
    getUsers()
    if not email:
        print ("请输入email，员工姓名可能存在重复！")
        return
    
    userId = USER_DICT[email]['id']
    resetUrl = 'http://10.3.12.30:8880/sso/adminUser/setState/' + userId + '-0'
    restPwdResp = SESSION.get(resetUrl, headers = HEADERS)

    jo = demjson.decode(restPwdResp.text)
    result = jo['success']
    if result == 'true':
        print ('Done...！')
    else:
        print ('Ohh, something wrong, please go to website to check it!')
    return

#查找用户
def findUser(email):
    getUsers()
    if not email:
        print ("请至少输入查询条件！")
        return    
    try:
        user = USER_DICT[email]
        print("姓名:", user['name'])
        print("邮箱:", user['email'])
        print("状态:", user['status'])
    except Exception:
        print ("未找到该邮箱，请确认邮箱是否正确！")
    return

def get_parser():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='SSCTV SSO CLI Tools.')
    parser.add_argument('-s', '--search', action='store_true',
                        help='search user by email.')
    parser.add_argument('-r', '--reset', action='store_true',
                        help='reset user sso password')
    parser.add_argument('-a', '--add', action='store_true',
                        help='add sso user')
    parser.add_argument('-d', '--del',  action='store_true',
                        help='delete user by email')
    parser.add_argument('-b', '--back',  action='store_true',
                        help='bring back user by email')
    parser.add_argument('-e', '--email', type=str,
                        help='user email.')
    parser.add_argument('-n', '--name', type=str,
                        help='user name.')
    parser.add_argument('-v', '--version', action='store_true',
                        help='version information.')
    return parser    

def command_line_runner():
    """ 执行命令行操作
    """
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)
        return

    if not args["email"] and not args['name']:
        parser.print_help()
    else:
        if args['search']:
            findUser(args['email'])
        elif args['reset']:
            resetPassWd(args['email'])
        elif args['add']:
            addUser(args['email'], args['name'])
        elif args['del']:
            delUser(args['email'])
        elif args['back']:
            activeUser(args['email'])
if __name__ == "__main__":
    command_line_runner()
