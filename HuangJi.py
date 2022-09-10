from PaiPan import paipan_csh,HePan,get_dungan,ty_js,get_4z,xingnian
from SanShi import ModList
import pendulum as pdlm

Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])
Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
najia ={}

najia_G = dict(ModList([(Gan.get(x),ModList([[6],[2],[8],[7],[1],[9],[3],[4]]).get(x)) for x in range(10)]))

shu =  [1,5,3,3,5,2,2,5,4,4,5,1]

najia_Z=dict([(Zhi[i],[shu[i],shu[i]+5]) for i in range(12)])

najia.update(najia_Z)
najia.update(najia_G)

def get_tiandishu(sz):
    sl=[]
    for x in sz:
        for y in sz[x]:
            sl+=najia[y]

    tianshu =sum( [x for x in sl if x%2])
    dishu = sum([x for x in sl if x%2==0])

    return tianshu,dishu

def gua_help(x):
    out = [s for s in x]
    if len(out)==3:
        return out
    elif len(out)==2:
        out = [0] + out
    else:
        out = [0,0] + out
    return out

gua2yao=dict(zip('乾兑离震巽坎艮坤',[gua_help(bin(x-1).split('b')[1]) for x in range(1,9)]))

helper=lambda x :''.join(str(x) for x in gua2yao[x])
yao2gua = dict([(helper(x),x) for x in gua2yao])

def get_tian(shu):
    rslt = shu%25 if shu>25 else shu
    rslt = rslt%10 if rslt%10!=0 else rslt//10
    return rslt

def get_di(shu):
    rslt = shu%30 if shu>30 else shu
    rslt = rslt%10 if rslt%10!=0 else rslt//10
    return rslt


def get_guanum(sz):
    ts,ds = get_tiandishu(sz)
    tgs=get_tian(ts)
    dgs=get_di(ds)
    #return shu2gua[tgs],shu2gua[dgs],(tgs+dgs+Zhi.index(sz['时'][1])+1)%6
    return tgs,dgs

def htgua(shu,yy=0):
    ht = dict(zip(range(1,10),'坎坤震巽坤乾兑艮离')) if yy else dict(zip([1,2,3,4,5,6,7,8,9],'坎坤震巽艮乾兑艮离'))
    return ht[shu]

def cegui_shu(tian_g,di_g,yao,gxh=0,cgxh=0):
    g2s = dict(zip('乾兑离震巽坎艮坤',list(range(1,9)),)) if gxh==0 else dict(zip("坎坤震巽乾兑艮离",[1,2,3,4,6,7,8,9]))
    yang=36 if cgxh==0 else 128
    yin =24 if cgxh==0 else 112
    
    yuan = 0  #原策轨
    ty=gua2yao[tian_g] #天卦数
    dy=gua2yao[di_g]   #地卦数
    ls = dy+ty
    for x in ls:
        if int(x) == 0:
            yuan+=yang
        else:
            yuan+=yin
    ts = g2s[tian_g]
    ds = g2s[di_g]
    rslt = 0
    if yao in [4,5,0]:
        yao=6 if yao==0 else yao
        rslt=yuan*(yao*10+ts+1)+ts+ds+yao
    elif yao in [1,2,3]:
        rslt = yuan*(ds*10+yao+1)+ts+ds+yao
    
    return rslt

def bian_gua(tian_g,di_g,yao):
    ty=gua2yao[tian_g]
    dy=gua2yao[di_g] 
    xg = dy+ty
    y=5 if yao==0 else yao-1
    xg[y]=0 if int(xg[y])==1 else 1
    xdg =yao2gua[ ''.join([str(x) for x in xg[:3]])]
    xtg = yao2gua[ ''.join([str(x) for x in xg[3:]])]
    return (xtg,xdg,yao)

def gz2gua(sz):
    tgs,dgs = get_guanum(sz)
    yy = Zhi.index(sz['日'][1])
    tg=htgua(tgs,yy) if yy%2==0 else htgua(dgs,yy)
    dg=htgua(dgs,yy) if yy%2==0 else htgua(tgs,yy)
    zidx = Zhi.index(sz['时'][1])+1
    yao = (tgs+dgs+zidx)%6
    return tg,dg,yao