#! /usr/bin/env python3
'Download all the class files to a local directory'

import os, urllib.request, urllib.error, urllib.parse, re, dbm.dumb, time, gzip, io, threading, sys
from collections import namedtuple
from base64 import b64encode
from gzip import GzipFile
import re
from datetime import date, timedelta
from time import sleep
from multiprocessing.pool import ThreadPool as Pool
import ssl

# Monkeypatch ssl to disable certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

class_id = 'pyclass_d59'
pyclass_links = 'https://bit.ly/pyclass_links'
dirname = 'notes'
auth = b64encode('{0}:{1}'.format(class_id, '').encode()).decode()

Response = namedtuple('Response', ['code', 'msg', 'compressed', 'written'])

def retry_urlopen(request, tries=5, pause=0.2):
    for i in range(tries):
        try:
            return urllib.request.urlopen(request)
        except (urllib.error.HTTPError, urllib.error.URLError) as exception:
            exc = exception
            sleep(pause)
    return Response(500, 'URLError', False, False)

def urlretrieve(url, filename, cache={}, lock=threading.Lock()):
    'Read contents of an open url, use etags and decompress if needed'

    request = urllib.request.Request(url)
    request.add_header('User-Agent', "Raymond's Downloader")
    request.add_header('Accept-Encoding', 'gzip')
    request.add_header("Authorization", "Basic %s" % auth)
    with lock:
        if ('etag ' + url) in cache:
            request.add_header('If-None-Match', cache['etag ' + url])
        if ('mod ' + url) in cache:
            request.add_header('If-Modified-Since', cache['mod ' + url])

    u = retry_urlopen(request)
    if isinstance(u, Response):
        return u
    content = u.read()
    u.close()

    compressed = u.getheader('Content-Encoding') == 'gzip'
    if compressed:
        content = gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb').read()

    written = writefile(filename, content)

    with lock:
        etag = u.getheader('Etag')
        if etag:
            cache['etag ' + url] = etag
        timestamp = u.getheader('Last-Modified')
        if timestamp:
            cache['mod ' + url] = timestamp

    return Response(u.code, u.msg, compressed, written)

def writefile(filename, content):
    "Only write content if it is not already written."
    try:
        with open(filename, 'rb') as f:
            curr_content = f.read()
            if curr_content == content:
                return False
    except IOError:
        pass
    with open(filename, 'wb') as f:
        f.write(content)
    return True


def download(target, dirname=dirname):
    'Retrieve a target url and return the download status as a string'
    filename = target.rsplit('/', 1)[-1]
    fullname = os.path.join(dirname, filename)
    r = urlretrieve(target, fullname, etags)
    if r.code != 200:
        return '%3d  %-16s %s' % (r.code, r.msg, target)
    compressed = '*' if r.compressed else ' '
    written = '(updated)' if r.written else '(current)'
    return '%3d%1s %-16s %-55s --> %-25s %s ' % \
           (r.code, compressed, r.msg, target, fullname, written)

if __name__ == '__main__':
    try:
        os.mkdir(dirname)
    except OSError:
        pass

    print((' Source: %s' % pyclass_links).center(117, '='))
    print((' Starting download at %s ' % time.ctime()).center(117))

    etags = dbm.dumb.open(os.path.join(dirname, 'etag_db'))
    request = urllib.request.Request(pyclass_links)
    request.add_header("Authorization", "Basic %s" % auth)
    web_object = urllib.request.urlopen(request)
    root_url = os.path.dirname(web_object.geturl())
    if web_object.getheader('Content-Encoding') == 'gzip':
        web_object = GzipFile(fileobj=web_object)
    links_text = web_object.read().decode('utf-8')
    links_text = re.sub('https://127.0.0.1:8080', root_url, links_text)
    targets = re.findall(r'^http(?:s?)://\S+', links_text, re.M)
    mapper = Pool(5).imap_unordered
    # mapper = map
    for line in mapper(download, targets):
        print(line)
    etags.close()

