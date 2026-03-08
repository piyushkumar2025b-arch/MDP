f = open('app.py', encoding='utf-8')
content = f.read()
f.close()

old = 'data = analyze(input_text.split(","))'
new = '''try:\n    data = analyze(input_text.split(","))\nexcept Exception as e:\n    st.error(f"Analysis error: {e}")\n    data = []'''

if old in content:
    open('app.py', 'w', encoding='utf-8').write(content.replace(old, new))
    print('FIXED!')
else:
    print('Pattern not found')
