#!/bin/python

import urllib2
import MySQLdb
import time
import re

# this is get from ../newsmth.net/mysql.php


url ='http://bbs.nju.edu.cn/bbstop10'

content = urllib2.urlopen(url).read()
table = re.findall(r'<a href="(.*?)">', content)

#Con = MySQLdb.Connect(host=MYSQL_HOST, port=3307, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB ,charset='utf8')

def GetTitle(Con):
    Con = Con.replace('\n','')
    Con = Con.replace('\r','')
    title = re.findall(r'A">(.*?)</a>',Con)
    return title

title = GetTitle(content)
for i in range(0,len(title)):
    print title[i]

def Traverse(data):
    text = data[0] + '<!--more-->'
    for i in range(1,len(data)):
        text =text + data[i]
        if (i % 10 ==0):
            text = text + '<!--nextpage-->'
    return text

def InsertDatabase(title,content):
    now = time.localtime()
    sdate = time.strftime("%Y-%m-%d",now)
    Con = MySQLdb.Connect(host=MYSQL_HOST, port=3307, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB ,charset='utf8')
    Cursor = Con.cursor()
    para = (content,title)
    sql = "INSERT INTO `wp_posts` (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES (NULL, '1', now(), now(), %s,%s, '', 'publish', 'open', 'open', '', 'hello-world', '', '', now(), now(), '', '0', 'http://localhost:8080/wordpress/?p=1', '0', 'post', '', '0');"
    Cursor.execute(sql,para)
    Con.commit()
    maxid = "select max(ID) from `wp_posts`"
    Cursor.execute(maxid)
    cds=Cursor.fetchall() #.....
    para1=(cds[0][0])
    insert = "INSERT INTO  `wp_term_relationships` (`object_id` ,`term_taxonomy_id` ,`term_order`)VALUES (%s,  '6',  '0');"
    Cursor.execute(insert,para1)
    Con.commit()
    
        
def GetContent(url,title):
	Con = urllib2.urlopen(url).read()
	Con = Con.replace('\n','<br/>')
	text = re.findall(r'class=hide>(.*?)</textarea',Con)
	#print len(text) 
	content =  Traverse(text)
	content = content.replace('[m','')
	title = title.decode('gb2312','ignore')
	content = content.decode('gb2312','ignore')
	InsertDatabase(title,content)

for i in range(0,len(table)):
    newurl = 'http://bbs.nju.edu.cn/' + table[len(table)-i-1] + '&start=-1'
    #print newurl
    GetContent(newurl,title[len(table)-i-1])

