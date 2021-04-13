#!/usr/bin/env python3

from highlight import analyze_python, build_html_page
import os, re
from glob import glob
from html import escape
from pathlib import Path
from itertools import chain
from subprocess import getoutput

index_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8">
<meta http-equiv="refresh" content="15">
<link rel="shortcut icon" href="https://www.python.org/favicon.ico">
<title> {title} </title>
<style type="text/css">
{css}
</style>
</head>
<body>
{body}
</body>
</html>
'''

html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8">
<title> {title} </title>
<link rel="shortcut icon" href="https://www.python.org/favicon.ico">
<style type="text/css">
{css}
</style>
</head>
<body>{body}
</body>
</html>
'''

def publish_one(sourcefile, destfile):
    if sourcefile.endswith('.ipynb'):
        encoded = getoutput(f'jupyter-nbconvert --stdout {sourcefile}')
    else:
        with open(sourcefile) as sf:
            source = sf.read()
        try:
            classified_text = analyze_python(source)
            encoded = build_html_page(classified_text, html=html, title=sourcefile)
        except Exception:  # Process source without highlighting
            with open(sourcefile) as sf:
                source = ''.join(f'{escape(line.rstrip())}<br>\n' for line in sf)
            encoded = html.format(title=sourcefile, css='', body=source)
    with open(destfile, 'w') as df:
        df.write(encoded)

def make_index_page(index):
    lines = [
        '<h2> Python Class Files </h2>\n',
        '<h5> Copyright \N{copyright sign} 2021 Raymond Hettinger </h5>\n',
        '<ul>\n',
        '<li><a href="/shared/pyinstall/html/index.html">'
            'pyinstall.html</a></li>\n',
        '<li><a href="/shared/pyinstall/html/_static/CSR-1000v.pdf">'
            'CSR-1000v.pdf \N{copyright sign} CISCO</a></li>\n',
    ]
    for htmlfile, sourcefile in sorted(index):
        line = '<li><a href="%s">%s</a></li>\n' % (
            htmlfile, sourcefile)
        lines.append(line)
    lines += ['</ul>\n']
    body = ''.join(lines)
    css = 'body {background-color:#F8FFFF;}'
    return index_html.format(title='FileIndex', css=css, html=html, body=body)

def publish(pubdir):
    try:
        os.mkdir(pubdir)
    except OSError:
        pass
    updates = 0
    index = []
    for sourcefile in chain(glob('*.py'), glob('*.log'), glob('*.ipynb')):
        disamb = 'NB_' if sourcefile.endswith('.ipynb') else ''

        htmlfile = disamb + os.path.splitext(os.path.basename(sourcefile))[0] + '.html'
        destfile = os.path.join(pubdir, htmlfile)
        if not os.path.exists(destfile) or \
           os.stat(sourcefile).st_ctime > os.stat(destfile).st_ctime:
                print(time.ctime(), 'Updating', sourcefile, '-->', destfile)
                publish_one(sourcefile, destfile)
                updates += 1
        index.append((htmlfile, sourcefile))
    index_filename = os.path.join(pubdir, 'index.html')
    if updates or not os.path.exists(index_filename):
        Path(pubdir).touch()
        print('New index:', index_filename)
        index_page = make_index_page(index)
        with open(index_filename, 'w') as f:
            f.write(index_page)
    return index_filename

if __name__ == '__main__':
    import sys, time

    print('Starting in:', os.getcwd())
    pubdir = sys.argv[1] if len(sys.argv) > 1 else 'pub'
    print('Writing to:', pubdir)
    while True:
        publish(pubdir)
        time.sleep(3)
