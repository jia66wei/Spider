# ke da University
import urllib2
import re
import time
import MySQLdb

url = "http://bbs.ustc.edu.cn/cgi/bbstop10"
link = "http://bbs.ustc.edu.cn/cgi/"


content = urllib2.urlopen(url).read()
global more


def InsertDatabase(title,content):
    title = title.decode('gb2312','ignore')
    content = content.decode('gb2312','ignore')
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
    insert = "INSERT INTO  `wp_term_relationships` (`object_id` ,`term_taxonomy_id` ,`term_order`)VALUES (%s,  '5',  '0');"
    Cursor.execute(insert,para1)
    Con.commit()


def Traverse(T):
    print len(T)
    global more
    more = T[0] + '<!--more-->'
    for i in range(1,len(T)):
        #print T[i]
        more = more + T[i]
    more += '<!--nextpage-->'

def Getcontent(url,title):
    print url
    Con = urllib2.urlopen(url).read()
    Con = Con.replace('\n','<br/>')
    Con = Con.replace('<br/><br/>','<br/>')
    cont = re.findall(r'<div class="post_text">(.*?)</div><br/></td>',Con)
    nextpage = re.findall(r' <a class="next" href="(.*?)"',Con)
    if(len(cont) > 0):
