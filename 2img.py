from PIL import Image
import sys
from math import sqrt
import textwrap
 
"""
(237,237,237) -> 白色
(239, 176, 50) -> 橙色
(226, 125, 213) -> 品红
(151, 176, 239) -> 淡蓝
(219, 219, 107) -> 黄色
(125, 202, 25) -> 绿色
(239, 176, 202) -> 粉色
(75, 75, 75) -> 深灰
(151, 151, 151) -> 淡灰
(75, 151, 176) -> 陶蓝
(176, 101, 226) -> 紫色
(50, 101, 202) -> 湖蓝
(125, 101, 75) -> 棕色
(86, 164, 77) -> 绿色
(202, 75, 75) -> 红色
(17,17,17) -> 黑色
"""
 
color_map = \
    {
        (237, 237, 237): '0',
        (239, 176, 50): '1',
        (226, 125, 213): '2',
        (151, 176, 239): '3',
        (219, 219, 107): '4',
        (125, 202, 25): '5',
        (239, 176, 202): '6',
        (75, 75, 75): '7',
        (151, 151, 151): '8',
        (75, 151, 176): '9',
        (176, 101, 226): 'a',
        (50, 101, 202): 'b',
        (125, 101, 75): 'c',
        (86, 164, 77): 'd',
        (202, 75, 75): 'e',
        (17, 17, 17): 'f'
    }
 
keys = list(color_map.keys())
 
# path = None
# w = None
# h = None
path = r"D:\Download\AB3769A3F0A66A448A89B75BDDC0A580.jpg"
w = 82
h = 40
vec = [(-2, -1), (-2, 0), (-1, -1), (-1, 0), (0, -1), (0, 0)]
head = r'\x'
 
 
def list_sub(x: list):
    re = ""
    for t in x:
        re += str(t)
    return re
 
 
def to_hex(num: str):
    assert num[0] == '1'
    assert num[2] == '0'
    num = int(num, 2)
    re = hex(num)[2:]
    if len(re) == 1:
        re = '0' + re
    return re
 
 
def line(word, com, total):
    print("\r", end="")
    print(f"{word} {com}/{total}: ", "#" * (int(com / total) // 2), end="")
    sys.stdout.flush()
 
 
def found_color(r, g, b, *a):
 
    score = 255 * 3
    color = ''
    for br, bg, bb in color_map.keys():
        # if (now_score := (sqrt(abs(r * r - br * br) + sqrt(abs(g * g - bg * bg)) + sqrt(abs(b * b - bb * bb))))) < score:
        if (now_score := (abs(r - br) + abs(g - bg) + abs(b - bb))) < score:
            score = now_score
            color = color_map[(br, bg, bb)]
    return color
 
 
def co_count(inp: str):
    co_dir = {}
 
    mx = -1
    mxt = ''
    mn = -1
    mnt = ''
    assert inp != ''
    for c in inp:
        if c not in co_dir.keys():
            co_dir[c] = inp.count(c)
            if co_dir[c] > mx:
                mx = co_dir[c]
                mxt = c
            elif co_dir[c] > mn:
                mn = co_dir[c]
                mnt = c
    assert mxt != ''
    return mxt, mnt
 
 
def open_image(pa):
    img = Image.open(pa)
    return img
 
 
def write_in(f_co, b_co, te, file_name=''):
    assert len(f_co) == len(b_co) == len(te)
    with open(".\\" + file_name + ".lua", "w+") as file:
        for i in range(len(f_co)):
            f = f_co[i]
            b = b_co[i]
            t = te[i]
            t = textwrap.wrap(t, 2)
            file.write('term.scroll(-1)\nterm.setCursorPos(1,1)\n')
            file.write(f"term.blit('{list_sub([head + x for x in t])}', '{f}', '{b}')\n")
 
 
def main(img, iw, ih):
    iw *= 2
    ih *= 3
    img.convert("P")
    img = img.resize((iw, ih))
 
    # img.show()
 
    pix = list(img.getdata())
    out = ''
    for i in pix:
        out += found_color(*i)
    input_pix = textwrap.wrap(out, iw)
 
    '''
    i[0][0] i[0][1]
    i[1][0] i[1][1]
    1[2][0] |1[2][1]|
    '''
 
    f_co = []
    b_co = []
    te = []
 
    for i in range(2, ih, 3):
        f_co.append('')
        b_co.append('')
        te.append('')
        for j in range(1, iw, 2):
            out = ''
            for x, y in vec:
                out += input_pix[i + x][j + y]
            m1, m2 = co_count(out)
            if out[-1] == m1:
                # 001_____ -> bg
                f_co[-1] += m2 if m2 != '' else m1
                b_co[-1] += m1
                trans_word = ''
                for c in '0123456789abcdef':
                    if c == m2:
                        trans_word += '1'
                    else:
                        trans_word += '0'
                out = list(out.translate(str.maketrans('0123456789abcdef', trans_word)))
                out.reverse()
                te[-1] += to_hex('10' + list_sub(out))
            else:
                f_co[-1] += m1
                b_co[-1] += m2 if m2 != '' else m1
                trans_word = ''
                for c in '0123456789abcdef':
                    if c == m1:
                        trans_word += '1'
                    else:
                        trans_word += '0'
                out = list(out.translate(str.maketrans('0123456789abcdef', trans_word)))
                out.reverse()
                te[-1] += to_hex('10' + list_sub(out))
    f_co.reverse()
    b_co.reverse()
    te.reverse()
    return f_co, b_co, te
 
 
if __name__ == "__main__":
    if path is None:
        path = input("输入图片完整路径")
    if w is None or h is None:
        w, h = int(*input("输入图片宽高，以空格分割").split(" "))
    write_in(*main(open_image(path), w, h))