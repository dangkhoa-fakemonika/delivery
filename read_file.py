input_dir = 'input_level1.txt'
fs = open(input_dir, "r")


n, m, t, f = fs.readline().split()
adj = []
for _ in range(int(n)):
    line = fs.readline().split()
    temp = [int(i) if i.isnumeric() or (i.lstrip('-')).isnumeric() else i for i in line]
    if 'S' in temp:
        s_pos = (temp.index('S'), _)
    if 'G' in temp:
        e_pos = (temp.index('G'), _)
    adj.append(temp)
fs.close()

# print(n, m, t, f)
for _ in adj:
    print(_)

print(s_pos)
print(e_pos)