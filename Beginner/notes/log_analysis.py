import collections, pprint, re

visited = collections.Counter()
with open('notes/nasa_19950801.log') as f:
    for line in f:
        mo = re.search(r'GET\s+(\S*)\s+200', line)
        if mo is not None:
            url = mo.group(1)
            visited[url] += 1

pprint.pprint(visited.most_common(20))
