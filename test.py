import re

with open('dist/css/index.css') as file:
    contents = file.read()


exp = r'url\(\'?([(..)/].*?)\'?\)'
links = re.findall(exp, contents)

for i in range(len(links)):
    links[i] = links[i].split('?')[0]
    links[i] = links[i].split('#')[0]

# 2) Clear all duplicates
links = list(dict.fromkeys(links))