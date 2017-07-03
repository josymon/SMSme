
#!/usr/bin/python

import re
import time
import urllib2
import cookielib
import sys
import os
hostname = ''

# Replace SITE with the respective value
def foodie_download():
 url = 'http://SITE/index.php'
 hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
     'Accept-Encoding': 'gzip, deflate',
     'Accept-Language': 'en-US,en;q=0.8',
     'Cookie': 'PHPSESSID=4667087f38951fb911d0741515ccbf8f',
     'Connection': 'keep-alive'}
 req = urllib2.Request(url,headers=hdr)

 try:
  usock = urllib2.urlopen(req)
  html = usock.read()
  f = open('foodie.html', 'w')
  f.write(html)
  f.close()
 except Exception, e:
  print str(e)


def foodfinder():
 message = ''
 h = re.compile('myList = (.*?);')
 for line in open('foodie.html'):
  if 'myList = ' in line:
   res = h.findall(line)

 start = res[0].find('"Today":')

 end = res[0].find('"Tomorrow"')

 find = re.compile('"value":"(.*?)"')
 list = find.findall(res[0][start:end].strip())
 list = [item.replace('\\r\\n', ' ') for item in list]

 hour = time.strftime("%H")

 if '03' in hour:
  message = '#BREAKFAST\n' + list[0] + '\n\n#LUNCH\n' + list[1]

 elif '15' in hour:
  message = '#TEA\n' + list[2] + '\n\n#DINNER\n' + list[3]
 return message
 
# Enter the correct username, password and numbers to which message need to send  
def send_message():
 username = "" 
 passwd = ""
 foodie_download()
 message = ""
 message = foodfinder()
 numbers = [""]
 message = "+".join(message.split(' '))

 url = 'http://site24.way2sms.com/Login1.action?'
 data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

 cj = cookielib.CookieJar()
 opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

 opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

 try:
  usock = opener.open(url, data)
 except IOError:
  print "Error while logging in."
  sys.exit(1)
  
 jession_id = str(cj).split('~')[1].split(' ')[0]
 send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
 for number in numbers:
        send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
        opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
 try:
    sms_sent_page = opener.open(send_sms_url,send_sms_data)
 except IOError:
    print "Error while sending message"

 sys.exit(1)


if __name__ == '__main__':
        send_message()
