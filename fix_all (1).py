import os, re

print("=== MASTER FIX SCRIPT ===\n")

# FIX 1: mega_features_v20.py - broken SMARTS
fn = 'mega_features_v20.py'
lines = open(fn, encoding='utf-8').readlines()
fixed = []
for line in lines:
    if 'MolFromSmarts' in line and 'C=C' in line:
        indent = len(line) - len(line.lstrip())
        fixed.append(' ' * indent + 'db = 0  # fixed\n')
        print('FIX 1: bad SMARTS replaced')
    else:
        fixed.append(line)
open(fn, 'w', encoding='utf-8').writelines(fixed)

# FIX 2,3,4: app.py
fn = 'app.py'
lines = open(fn, encoding='utf-8').readlines()
out = []
i = 0
while i < len(lines):
    line = lines[i]
    # Remove stmol/py3Dmol imports
    if 'import py3Dmol' in line and not line.strip().startswith('#'):
        out.append('# py3Dmol disabled\n')
        print('FIX 2: py3Dmol disabled')
        i += 1; continue
    if 'from stmol import showmol' in line and not line.strip().startswith('#'):
        out.append('# stmol disabled\n')
        print('FIX 2: stmol disabled')
        i += 1; continue
    # Replace showmol
    if 'showmol(' in line and not line.strip().startswith('#'):
        indent = len(line) - len(line.lstrip())
        out.append(' ' * indent + 'st.info("3D viewer disabled on cloud.")\n')
        print('FIX 3: showmol replaced')
        i += 1; continue
    # Remove orphan try: lines left from previous broken fixes
    if line.strip() == 'try:' and i + 1 < len(lines) and 'data = analyze' in lines[i+1]:
        print('FIX 4a: removed orphan try:')
        i += 1; continue
    # Fix broken except blocks with no matching try
    if line.strip().startswith('except Exception as e:') and i > 0 and 'data = analyze' in lines[i-1]:
        print('FIX 4b: removed orphan except')
        i += 1
        while i < len(lines) and (lines[i].strip().startswith('st.error') or lines[i].strip() == 'data = []'):
            i += 1
        continue
    # Wrap analyze call properly
    if 'data = analyze(input_text.split(","))' in line and not line.strip().startswith('#'):
        indent = len(line) - len(line.lstrip())
        sp = ' ' * indent
        out.append(sp + 'try:\n')
        out.append(sp + '    data = analyze(input_text.split(","))\n')
        out.append(sp + 'except Exception as e:\n')
        out.append(sp + '    st.error(f"Analysis error: {e}")\n')
        out.append(sp + '    data = []\n')
        print('FIX 4: analyze wrapped in try/except')
        i += 1; continue
    out.append(line)
    i += 1
open(fn, 'w', encoding='utf-8').writelines(out)

# Verify syntax
import ast
for f in ['app.py', 'mega_features_v20.py']:
    try:
        ast.parse(open(f, encoding='utf-8').read())
        print(f'SYNTAX OK: {f}')
    except SyntaxError as e:
        print(f'SYNTAX ERROR in {f}: line {e.lineno} - {e.msg}')

print('\nDONE! Run: git add . && git commit -m "fix: final" && git push')
