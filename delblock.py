__author__ = 'yanghongsheng-lt'
#-*- coding:utf-8 -*-
#加载webdriver模块S
from selenium import webdriver
import selenium
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






driver.implicitly_wait(5)
driver.switch_to.window(now_handle)
driver.switch_to.frame('cmd')
elem = driver.find_elements_by_id("tabs")
elem[1].click()


driver.implicitly_wait(5)
driver.switch_to.window(now_handle)
driver.switch_to.frame('cnt')

data =[]
for tr in driver.find_elements_by_xpath('//table[@id="table1"]//tr'):
        tds=tr.find_elements_by_tag_name('td')
        if tds:
            data.append([td.text for td in tds])

nu = 0
for i in data:
    if len(i) == 9 :
        nu=nu+1
        if i[1] == ip :
            # open block ip windowsu
            print nu
            elem = driver.find_elements_by_id("Unlock")
            elem[nu-2].click()
            break

print ip,nu
driver.switch_to.alert.accept()
# aalhandles=driver.window_handles#获取所有窗口句柄
# for handle in aalhandles:#在所有窗口中查找弹出窗口
#     if handle!=nowhandle:
#         driver.switch_to.window(handle)#这两步是在弹出窗口中进行的操作，证明我们确实进入了
#         driver.find_element_by_link_text("新闻").click()






try:


    logging.info('Frist Switch  to cmd  frame and click userblock')
except:
    logging.warning('can not find  cmd,quit!')
    print 'None'
    driver.quit()
    sys.exit()


driver.implicitly_wait(5)
driver.switch_to.window(now_handle)



time.sleep(3)

driver.quit()
