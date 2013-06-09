import re
import urllib2
import time
import MySQLdb



url = "http://m.byr.cn"

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
    insert = "INSERT INTO  `wp_term_relationships` (`object_id` ,`term_taxonomy_id` ,`term_order`)VALUES (%s,  '9',  '0');"
    Cursor.execute(insert,para1)
    Con.commit()


def Getcontent(title,url):
	content = urllib2.urlopen(url).read()
	con = re.findall(r'<ul(.*?)</ul>',content)
	print url
	print len(con)
#	print con[0]
	article = "<ul" + con[0] + "</ul>" + "<!--nextpage-->"
	return article

def Getpage(ptitle,purl):
        link = "http://m.byr.cn" + purl
        link = link.replace("\"","")
        print link
        content = urllib2.urlopen(link).read()
	#print content
        pages = re.findall(r'>1/(.*?)</a>',content)
        article = ""
        for i in range(1, int(pages[0]) + 1):
                u = link + "?p=" + str(i)
                article += Getcontent(ptitle,u)
        InsertDatabase(ptitle,article)


def Traverse(T):
	for i in range(1, len(T)):
		purl = re.findall(r'href=(.*?)>',T[len(T)-i-1])
		ptitle = re.findall(r'>(.*?)\(<span',T[len(T)-i-1])
		print ptitle[0]
		print purl[0]
		Getpage(ptitle[0],purl[0])


def Gettitle(url):
	content = urllib2.urlopen(url).read()
	ul = re.findall(r'<ul class="slist sec">(.*?)/ul>',content)
	title = re.findall(r'<li>(.*?)</li>',ul[0])
	#print len(title)
	Traverse(title)
	#print content

Gettitle(url)
