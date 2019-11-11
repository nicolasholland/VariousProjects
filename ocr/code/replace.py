
def replace(b):
    with open(b, 'r') as r:
        c = r.read()
    d = c.replace('#', '|')

    with open(b, 'w') as w:
        w.write(d)
