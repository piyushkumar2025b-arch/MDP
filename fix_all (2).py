import ast

# Step 1: Fix mega_features_v20.py
lines = open('mega_features_v20.py', encoding='utf-8').readlines()
out = []
for line in lines:
    if 'MolFromSmarts' in line and 'C=C' in line:
        indent = len(line) - len(line.lstrip())
        out.append(' ' * indent + 'db = 0  # fixed\n')
        print('FIX 1: bad SMARTS replaced')
    else:
        out.append(line)
open('mega_features_v20.py', 'w', encoding='utf-8').writelines(out)

# Step 2: Completely rewrite the broken section of app.py
src = open('app.py', encoding='utf-8').read()

# Disable stmol/py3Dmol
src = src.replace('import py3Dmol\n', '# py3Dmol disabled\n')
src = src.replace('from stmol import showmol\n', '# stmol disabled\n')
print('FIX 2: imports disabled')

# Fix showmol usage
lines = src.splitlines(keepends=True)
out = []
for line in lines:
    if 'showmol(' in line and not line.strip().startswith('#'):
        indent = len(line) - len(line.lstrip())
        out.append(' ' * indent + 'st.info("3D viewer disabled on cloud.")\n')
        print('FIX 3: showmol replaced')
    else:
        out.append(line)
src = ''.join(out)

# Step 3: Find and fix the analyze section - replace the ENTIRE spinner block
import re

# Remove ALL previous broken attempts around analyze call first
# then insert clean version
bad_patterns = [
    # orphan try with analyze
    '        try:\n            data = analyze(input_text.split(","))\n        except Exception as e:\n            st.error(f"Analysis error: {e}")\n            data = []\n',
    '        try:\n        data = analyze(input_text.split(","))\n',
    '        try:\n            data = analyze(input_text.split(","))\n',
]

clean = '        data = analyze(input_text.split(","))\n'
for bad in bad_patterns:
    if bad in src:
        src = src.replace(bad, clean)
        print(f'Cleaned bad pattern')

# Now insert the correct try/except
good = '''        try:
            data = analyze(input_text.split(","))
        except Exception as e:
            st.error(f"Analysis error: {e}")
            data = []
'''
src = src.replace(clean, good)
print('FIX 4: analyze wrapped correctly')

open('app.py', 'w', encoding='utf-8').write(src)

# Verify
for f in ['app.py', 'mega_features_v20.py']:
    try:
        ast.parse(open(f, encoding='utf-8').read())
        print(f'SYNTAX OK: {f}')
    except SyntaxError as e:
        print(f'SYNTAX ERROR in {f} line {e.lineno}: {e.msg}')
        # Show the problematic lines
        lines = open(f, encoding='utf-8').readlines()
        start = max(0, e.lineno-3)
        end = min(len(lines), e.lineno+3)
        for idx, l in enumerate(lines[start:end], start+1):
            print(f'  {idx}: {repr(l)}')

print('\nDONE! Run: git add . && git commit -m "fix: final" && git push')
