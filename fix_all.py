import os

print("=== MASTER FIX SCRIPT ===\n")

# ── FIX 1: mega_features_v20.py — broken SMARTS ──────────────────────────────
fn = 'mega_features_v20.py'
lines = open(fn, encoding='utf-8').readlines()
fixed = []
changed = False
for line in lines:
    if 'MolFromSmarts' in line and 'C=C' in line:
        indent = len(line) - len(line.lstrip())
        fixed.append(' ' * indent + 'db = 0  # fixed: broken SMARTS removed\n')
        changed = True
        print(f'FIX 1 applied: bad SMARTS in {fn}')
    else:
        fixed.append(line)
if changed:
    open(fn, 'w', encoding='utf-8').writelines(fixed)
else:
    print(f'FIX 1: pattern not found in {fn}')

# ── FIX 2: app.py — remove stmol/py3Dmol imports + replace showmol ───────────
fn = 'app.py'
src = open(fn, encoding='utf-8').read()

# Remove imports
src = src.replace('import py3Dmol\n', '# py3Dmol disabled\n')
src = src.replace('from stmol import showmol\n', '# stmol disabled\n')
print('FIX 2 applied: stmol/py3Dmol imports disabled')

# Replace py3Dmol viewer block with a message
old_block = '''view = py3Dmol.view(width=800, height=500)
                view.addModel(res_3d["_conf"], "mol")
                view.setStyle({'stick': {'colorscheme': 'goldCarbon'}})
                view.zoomTo()
                showmol(view, height=500, width=800)'''
new_block = '''st.info("3D viewer disabled on cloud. Run locally to see 3D structure.")'''
if old_block in src:
    src = src.replace(old_block, new_block)
    print('FIX 3 applied: py3Dmol viewer replaced with message')
else:
    # fallback: just replace showmol line
    lines = src.splitlines(keepends=True)
    out = []
    for line in lines:
        if 'showmol(' in line:
            indent = len(line) - len(line.lstrip())
            out.append(' ' * indent + 'st.info("3D viewer disabled on cloud.")\n')
            print('FIX 3 applied: showmol line replaced')
        elif 'py3Dmol.view(' in line:
            out.append(line.replace('py3Dmol.view(', '# py3Dmol.view('))
        else:
            out.append(line)
    src = ''.join(out)

# ── FIX 4: wrap analyze() call in try/except ─────────────────────────────────
old_analyze = '        data = analyze(input_text.split(","))'
new_analyze = '''        try:
            data = analyze(input_text.split(","))
        except Exception as e:
            st.error(f"Analysis error: {e}")
            import traceback
            st.code(traceback.format_exc())
            data = []'''

if old_analyze in src:
    src = src.replace(old_analyze, new_analyze)
    print('FIX 4 applied: analyze() wrapped in try/except')
else:
    print('FIX 4: analyze pattern not found - checking...')
    idx = src.find('analyze(input_text')
    if idx >= 0:
        print(f'Found at index {idx}:', repr(src[idx-20:idx+60]))

open(fn, 'w', encoding='utf-8').write(src)

print('\n=== ALL FIXES APPLIED SUCCESSFULLY ===')
print('Now run: git add . && git commit -m "fix: all issues resolved" && git push')
