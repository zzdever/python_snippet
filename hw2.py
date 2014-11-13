# This script find all urls which contains the keyword
# Extra action: create a cache folder under current directory
 
import urllib2
import re
from urlparse import urljoin
import hashlib
import os

def fetch(url):
    # create cache folder
    cache_folder = 'cache'
    if not os.path.exists(cache_folder):
	os.mkdir(cache_folder)

    # generate html file name
    filename = hashlib.sha1(url).hexdigest()
    path = os.path.join(cache_folder, filename)

    # if the html is not cached, fetch from the remote server
    if not os.path.exists(path):
        r = urllib2.urlopen(url)
        content = r.read()
        with open(path, 'w') as f:
            f.write(content)

    # open file and read in the content
    with open(path, 'r') as f:
        return f.read()


# urls of all problems in one page
def post_urls(page):
    data = fetch('http://acm.zju.edu.cn/onlinejudge/showProblems.do?contestId=1&pageNumber=%d' % page) 
    urls = re.findall(r'/onlinejudge/showProblem\.do\?problemCode=\d+', data)
    return [urljoin('http://acm.zju.edu.cn', url) for url in urls]


def page_count():
    data = fetch('http://acm.zju.edu.cn/onlinejudge/showProblemsets.do')
    vols = re.findall(r'/onlinejudge/showProblems\.do\?contestId=1&pageNumber=\d+', data)
    urlset = set(vols)  # remove duplicates
    return len(urlset)  # the size of the set equals to the page amount


# find pattern in the page specified by url, which does the actual search
def check(url, pattern):
    data = fetch(url)
    return re.search(pattern, data) is not None


# find urls of problems in all pages
def post_urls_all():
    urls = []
    for page in range(1, page_count() + 1):
        urls.extend(post_urls(page))
    return urls


# find all urls and then serch in every page
def grepZOJ(pattern):
    urls = set([])
    posts = post_urls_all()
    for i, post in enumerate(posts):
        if check(post, pattern):
            urls.add(post)
    return urls


# main
for url in grepZOJ(r'[Mm]atrix|[Mm]atrices'): 
    print url
