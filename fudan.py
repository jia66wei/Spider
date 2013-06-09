#!/bin/python

import urllib2
import re
import time
import MySQLdb


MYSQL_DB = "app_campustopic"
MYSQL_USER = "5nz303m111"
MYSQL_PASS = "lizywjyhly1m2zil5khhhjw15ijm30ywl1l5hh21"
MYSQL_HOST = "w.rdc.sae.sina.com.cn"
MYSQL_PORT = 3307

url = "http://bbs.fudan.edu.cn/m/bbs/top10"
fudan = "http://bbs.fudan.edu.cn/m/bbs/"

#http://bbs.fudan.edu.cn/m/bbs/tcon?board=Astrology&f=802708
#content = urllib2.urlopen(url).read()
article = ""


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
    insert = "INSERT INTO  `wp_term_relationships` (`object_id` ,`term_taxonomy_id` ,`term_order`)VALUES (%s,  '7',  '0');"
    Cursor.execute(insert,para1)
    Con.commit()


def GetPage(url):
    content = urllib2.urlopen(url).read()
    Con = re.findall(r'<div id="main">(.*?)<div id="ft">',content)
   # print len(Con)
    global article
    article = article + Con[0] +"<!--nextpage-->"
    nextpage = re.findall(r'<a href="tcon(.*?)a=n">',content)
    print len(nextpage)
    if(len(nextpage) != 0):
        pagenum = fudan + "tcon" + nextpage[0]+ "a=n"
        pagenum = pagenum.replace("amp;","")
        print pagenum
        return pagenum
    else:
        return 0

def Compose(title,url):
    next = GetPage(url)
    global article
    while(next != 0):
        next = GetPage(next)

    article_utf = article.decode('gb18030','ignore')
    title_utf = title.decode('gb18030','ignore')
    InsertDatabase(title_utf,article_utf)
    article = ""
    fout = open('test.txt','w')
    fout.write(article)
    fout.close()    

def Traverse(T):
    for i in range(0,len(T)):
        #print T[i]
        purl = re.findall(r'<a href="(.*?)">',T[len(T)-i-1])
        ptitle = re.findall(r'">(.*?)</a>',T[len(T)-i-1])
        purl[0] = purl[0].replace("amp;","")
        pu = fudan + purl[0]
        print pu
        print ptitle[0]
        Compose(ptitle[0],pu)

def GetTitle(url):
    content = urllib2.urlopen(url).read()
    title = re.findall(r'<p>(.*?)</p>',content)
    Traverse(title)

GetTitle(url)



