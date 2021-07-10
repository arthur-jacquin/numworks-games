def howmany(ch):
    id = ch[0]
    number = 0
    for char in ch:
        if char == id: number += 1
        else: break
    return number

src, index = input('Name of the file : '), 0
content = open(src, 'r')
output = open(src.strip('.slc') + '_extracted.py', 'w')
output.write('# ' + src + '\n\n')
for line in content:
    line = line.strip()
    if line.startswith('<Level'): array = []
    elif line.startswith('<L>'): array.append(line[3:-4])
    elif line == '</Level>':
        index, level = index + 1, ''
        WIDTH, HEIGTH = len(max(array, key=len)), len(array)
        if WIDTH > 50 or HEIGTH > 30: continue
        for li in array:
            while len(li) < WIDTH: li += ' '
            reduced = ''
            while li:
                number = howmany(li)
                reduced += str(number) + li[0] if int(number) > 1 else li[0]
                li = li[number:]
            level += '|' + reduced.replace(' ', '-')
        output.write(f"'{level[1:]}'\n")
content.close()
output.close()
