__author__ = 'yanghongsheng-lt'
import os
import sys
path = os.path.abspath(os.path.dirname(sys.argv[0]))
fi = path + '\\config'
a = ('192.168.67.27',)
b= [u'192.168.67.27', u'192.168.76.218']


c = a[0].decode('utf-8')
if c in b:
    b.remove(c)

    print b


