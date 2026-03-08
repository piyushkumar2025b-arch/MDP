import ast

# Fix app.py - surgically clean the spinner block
src = open('app.py', encoding='utf-8').read()

# Find the spinner block and replace the ENTIRE thing cleanly
import re

# Replace any variation of the broken spinner+try block with clean version
pattern = r'    with st\.spinner\([^)]+\):\n(?:[ \t]*try:\n)*[ \t]+(data = analyze\(input_text\.split\(","\)\))\n(?:[ \t]*try:\n)*(?:[ \t]*except[^\n]*\n[ \t]*[^\n]*\n[ \t]*[^\n]*\n)*'

clean_block = '''    with st.spinner("  Running ADMET  CYP  SA  AI analysis..."):\n        try:\n            data = analyze(input_text.split(","))\n        except Exception as e:\n            st.error(f"Analysis error: {e}")\n            data = []\n'''

new_src = re.sub(pattern, clean_block, src)

if new_src != src:
    print('Pattern matched and replaced!')
else:
    print('Regex did not match - doing line by line fix')
    lines = src.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        # Skip all stacked try: lines before analyze call
        if lines[i].strip() == 'try:':
            # Look ahead - if there's another try: or analyze call coming, skip this try:
            j = i + 1
            while j < len(lines) and lines[j].strip() == 'try:':
                j += 1
            if j < len(lines) and 'data = analyze' in lines[j]:
                # Skip all the try: lines
                print(f'Removed {j-i} stacked try: lines')
                i = j
                continue
        out.append(lines[i])
        i += 1
    new_src = ''.join(out)

open('app.py', 'w', encoding='utf-8').write(new_src)

# Verify
try:
    ast.parse(open('app.py', encoding='utf-8').read())
    print('SYNTAX OK: app.py')
except SyntaxError as e:
    print(f'SYNTAX ERROR line {e.lineno}: {e.msg}')
    lines = open('app.py', encoding='utf-8').readlines()
    for idx in range(max(0,e.lineno-4), min(len(lines),e.lineno+4)):
        print(f'  {idx+1}: {repr(lines[idx])}')

print('\nDONE! Run: git add . && git commit -m "fix: final" && git push')
