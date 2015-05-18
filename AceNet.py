__author__ = 'yanghongsheng-lt'
#coding:utf-8
#加载webdriver模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time
import MySQLdb
import sys,os
#获取排名前n 的数据
n =10
iedriver = os.getcwd() + '\\IEDriverServer.exe'
os.environ["webdriver.ie.driver"] = iedriver
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='Acenet.log',
                filemode='w')

#logging.debug('This is debug message')
#logging.info('This is info message')
#logging.warning('This is warning message')

#b.pop()
try:
  con = MySQLdb.connect(host='192.168.65.202',user='python',passwd='python',db='IT')
except Exception, e:
  print e
  logging.warning('Mysql connect Error')
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
        sql = "insert into %s(ip, flow, paixu,flowtime) values ('%s', %d, %d,NOW())" % (table,j[0], c, n)
        try:
            cur.execute(sql)
        except Exception, e:
            print 'insert database Error'

def inser_total_data(table,data):
    b = data.split(';')
    b.pop()
    n = 0
    for i in b:
        n = n+1
        j =i.split(",")
        if j[1][-2] == 'G':
            c=int(float(j[1][0:-2])*1024)
        else:
            c =int(float(j[1][0:-2]))
        sql = "insert into %s(ip, flow, paixu,flowtime) values ('%s', %d, %d,NOW())" % (table,j[0], c, n)
        try:
            cur.execute(sql)
        except Exception, e:
            print 'insert database Error'
#　　elem.send_keys(Keys.RETURN)
driver = webdriver.Ie()
#测试网址
driver.get("http://192.168.67.251:8080")

#input username and password
if driver.find_elements_by_id("username2"):
    #login
    elem = driver.find_elements_by_id("username2")
    elem[2].send_keys("root")
    elem = driver.find_elements_by_id("password2")
    elem[2].send_keys("tibco1234")
    elem = driver.find_elements_by_name("goto")
    elem[2].click()
    time.sleep(1)
    logging.info('User had login')
else:
    print "can not find  username elements!"
    logging.warning('can not find  username elements!,Quit!')
    driver.quit()

now_handle = driver.current_window_handle #获取当前窗口句柄
# click more info
time.sleep(2)
try:
    driver.switch_to.frame('cnt')
    elem = driver.find_elements_by_id("aaaera22")
    elem[1].click()
    logging.info('Frist Switch  to cnt frame')
except:
    logging.warning('can not find  cnt frame,quit!')
    print 'None'
    driver.quit()
    sys.exit()

# start data,input
cur = con.cursor()
driver.implicitly_wait(5)
driver.switch_to.window(now_handle)

try:
    driver.switch_to.frame('cnt')
    totaldata = driver.find_element_by_id("eum_last5_traffic_total").get_attribute("value")
    recvdata = driver.find_element_by_id("eum_last5_traffic_recv").get_attribute("value")
    senddata = driver.find_element_by_id("eum_last5_traffic_send").get_attribute("value")

    insertdata('flow_realtime_total',totaldata)
    insertdata('flow_realtime_recv',recvdata)
    insertdata('flow_realtime_send',senddata)
    print 'Insert realtime data OK'
    logging.info('Insert realtime  date OK!')
except Exception, e:
    logging.warning('driver.switch_to.frame(cnt ) have error! exit!')
    print e
    driver.quit()
    sys.exit()

driver.implicitly_wait(5)
driver.switch_to.window(now_handle)
try:
    driver.switch_to.frame('cmd')
    print 'swithch to cmd'
    elem = driver.find_elements_by_id("tabs")
    elem[1].click()
    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)
    driver.switch_to.frame('cnt')
    print 'switch to cnt'
    totaldata = driver.find_element_by_id("eum_ip_subscriber_online_today_total").get_attribute("value")
    recvdata = driver.find_element_by_id("eum_ip_subscriber_online_today_recv").get_attribute("value")
    senddata = driver.find_element_by_id("eum_ip_subscriber_online_today_send").get_attribute("value")

    inser_total_data('flow_total_total',totaldata)
    inser_total_data('flow_total_recv',recvdata)
    inser_total_data('flow_total_send',senddata)

    logging.info('Insert total  date OK!')
    print 'Insert total data  OK'
except Exception,e:
    print e
    logging.warning('driver.switch_to.frame(cmd) have error! exit!')
    driver.quit()
    sys.exit()

#end
cur.close()
con.close()
driver.quit()
