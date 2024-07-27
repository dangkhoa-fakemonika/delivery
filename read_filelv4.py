input_dir = 'input_lv4.txt'
fs = open(input_dir, "r")

s_list = [(-1,-1)] * 10
g_list = [(-1,-1)] * 10

n, m, t, f = fs.readline().split()
adj = []
for _ in range(int(n)):
    line = fs.readline().split()
    temp = [int(i) if i.isnumeric() or (i.lstrip('-')).isnumeric() else i for i in line]

    for s in temp:
        if isinstance(s, str):
            if s == 'S':
                s_list[0] = (_, temp.index(s))
            elif s[0] == 'S':
                pos = int(s[-1])
                s_list[pos] = (_, temp.index(s))

    for g in temp:
        if isinstance(g, str):
            if g == 'G':
                g_list[0] = (_, temp.index(g))
            elif g[0] == 'G':
                pos = int(g[-1])
                g_list[pos] = (_, temp.index(g))

    adj.append(temp)
fs.close()

s_list = list(filter(lambda x: x != (-1,-1), s_list))
g_list = list(filter(lambda x: x != (-1,-1), g_list))