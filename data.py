# coding=utf-8
__author__ = 'yanghongsheng-lt'


import MySQLdb

a="192.168.66.34,3.42Mb/s,100;192.168.67.87,1.96Mb/s,57;192.168.66.86,1.64Mb/s,47;192.168.75.20,1.43Mb/s,41;192.168.66.129,986Kb/s,28;192.168.76.175,817Kb/s,23;192.168.68.76,647Kb/s,18;192.168.69.88,530Kb/s,15;192.168.74.42,519Kb/s,15;192.168.66.118,414Kb/s,12;192.168.66.38,404Kb/s,11;192.168.74.53,352Kb/s,10;192.168.68.24,330Kb/s,9;192.168.67.71,298Kb/s,8;192.168.69.38,259Kb/s,7;192.168.67.123,245Kb/s,7;192.168.67.51,244Kb/s,7;192.168.69.27,243Kb/s,7;192.168.67.81,230Kb/s,6;192.168.66.91,225Kb/s,6;192.168.67.92,210Kb/s,6;192.168.66.25,193Kb/s,5;192.168.69.56,186Kb/s,5;192.168.69.55,172Kb/s,5;192.168.74.160,168Kb/s,4;192.168.68.64,161Kb/s,4;192.168.69.44,153Kb/s,4;192.168.67.39,150Kb/s,4;192.168.69.30,149Kb/s,4;192.168.76.113,149Kb/s,4;192.168.69.22,144Kb/s,4;192.168.74.124,140Kb/s,4;192.168.76.180,139Kb/s,4;192.168.74.52,134Kb/s,3;192.168.68.37,134Kb/s,3;192.168.74.41,131Kb/s,3;192.168.74.55,131Kb/s,3;192.168.68.56,131Kb/s,3;192.168.74.72,131Kb/s,3;192.168.74.29,130Kb/s,3;192.168.66.30,124Kb/s,3;192.168.66.87,123Kb/s,3;192.168.69.24,117Kb/s,3;192.168.68.80,116Kb/s,3;192.168.69.28,109Kb/s,3;192.168.67.61,106Kb/s,3;192.168.68.62,102Kb/s,2;192.168.67.24,102Kb/s,2;192.168.68.36,100Kb/s,2;192.168.69.32,99Kb/s,2;192.168.68.34,96Kb/s,2;192.168.65.9,96Kb/s,2;192.168.66.145,94Kb/s,2;192.168.66.56,91Kb/s,2;192.168.76.21,88Kb/s,2;192.168.67.36,87Kb/s,2;192.168.67.25,87Kb/s,2;192.168.74.38,87Kb/s,2;192.168.66.102,81Kb/s,2;192.168.69.43,80Kb/s,2;192.168.66.112,80Kb/s,2;192.168.74.95,77Kb/s,2;192.168.69.79,76Kb/s,2;192.168.68.49,75Kb/s,2;192.168.67.98,74Kb/s,2;192.168.69.49,74Kb/s,2;192.168.67.80,73Kb/s,2;192.168.67.74,73Kb/s,2;192.168.67.40,70Kb/s,2;192.168.69.47,65Kb/s,1;192.168.66.51,63Kb/s,1;192.168.67.59,63Kb/s,1;192.168.67.49,61Kb/s,1;192.168.74.56,61Kb/s,1;192.168.67.52,60Kb/s,1;192.168.66.81,58Kb/s,1;192.168.67.46,55Kb/s,1;192.168.74.84,54Kb/s,1;192.168.66.111,54Kb/s,1;192.168.68.47,53Kb/s,1;192.168.74.36,51Kb/s,1;192.168.68.35,50Kb/s,1;192.168.67.43,47Kb/s,1;192.168.69.21,47Kb/s,1;192.168.71.200,43Kb/s,1;192.168.74.49,42Kb/s,1;192.168.66.41,41Kb/s,1;192.168.74.27,41Kb/s,1;192.168.69.20,40Kb/s,1;192.168.67.21,39Kb/s,1;192.168.74.30,39Kb/s,1;192.168.76.167,38Kb/s,1;192.168.68.39,36Kb/s,1;192.168.65.5,35Kb/s,1;192.168.71.120,33Kb/s,1;192.168.74.77,33Kb/s,1;192.168.66.60,33Kb/s,1;192.168.74.44,33Kb/s,1;192.168.76.69,31Kb/s,1;192.168.67.63,30Kb/s,1;"


n_table= 'flow'
try:
  con = MySQLdb.connect(host='192.168.65.202',user='python',passwd='python',db='IT')
except Exception, e:
  print e
  sys.exit()
def insertdata(table,data):
    b = data.split(';')
    b.pop()
    n = 0
    for i in b:
        n = n+1
        j =i.split(",")
        if j[1][-4] == 'M':
            c=int(float(j[1][0:-4])*1000)
        else:
            c =int(j[1][0:-4])
        #sql = "insert into flow(ip, flow, paixu) values (%s, %d, %d,)"
        print table,j[0],c,n
        sql = "insert into %s(ip, flow, paixu) values ('%s', %d, %d)" % (table,j[0], c, n)
        print sql
        cur.execute(sql)
        try:
            #cur.executemany(sql)
            cur.execute(sql)
        except Exception, e:
            print 'insert database Error'

if con:

    #获取连接的cursor，只有获取了cursor,才能进行操作
    cur = con.cursor()
    insertdata('flow_realtime_recv',a)
    #conn.commit()
    cur.close()
    con.close()
else:
   print "Error"