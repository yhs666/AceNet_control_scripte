__author__ = 'yanghongsheng-lt'
#coding=utf-8

s = '1day'

import datetime
import MySQLdb

def gettime(s):
    try:
        b = s[-3:]
        d = int(s.split(b)[0])
        if b == 'min':
            t = datetime.datetime.now() + datetime.timedelta(minutes=d)
        elif b == 'day':
            t = datetime.datetime.now() + datetime.timedelta(days=d)
        t = "'" + t.strftime("%Y-%m-%d %H:%M:%S") + "'"
        return t
    except:

        return "0000-00-00 00:00:00"







con = MySQLdb.connect(host='192.168.65.202',user='python',passwd='python',db='IT')
if con:

    #获取连接的cursor，只有获取了cursor,才能进行操作
    cur = con.cursor()
    j = '192.168.1.1'
    t =gettime(s)


    # sql ="insert into %s(ip, status, type,createtime,endtime) \
    #                       values ('%s', 'block', 'total', NOW(), %s)" % ('flow_flowlog', j, gettime(s))
    # sql ="insert into %s(ip, status, type,createtime,endtime) \
    #       values ('%s', 'block', 'realtime',NOW(), %s)" % ('flow_logip', i, t)
    # cur.execute(sql)
    #
    # sql ="insert into %s(ip, name,remask,type,endtime,createtime) \
    #           values ('%s', 'auto', 'auto','unlock', %s, NOW())" % ('flow_safeip', j, t)
    # cur.execute(sql)
    safe_ip ='flow_safeip'
    s = ('192.168.65.201',)
    ip = str(s[0])

    sql ="update %s Set type ='done' where type = 'unlock' and ip = ' %s'" % (safe_ip, ip)

    print sql
    cur.execute(sql)
    # for r in results:
    #     print r
    #     rip = r[0].decode('utf-8')
    #     print rip
    #     if rip in realtime_block:
    #         realtime_block.remove(rip)
    #
    # print 'filter'
    # print realtime_block
    #cur.executemany(sql)
    #cur.execute(sql)

    cur.close()
    con.close()
else:
   print "Error"





