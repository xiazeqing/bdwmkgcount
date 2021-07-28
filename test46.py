import os
import requests
import html.parser

lastlegal = True

pagecount = 1

usernamelist = ['zlmyb', 'MichaelYang', 'MlKU', 'yulievol&wuyuchuan', 'xxxxx', 'since', 'keyes', 'steelwedge', 'pkp',
                'niisikhsurg', 'voltanis', 'wangpx', 'tarrm&hatter', 'EatingAG', 'Bpple&westerlies',
                'HydraliskIII&Chips', 'FlyingOmelet&NicoleG', 'pthcjh&mycNoone', 'BIGBIN&cavedolphin', 'Mister']
lusn = len(usernamelist)
usernameindexs = []
usercount = []
for i in range(lusn):
    usernameindexs.append(usernamelist[i].split('&'))
    usercount.append(0)

while lastlegal:

    r = requests.get('https://bbs.pku.edu.cn/v2/thread.php?bid=958&mode=single&page=' + str(pagecount))


    # print(r.text)

    def get_body(k: str) -> str:
        r = k.split('<!-- start board-body -->')[1]
        l = r.split('<!-- end board-body -->')[0]
        return l


    b = get_body(r.text)


    # print(b)

    def get_pair_angle_brackets(k: str):
        ks = k.split('<')
        if len(ks) < 2:
            return '', ks
        kk = ks[1]
        l = len(kk)
        b = 0
        ans = -1
        for i in range(l):
            if kk[i] == '"':
                b = 1 - b
            if kk[i] == '>' and b == 0:
                ans = i
                break
        if ans < 0:
            return '', k
        else:
            return kk[0:ans], k[len(ks[0]) + ans + 2:]


    class Div(object):
        def __init__(self, k: str):
            kk, after = get_pair_angle_brackets(k)
            if kk[0:3] == 'div':
                self.valid = True
                kid = kk.split('id')
                if len(kid) > 1:
                    kkid = kid[1]
                    kquote = kkid.split('"')
                    self.id = kquote[1]
                kclass = kk.split('class')
                if len(kclass) > 1:
                    kk1 = kid[1]
                    kquote = kk1.split('"')
                    self.kclass = kquote[1]
                # then add inner
                laf = len(after)
                count = 0
                for i in range(laf - 6):
                    if after[i:i + 4] == '<div':
                        count += 1
                        # print(count,'++',after[i:i+400])
                    elif after[i:i + 6] == '</div>':
                        count -= 1
                        # print(count,'--',after[i:i+400])
                        if count < 0:
                            self.inner = after[:i]
                            self.after = after[i + 6:]
                            break
            else:
                self.valid = False


    # print(b)
    k0, k1 = get_pair_angle_brackets(b)
    k2, k3 = get_pair_angle_brackets(k1)
    bbody = Div(k3)
    h1 = Div(bbody.inner)
    lb = Div(h1.after)
    lh = Div(lb.inner)
    lc = Div(lh.after)
    lci = lc.inner

    while True:
        bef, aft = get_pair_angle_brackets(lci)
        if bef.startswith('!--'):
            lci = aft
        lcd = Div(lci)
        if not lcd.valid:
            break
        lcdi = lcd.inner
        if len(lcdi.split('<div class="pin">')) > 1:
            pass
        elif len(bef.split('display: none')) > 1:
            pass
        else:
            authname = lcdi.split('<div class="name limit">')[1].split('</div>')[0]
            posttime = lcdi.split('<div class="time">')[1].split('</div>')[0]
            print(authname, posttime)

            if '0' <= posttime[0] <= '9':
                find=False
                for i in range(lusn):
                    if authname in usernameindexs[i]:
                        usercount[i] += 1
                        find=True
                if not find:
                    print('!!!!!!')
            else:
                lastlegal = False
                for i in range(lusn):
                    print(i, usernamelist[i], usercount[i])
                os._exit(0)

        lci = lcd.after
    pagecount += 1
