import commands
import re
import json

def invoke():
    output = str(commands.getoutput("bash pyflakes.sh $CHOC_FILE"))
    parse(output)

def parse(output):
    errormessage = r'^([^:\n]+):(\d+): ([^\n]+)'
    caretposition = r'( *)\^ *'
    fullregex_inner = r'%s(\n[^\n]+\n%s)?' % (errormessage, caretposition)
    fullregex = re.compile(fullregex_inner, re.MULTILINE)
    matches = re.findall(fullregex, output)
    display(map(parse_match, matches))

def parse_match(match):
    path = match[0]
    line = int(match[1])
    message = match[2]
    caret_outer = match[3]
    caret_inner = match[4]
    
    column = -1
    if len(caret_outer) > 0:
        column = len(caret_inner) + 1
    
    return {
        'path': path,
        'line': line,
        'message': message,
        'column': column,
        'type': 'error' if 'error' in message or 'syntax' in message or 'unexpected' in message else 'warning',
    }

def display(output):
    print json.dumps(output)

invoke()
