__author__ = 'yanghongsheng-lt'
#-*- coding:utf-8 -*-
#加载webdriver模块S
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time
import MySQLdb
import sys,os
#获取排名前n 的数据
ip ='192.168.1.2'
blocktime1 = '1day'
blocktime ='10min'
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

driver.implicitly_wait(5)
now_handle = driver.current_window_handle #获取当前窗口句柄
# click more info
try:
    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)
    driver.switch_to.frame('leftframe')
    elem = driver.find_element_by_id("user")
    elem.click()
    elem = driver.find_element_by_id("blacklist").click()
    logging.info('Frist Switch  to leftframe frame and click user and status')
except:
    logging.warning('can not find  leftframe,quit!')
    print 'None'
    driver.quit()
    sys.exit()









try:
    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)
    driver.switch_to.frame('cmd')
    elem = driver.find_elements_by_id("tabs")
    elem[1].click()


    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)
    driver.switch_to.frame('cnt')
    # open block ip windows
    elem = driver.find_element_by_id("b_addnew32").click()

    #eum_blacklist_manual_name   block ip
    elem = driver.find_element_by_id("eum_blacklist_manual_name")
    elem.send_keys(ip)

    # choice time
    if blocktime[-3:] == 'day':
        driver.find_element_by_id("c2").click()
    elif blocktime[-3:] == 'min':
        driver.find_element_by_id("c1").click()
    #input time
    elem = driver.find_element_by_id("punitive_time")
    s = blocktime.split(blocktime[-3:])[0]
    print s
    elem.clear()
    elem.send_keys(s)
    #yingyong config(setting)
    driver.find_element_by_id("setting").click()

    logging.info('Frist Switch  to cmd  frame and click userblock')
except:
    logging.warning('can not find  cmd,quit!')
    print 'None'
    driver.quit()
    sys.exit()


driver.implicitly_wait(5)
driver.switch_to.window(now_handle)



time.sleep(30)

driver.quit()
