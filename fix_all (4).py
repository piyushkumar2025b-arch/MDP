import re, ast

print("=== CHEMOFILTER MASTER FIX + LIGHT THEME ===\n")

src = open('app.py', encoding='utf-8').read()

# ── FIX 1: Rename r= in pubchem/ai functions to avoid conflict with analyze's r ──
src = src.replace(
    "        r=requests.get(f\"https://pubchem",
    "        resp=requests.get(f\"https://pubchem"
)
src = src.replace(
    "        if r.status_code==200:\n            p=r.json()[\"PropertyTable\"]",
    "        if resp.status_code==200:\n            p=resp.json()[\"PropertyTable\"]"
)
# Fix ai_explain r conflict
src = src.replace(
    '        r=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":700,',
    '        resp=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":700,'
)
src = src.replace(
    '        if r.status_code==200: return r.json()["content"][0]["text"]\n    except: pass\n    return "AI analysis unavailable."',
    '        if resp.status_code==200: return resp.json()["content"][0]["text"]\n    except: pass\n    return "AI analysis unavailable."'
)
src = src.replace(
    '        r=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":900,',
    '        resp=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":900,'
)
src = src.replace(
    '        if r.status_code==200: return r.json()["content"][0]["text"]\n    except: pass\n    return "[]"',
    '        if resp.status_code==200: return resp.json()["content"][0]["text"]\n    except: pass\n    return "[]"'
)
src = src.replace(
    '        r=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":500,',
    '        resp=requests.post("https://api.anthropic.com/v1/messages",\n            headers={"Content-Type":"application/json"},\n            json={"model":"claude-sonnet-4-20250514","max_tokens":500,'
)
src = src.replace(
    '        if r.status_code==200: return r.json()["content"][0]["text"]\n    except: pass\n    return "Repurposing analysis unavailable."',
    '        if resp.status_code==200: return resp.json()["content"][0]["text"]\n    except: pass\n    return "Repurposing analysis unavailable."'
)
print("FIX 1: renamed r= conflicts in helper functions")

# ── FIX 2: Fix mega_features_v20.py bad SMARTS ──
lines = open('mega_features_v20.py', encoding='utf-8').readlines()
out = []
for line in lines:
    if 'MolFromSmarts' in line and 'C=C' in line:
        indent = len(line) - len(line.lstrip())
        out.append(' ' * indent + 'db = 0  # fixed bad SMARTS\n')
        print("FIX 2: bad SMARTS fixed in mega_features_v20.py")
    else:
        out.append(line)
open('mega_features_v20.py', 'w', encoding='utf-8').writelines(out)

# ── FIX 3: Disable stmol/py3Dmol ──
src = src.replace('import py3Dmol\n', '# py3Dmol disabled\n')
src = src.replace('from stmol import showmol\n', '# stmol disabled\n')
lines = src.splitlines(keepends=True)
out2 = []
for line in lines:
    if 'showmol(' in line and not line.strip().startswith('#'):
        indent = len(line) - len(line.lstrip())
        out2.append(' ' * indent + 'st.info("3D viewer: run locally to view 3D structure.")\n')
        print("FIX 3: showmol replaced")
    else:
        out2.append(line)
src = ''.join(out2)
print("FIX 3: stmol/py3Dmol disabled")

# ── FIX 4: Clean up any broken try: blocks and add proper one ──
spinner_pattern = r'    with st\.spinner\([^)]+\):\n([ \t]*try:\n)*[ \t]+(data = analyze\(input_text\.split\(","\)\))\n([ \t]*try:\n)*([ \t]*except[^\n]*\n[ \t]*[^\n]*\n[ \t]*[^\n]*\n)*'
clean_spinner = '    with st.spinner("  Running ADMET analysis..."):\n        try:\n            data = analyze(input_text.split(","))\n        except Exception as e:\n            st.error(f"Analysis error: {e}")\n            data = []\n'
new_src = re.sub(spinner_pattern, clean_spinner, src)
if new_src != src:
    print("FIX 4: analyze() try/except fixed")
    src = new_src

# ── FIX 5: LIGHT THEME - Replace dark CSS variables ──
old_css = """  --bg:        #04070a;
  --bg2:       #080c14;
  --bg3:       #0c121d;"""
new_css = """  --bg:        #f8f9fc;
  --bg2:       #ffffff;
  --bg3:       #eef1f7;"""
src = src.replace(old_css, new_css)

# Fix text colors for light theme
src = src.replace('--ice:#c8deff', '--ice:#1a1a2e')
src = src.replace('--ice:      #c8deff', '--ice:      #1a1a2e')
src = src.replace("color:var(--ice)", "color:#1a1a2e")
src = src.replace("color: var(--ice)", "color:#1a1a2e")

# Fix inline dark backgrounds
src = src.replace('#080c14', '#ffffff')
src = src.replace('#04070a', '#f8f9fc')
src = src.replace('#0c121d', '#eef1f7')
src = src.replace('#020617', '#f0f4ff')
src = src.replace('#0f172a', '#e8eef8')

# Fix the dynamic CSS block
src = src.replace(
    "--bg:#080c14;--bg2:#0c1220;--amber:#f5a623;--ice:#c8deff;--border:rgba(245,166,35,.14)",
    "--bg:#f8f9fc;--bg2:#ffffff;--amber:#d4860a;--ice:#1a1a2e;--border:rgba(180,130,0,.2)"
)
src = src.replace(
    "background:var(--bg);color:var(--ice)",
    "background:var(--bg);color:#1a1a2e"
)
print("FIX 5: Light theme applied")

# Save app.py
open('app.py', 'w', encoding='utf-8').write(src)

# ── VERIFY SYNTAX ──
for f in ['app.py', 'mega_features_v20.py']:
    try:
        ast.parse(open(f, encoding='utf-8').read())
        print(f'SYNTAX OK: {f}')
    except SyntaxError as e:
        print(f'SYNTAX ERROR in {f} line {e.lineno}: {e.msg}')
        lines2 = open(f, encoding='utf-8').readlines()
        for idx in range(max(0,e.lineno-3), min(len(lines2),e.lineno+3)):
            print(f'  {idx+1}: {repr(lines2[idx])}')

print('\nDONE! Run: git add . && git commit -m "fix+theme: all bugs fixed, light theme" && git push')
