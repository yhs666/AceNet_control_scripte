__author__ = 'yanghongsheng-lt'
#-*- coding: utf-8 -*-
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time
import MySQLdb
import sys,os

config = ConfigParser.ConfigParser()
#config.readfp(open(raw_input("Input file name : "),"rb"))
path = os.path.abspath(os.path.dirname(sys.argv[0]))
fi = path + '\\config'
config.readfp(open(fi,"rb"))

# get config to var
acenet_url = config.get('acenet','url')
acenet_user = config.get('acenet','username')
acenet_pass =  config.get('acenet','password')
db_ip = config.get('database','ip')
db_user = config.get('database','username')
db_pass = config.get('database','password')
db_db = config.get('database','db')

#get db table name
realtime_total = config.get('table','realtime_total')
realtime_recv = config.get('table','realtime_recv')
realtime_send = config.get('table','realtime_send')

total_total = config.get('table','total_total')
total_recv = config.get('table','total_recv')
total_send = config.get('table','total_send')

blockip = config.get('table','blockip')
unlockip  = config.get('table','unlockip')

#limit
realtime_limit = config.get('limits','realtime')
total_limit  = config.get('limits','total')
# get block ip config

realtime = config.get('blockip','realtime')
total = config.get('blockip','total')

#
safe_ip = config.get('policy','safe_ip')
log_ip = config.get('policy','ip_log')
#define log file
log = path + '\\AceNet.log'
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=log,
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)

#iedriver config
iedriver = os.getcwd() + '\\IEDriverServer.exe'
os.environ["webdriver.ie.driver"] = iedriver


def login(driver,username,password):
    driver.implicitly_wait(7)
    try:

        elem = driver.find_elements_by_id("username2")
        elem[2].send_keys(username)
        elem = driver.find_elements_by_id("password2")
        elem[2].send_keys(password)
        elem = driver.find_elements_by_name("goto")
        elem[2].click()
        time.sleep(1)
        logging.info('User had login OK!')
        return driver.current_window_handle
    except:
        print "can not find  username and password elements!"
        logging.info('can not find  username elements!,Quit!')
        return  'ERROR'

def get_realtime_data(driver,now_handle):
    data = []
    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)
    try:
        driver.switch_to.frame('cnt')
        elem = driver.find_elements_by_id("aaaera22")
        elem[1].click()
        logging.info('Frist Switch  to cnt frame')
    except:
        logging.info('Switch  to cnt frame ERROR!')
        print 'Switch  to cnt frame ERROR'
        return 'ERROR'

    driver.implicitly_wait(5)
    driver.switch_to.window(now_handle)

    try:
        driver.switch_to.frame('cnt')
        data.append(driver.find_element_by_id("eum_last5_traffic_total").get_attribute("value"))
        data.append(driver.find_element_by_id("eum_last5_traffic_recv").get_attribute("value"))
        data.append(driver.find_element_by_id("eum_last5_traffic_send").get_attribute("value"))
        logging.info('Get realtime  date OK!')
        print 'Get Realtime data ok!'
        return data
    except Exception, e:
        logging.info('Get Realtime data Error!!')
        print  'Get Realtime data Error!'
        return 'ERROR'

def get_total_data(driver,now_handle):
    data = []
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
        data.append(driver.find_element_by_id("eum_ip_subscriber_online_today_total").get_attribute("value"))
        data.append(driver.find_element_by_id("eum_ip_subscriber_online_today_recv").get_attribute("value"))
        data.append(driver.find_element_by_id("eum_ip_subscriber_online_today_send").get_attribute("value"))

        logging.info('Get total Data OK!')
        print 'Get total data  OK'
        return  data
    except Exception,e:
        print e
        logging.warning('Get total Data Error!')
        return  'ERROR'


def insert_data(data,table1,table2,table3):
    try:
        db_table =[table1,table2,table3]
        for k in range(0,len(data)):
            b = data[k].split(';')
            b.pop()
            n = 0
            for i in b:
                n = n+1
                j =i.split(",")
                if j[1][-4] == 'M':
                    c=int(float(j[1][0:-4])*1000)
                elif j[1][-4] == 'K' :
                    c =int(j[1][0:-4])
                elif j[1][-2] == 'G':
                    c=int(float(j[1][0:-2])*1024)
                elif j[1][-2] == 'M':
                    c =int(float(j[1][0:-2]))
                sql = "insert into %s(ip, flow, paixu,flowtime) values ('%s', %d, %d,NOW())" % (db_table[k],j[0], c, n)
                try:
                    cur.execute(sql)
                except Exception, e:
                    print 'insert database Error'
        logging.info('Insert database OK!')
        print  'Insert database OK'
        return True
    except:
        return  False


def search_ip(data,limits):
    try:
        high_ip=[]
        limits =limits.split(':')
        for k in range(0,len(data)):
            if limits[k] =='0': continue
            b = data[k].split(';')
            b.pop()
            n = 0
            for i in b:
                n = n+1
                j =i.split(",")
                if j[1][-4] == 'M':
                    c=int(float(j[1][0:-4])*1000)
                elif j[1][-4] == 'K' :
                    continue
                elif j[1][-2] == 'G':
                    c=int(float(j[1][0:-2])*1024)
                elif j[1][-2] == 'M':
                    continue
                else:
                    continue
                if c > int(limits[k]):
                    high_ip.append(j[0])
        logging.info('find high flow ip  OK!')
        print  'find high flow ip  OK'
        return  high_ip
    except:
        logging.info('find high flow Have Error!')
        return  'ERROR'


#switch to add block ip page
def change_block(driver,now_handle):
    try:
        driver.implicitly_wait(5)
        driver.switch_to.window(now_handle)
        driver.switch_to.frame('leftframe')
        elem = driver.find_element_by_id("user")
        elem.click()
        elem = driver.find_element_by_id("blacklist").click()

        driver.implicitly_wait(5)
        driver.switch_to.window(now_handle)
        driver.switch_to.frame('cmd')
        elem = driver.find_elements_by_id("tabs")
        elem[1].click()
        logging.info('Change to block ip page OK!')

        return  True
    except:
        logging.info('Change_block funcation have Error!')
        print 'Change_block funcation have Error!'
        return False

# add block ip funcation
def add_blockip(driver,now_handle,ip,blocktime):
    try:
        driver.implicitly_wait(5)
        driver.switch_to.window(now_handle)
        driver.switch_to.frame('cnt')
        # open block ip windows
        driver.find_element_by_id("b_addnew32").click()
        elem = driver.find_element_by_id("eum_blacklist_manual_name")
        elem.send_keys(ip)

        # choice time
        if blocktime[-3:] == 'day':
            driver.find_element_by_id("c2").click()
        elif blocktime[-3:] == 'min':
            driver.find_element_by_id("c1").click()
        #input time
        elem = driver.find_element_by_id("punitive_time")
        s = blocktime[0:-3]
        print s
        elem.clear()
        elem.send_keys(s)
        #yingyong config(setting)
        driver.find_element_by_id("setting").click()

        driver.implicitly_wait(5)
        driver.switch_to.window(now_handle)
        driver.switch_to.frame('cmd')
        elem = driver.find_elements_by_id("tabs")
        elem[1].click()
        logging.info('Add block ip: %s   OK!' % ip)
        return  True
    except:
        logging.info('Add block ip: %s is ERROR' % ip)
        print 'add block ip: %s is ERROR' % ip
        return  False

def remove_blockip(driver,now_handle,ip):
    try:
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
        flg =0
        for i in data:
            if len(i) == 9 :
                nu=nu+1
                if i[1] == ip :
                    # open block ip windowsu
                    print 'Find %s in block list'% ip
                    elem = driver.find_elements_by_id("Unlock")
                    elem[nu-2].click()
                    driver.switch_to.alert.accept()
                    print 'Unlock %s in block list'% ip
                    flg = 1
                    break
        if flg == 1 :
            logging.info('Remove block ip: %s OK!' % ip)
            print 'Remove block ip: %s OK!' % ip
            return 'find'
        else:
            logging.info('Can not find  unlock ip: %s OK!' % ip)
            print 'Can not find  unlock ip: %s OK!' % ip
            return 'notfind'
    except e:
        logging.info("Remove block ip: %s had Error" % ip)
        print "Remove block ip: %s had Error" % ip
        print e
        return  False
import datetime
def gettime(s):
    try:
        b = s[-3:]
        d = int(s.split(b)[0])
        if b == 'min':
            t = datetime.datetime.now() + datetime.timedelta(minutes=d)
        elif b == 'day':
            t = datetime.datetime.now() + datetime.timedelta(days=d)
        t = t.strftime("%Y-%m-%d %H:%M:%S")
        return t
    except:
        print "have error gettime()"
        return "0000-00-00 00:00:00"


if __name__=="__main__":
    driver = webdriver.Ie()
    driver.get(acenet_url)
    #login
    logging.info('---------------------------Login--------------------------------')
    print '---------------------------Login--------------------------------'
    handle = login(driver,acenet_user,acenet_pass)
    if  handle != 'ERROR':
        print 'login ok'
    else:
        print 'login error'
        driver.quit()
        sys.exit()
    #get data
    logging.info('---------------------------Get Flow Data--------------------------------')
    print '---------------------------Get Flow Data--------------------------------'
    realtime_data = get_realtime_data(driver,handle)
    total_data =get_total_data(driver,handle)

    if realtime_data !='ERROR' and total_data !='ERROR':
        print 'Get data is OK!'
        logging.info('Get data is OK!')
    elif realtime_data =='ERROR':
        logging.info("Get realtime_data Error! Quit!")
        print "Get realtime_data Error! Quit!"
        driver.quit()
        sys.exit()
    elif total_data =='ERROR':
        logging.info("Get total_data Error! Quit!")
        print "Get total_data Error! Quit!"
        driver.quit()
        sys.exit()

    #
    #deal data
    logging.info('---------------------------Connect mysql DB--------------------------------')
    print '---------------------------Connect mysql DB--------------------------------'
    try:
        con = MySQLdb.connect(host=db_ip,user=db_user,passwd=db_pass,db=db_db)
    except Exception, e:
        print e
        logging.info('Mysql connect Error')
        sys.exit()
    cur = con.cursor()

    logging.info('---------------------------Insert Flow Data to DB--------------------------------')
    print '---------------------------Insert Flow Data to DB--------------------------------'
    if insert_data(realtime_data,realtime_total,realtime_recv,realtime_send) \
            and insert_data(total_data,total_total,total_recv,total_send):
        print 'Insert data is ok!'
        logging.info('Run Insert data is ok!')

    else:
        print "Insert data have issue"
        logging.info("Insert data have issue")

    # filter high flow ip
    logging.info('---------------------------Get block ip list--------------------------------')
    print '---------------------------Get block ip list--------------------------------'
    realtime_block = search_ip(realtime_data,realtime_limit)
    total_blcok = search_ip(total_data,total_limit)

    if realtime_block != 'ERROR' and realtime_data !='ERROR':
        print realtime_block
        logging.info(realtime_block)
        print total_blcok
        logging.info(total_blcok)
    else:
        logging.info("Search High Flow Ip Have Error")
        print "Search High Flow Ip Have Error"

    logging.info('---------------------------Filter block ip list--------------------------------')
    print '---------------------------Filter block ip list--------------------------------'

    if len(realtime_block) != 0:
        try:
            sql ="select ip from %s where  type = 'realtime' or type ='all'" % safe_ip
            cur.execute(sql)
            results = cur.fetchall()
            logging.info('Realtime safe ip list')
            for r in results:
                print r
                logging.info(r)
                rip = r[0].decode('utf-8')
                if rip in realtime_block:
                    realtime_block.remove(rip)
        except:
            print "Get realtime safe ip have issue"
            logging.info("Get realtime safe ip have issue")
    print '-----split--------'
    if len(total_blcok) !=0:
        try:
            sql ="select ip from %s where  type = 'total' or type ='all'" % safe_ip
            cur.execute(sql)
            results = cur.fetchall()
            logging.info('Total safe ip list')
            for r in results:
                print r
                logging.info(r)
                rip = r[0].decode('utf-8')
                if rip in total_blcok:
                    total_blcok.remove(rip)
        except:
            print "Get total safe ip have issue"
            logging.info("Get total safe ip have issue")

    print '----------Filter total block ip-------------'
    if len(total_blcok) !=0:
        try:
            sql ="select ip from %s where  remask = 'total' and type = 'unlock' and endtime < NOW()" % safe_ip
            cur.execute(sql)
            results = cur.fetchall()
            logging.info('Filter Total safe ip list')
            for r in results:
                print r
                logging.info(r)
                rip = r[0].decode('utf-8')
                if rip in total_blcok:
                    total_blcok.remove(rip)
        except:
            print "Get filter total safe ip have issue"
            logging.info("Get filter total safe ip have issue")

    print realtime_block
    print total_blcok

    logging.info(realtime_block)
    logging.info(total_blcok)

    logging.info('---------------------------This is Add block ip info--------------------------------')
    print '---------------------------This is Add block ip info--------------------------------'
    if change_block(driver,handle):
        print "switch to block ip page"
        logging.info("switch to block ip page")
    else:
        print "can not switch to block ip page"
        logging.info("can not switch to block ip page")
        driver.quit()
        sys.exit()

    #add block ip

    if len(total_blcok) !=0:
        for j in total_blcok:
            if add_blockip(driver, handle, j, total):
                print 'add %s' % j
                try:
                    print gettime(total)
                    sql ="insert into %s(ip, status, type,createtime,endtime) \
                              values ('%s', 'block', 'total',NOW(), '%s')" % (log_ip, j, gettime(total))
                    cur.execute(sql)
                    print 'Insert log_table OK!'
                    sql ="insert into %s(ip, name,remask,type,endtime,createtime) \
                              values ('%s', 'auto', 'total','unlock', '%s', NOW())" % (safe_ip, j, gettime(total))
                    cur.execute(sql)
                    print 'Insert safe_table OK!'
                except:
                    print 'Insert total block data have error'


            else:
                print 'Can not add total blcok ip'
                logging.info("Can not add total blcok ip")
    else:
        print 'Not total ip need total block'
        logging.info("Not total ip need total block")


    if len(realtime_block) !=0:
        for i in realtime_block:
            if add_blockip(driver,handle,i,realtime) :
                print 'add %s' % i
                try:
                    sql ="insert into %s(ip, status, type,createtime,endtime) \
                          values ('%s', 'block', 'realtime',NOW(), '%s')" % (log_ip, i, gettime(realtime))
                    cur.execute(sql)
                    time.sleep(1)
                    sql ="insert into %s(ip, name,remask,type,endtime,createtime) \
                              values ('%s', 'auto', 'realtime','unlock', '%s', NOW())" % (safe_ip, i, gettime(realtime))
                    cur.execute(sql)
                except:
                    print 'Insert realtime block data have error'
            else:
                print 'Can not add realtime blcok ip'
                logging.info("Can not add realtime blcok ip")
    else:
        print 'Not realtime ip need  block'
        logging.info("Not realtime ip need  block")
    #remove some ip from block ip
    time.sleep(1)
    logging.info('---------------------------This is remove block ip info-------------------------------')
    print '---------------------------This is remove block ip info--------------------------------'

    try:
        sql ="select ip from %s where  type = 'unlock' and endtime < NOW() " % safe_ip
        count = cur.execute(sql)
        results = cur.fetchall()
        for r in results:
            print r
            ip = r[0]
            print ip
            tmp =remove_blockip(driver,handle,ip)
            if tmp:
                if  tmp == 'find':
                    try:
                        sql ="insert into %s(ip, status, type,createtime,endtime) values \
                                            ('%s', 'unlock', 'remove',NOW(), NOW())" % (log_ip, ip)
                        cur.execute(sql)
                        time.sleep(0.5)
                        sql ="update %s Set type ='done' where type = 'unlock' and ip = '%s'" % (safe_ip, ip)
                        cur.execute(sql)
                        logging.info('Remove  block  %s OK!' % ip)
                        print 'Remove  block  %s OK!' % ip
                    except:
                        print 'Remove  block  %s data have error' % ip
                else:
                    print 'Unlock ip  %s not in block list' % ip
                    sql ="update %s Set type ='done' where type = 'unlock' and ip = '%s'" % (safe_ip, ip)
                    cur.execute(sql)
                    logging.info('Unlock ip  %s not in block list' % ip)
            else:
                print 'Unlock ip: %s have Issue'%ip
                logging.info('Unlock ip: %s have Issue'%ip)

    except:
        print 'Open mysql table %s have issue'% safe_ip
        logging.info('Open mysql table %s have issue'% safe_ip)


    logging.info('----------------------------Run over! Quit!-------------------------------')
    print '---------------------------Run over! Quit!--------------------------------'

    cur.close()
    driver.quit()
    time.sleep(5)
    sys.exit()