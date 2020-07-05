import os
import re

def getUploadURL(team, relative):
    if re.match('http', relative):
        return relative
    else:
        extension = os.path.splitext(relative)[1][1:].upper()
        if extension == 'HTML':
            # remove '/index.html' from the end
            if relative.endswith('/index.html'):
                relative = relative[:-11]
            return 'https://2020.igem.org/wiki/index.php?title=Team:' + team + relative + '&action=edit'
        elif extension == 'CSS' or extension == 'JS': 
            final = os.path.splitext(relative)[0] + extension
            return 'https://2020.igem.org/wiki/index.php?title=Template:' + team + final + '&action=edit'

    
def URLreplace(team, relative):
    if re.match('http', relative):
        return relative
    
    extension = os.path.splitext(relative)[1][1:].upper()
    
    if extension == 'CSS':
        filetype = 'css'
    elif extension == 'JS':
        filetype = 'javascript'
    
    absolute = os.path.splitext(relative)[0] + extension
    if absolute[0] != '/':
        absolute = '/' + absolute
    absolute = 'https://2020.igem.org/Template:' + team + absolute + '?action=raw&ctype=text/' + filetype
    
    return absolute
