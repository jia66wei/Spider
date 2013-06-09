#!/bin/python
import time
import MySQLdb
import urllib2
import re


# this is get from ../newsmth.net/mysql.php
MYSQL_DB = "app_campustopic"      
MYSQL_USER = "5nz303m111"    
MYSQL_PASS = "lizywjyhly1m2zil5khhhjw15ijm30ywl1l5hh21" 
MYSQL_HOST = "w.rdc.sae.sina.com.cn"  

url ='http://www.newsmth.net/nForum/rss/topten'

def Smthspider(url):
    content = urllib2.urlopen(url).read()
    text = re.findall(r'<p>(.*?)</p>',content)
    cons = text[0] + '<!--more-->'
    for i in range(1,len(text)):
        cons = cons + text[i]
    cons = cons + '<!--nextpage-->'
    return cons
    
def InsertDatabase(title,content):
    now = time.localtime()
    sdate = time.strftime("%Y-%m-%d",now)
    Con = MySQLdb.Connect(host='w.rdc.sae.sina.com.cn', port=3307, user=MYSQL_USER , passwd=MYSQL_PASS, db=MYSQL_DB,charset='utf8')
    Cursor = Con.cursor()
    para = (content,title)
    
    sql = "INSERT INTO wp_posts (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES (NULL, '1', now(), now(), %s, %s, '', 'publish', 'open', 'open', '', 'hello-world', '', '', '2013-05-06 02:44:56', '2013-05-06 02:44:56', '', '0', 'http://localhost:8080/wordpress/?p=1', '0', 'post', '', '0');"
    Cursor.execute(sql,para)
    Con.commit()
    maxid = "select max(ID) from `wp_posts`"
    Cursor.execute(maxid)
    cds=Cursor.fetchall() 
    para1=(cds[0][0])
    insert = "INSERT INTO  `wp_term_relationships` (`object_id` ,`term_taxonomy_id` ,`term_order`)VALUES (%s,  '3',  '0');"
    Cursor.execute(insert,para1)
    Con.commit()
    
    Con.close()
    
       
def GetContent(url):
    content = urllib2.urlopen(url).read()
    title = re.findall(r'<title>(.*?)</title>',content)
    textNum = re.findall(r'<i>(.*?)</i>',content)
    if(len(textNum) == 0):
        return
    pages = int(textNum[0])/10 + 1
    text =''
    for i in range(1,pages+1):
        u = url + '?p=' + str(i)    
        text += Smthspider(u)
  
    text_utf = text.decode('gb2312','ignore')
    M_title = title[0]
    Mtitle_utf = M_title.decode('gb2312','ignore')
    InsertDatabase(Mtitle_utf,text_utf)
   

def app():
    url ='http://www.newsmth.net/nForum/rss/topten'
    s = ''	
    cont = urllib2.urlopen(url).read()
    guid= re.findall(r'<guid>(.*?)</guid>',cont)
    urln = ''
    
    for i in range(0,len(guid)):
        urln = guid[len(guid) - i -1]
        GetContent(urln)
    
    return 'sucess'
    
application = app()



    
