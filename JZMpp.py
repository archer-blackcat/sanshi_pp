from collections import UserList,OrderedDict,deque,ChainMap,Counter
from SanShi import LiuRen,TDpan,ModList,TaiYi,ShenSha,RiSha,YueSha,NianSha
import pandas as pd

Zhi=["子", "丑","寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
g5x=dict(zip(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],"木木火火土土金金水水"))
d5x=dict(zip(Zhi,"水土木木土火火土金金土水"))
jgd=dict(zip(["丑","寅", "辰", "巳", "未", "申", "戌", "亥"],[['癸'],['甲'],['乙'],['丙','戊'],['丁','己'],['庚'],['辛'],['壬']]))
jg = {'甲':'寅','乙':'辰','丙':'巳','丁':'未','戊':'巳','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
x5="木火土金水"
chong = dict(zip(Zhi,ModList(Zhi).rerange('午')))
xing = dict(zip(Zhi,"卯戌巳子辰申午丑寅酉未亥"))

def mkLiuRen(yj,s,rg,rz,zhouye,guiren_plan=0):
    xx=LiuRen(yj,s)
    xx.add_dungan(rg,rz)
    xx.add_guiren(rg,zy=zhouye,plan=guiren_plan)
    xx.add_6q(rg)
    sk = xx.mk_4k(rg,rz)
    return xx,sk

def shehai(sk,zhils,kw='地天关系',plan=1):
    #Zhi=["子", "丑","寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    zhi=ModList(Zhi)
    # g5x=dict(zip(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],"木木火火土土金金水水"))
    # d5x=dict(zip(Zhi,"水土木木土火火土金金土水"))
    # jgd=dict(zip(["丑","寅", "辰", "巳", "未", "申", "戌", "亥"],[['癸'],['甲'],['乙'],['丙','戊'],['丁','己'],['庚'],['辛'],['壬']]))
    # jg = {'甲':'寅','乙':'辰','丙':'巳','丁':'未','戊':'巳','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
    # x5="木火土金水"
    q6=['庙','脱','贼','克','生']
    x5cmp=lambda t,d:q6[x5.index(t)-x5.index(d)]
    if plan == 1:
        

        final = {}

        for dz in zhils:
            z = jg[dz] if dz in jg.keys() else dz
            steps=zhi.rerange(z).index(sk[dz]['天盘'])
            slf=d5x[sk[dz]['天盘']]
            rslt = []
            for x in zhi.rerange(z)[:steps+1]:
                tt=d5x[x]
                rslt.append(x5cmp(slf,tt))
                if x in jgd:
                    for ji in jgd[x]:
                        rslt.append(x5cmp(slf,g5x[ji]))
            out = Counter(rslt)
            final[dz]=out[sk[dz][kw]]

        final = sorted(final.items(), key=lambda x: x[1], reverse=True)
        if final[0][1]>final[1][1]:
            return final[0][0]
        else:
            ils=[x[0] for x in final if x[1]==final[0][1]]
            return shehai(sk,ils,plan=0)
    else:
        test = "寅申巳亥子午卯酉丑辰未戌"
        zl = []
        for dz in zhils:
            z = jg[dz] if dz in jg.keys() else dz
            zl.append(z)
        for x in test:
            if x in zl:
                if x not in zhils:
                    for i in jgd[x]:
                        if i in zhils:
                            return i
                return x

def jzm_help(sk):
    sk=dict(sk)
    q6=['庙','脱','贼','克','生']
    zk=dict(zip(q6,[[],[],[],[],[]]))
    [zk[z].append(x) for z in q6 for x in sk if sk[x]['地天关系']==z]
    
    base = sk[list(sk.keys())[0]]['地盘刚柔']
    for x in sk:
        sk[x]['比干']=int(sk[x]['天盘刚柔']==base)
    
    p6=['兄弟','子孙','妻财','官鬼','父母']
    pk=dict(zip(p6,[[],[],[],[],[]]))
    [pk[z].append(x) for z in p6 for x in sk if sk[x]['六亲']==z]
    
    if zk['贼']==[] and zk['克']==[]:
        zk=[]
    if pk['妻财']==[] and pk['官鬼']==[]:
        pk=[]
        
    return sk,zk,pk

def kbs(sk,zk,pk,shpl=1):
    hx={}
        
    if zk!=[]:
        hx = {'始入':zk['贼'],'元首':zk['克']}
    if pk!=[]:
        hx['篙矢']=pk['官鬼']
        hx['弹射']=pk['妻财']
    for x in hx:
        if hx[x] != []:
            uls=hx[x]
            kname = x 
            break
            
    if len(uls)==1:
        if kname=='始入':
            kname='始入' if hx['元首']==[] else '重审'
        return [kname,sk[uls[0]]['天盘']]
    
    elif len(uls)>1:
        bg=[x for x in uls if sk[x]['比干']==1]
        if len(bg)==1:
            kn_map={'始入':'比用','元首':'知一','篙矢':'比用篙矢','弹射':'比用弹射'}
            return [kn_map[kname],sk[bg[0]]['天盘']]
        else:
            kn_map={'始入':'贼涉害','元首':'克涉害','篙矢':'篙矢涉害','弹射':'弹射涉害'}
            kw_map={'始入':'地天关系','元首':'地天关系','篙矢':'六亲','弹射':'六亲'}
            return [kn_map[kname],sk[shehai(sk,uls,kw=kw_map[kname],plan=shpl)]['天盘']]
        
def maoxing(xx,sk,zk,pk):
    count_tp = set([x[1]['天盘'] for x in sk])
    if zk==[] and pk==[] and len(count_tp)==4:
        if sk[0][1]['地盘刚柔']=='刚':
            kname='虎视'
            ccz=xx.get_tp('酉')[1]['天盘']
            zm = [xx.get_tp(sk[2][0]),xx.get_dp(sk[0][1]['天盘'])]
        elif sk[0][1]['地盘刚柔']=='柔':
            kname='蛇掩'
            ccz=xx.get_dp('酉')[0]
            zm = [xx.get_dp(sk[0][1]['天盘']),xx.get_tp(sk[2][0])]
    return [kname,ccz,zm]

def bieze(xx,sk,zk,pk):
    # Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # jg = {'甲':'寅','乙':'辰','丙':'巳','丁':'未','戊':'巳','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
    gan = ModList(Gan)
    ganh = gan.rerange('己')
    ganhe = dict(zip(gan,ganh))
    zhi=ModList(Zhi)
    zhiheju_q=dict(zip(zhi,zhi.rerange('辰')))
    count_tp = set([x[1]['天盘'] for x in sk])

    if zk==[] and len(count_tp)==3:
        if sk[0][1]['地盘刚柔']=='刚':
            ghdp = jg[ganhe[sk[0][0]]]
            ccz=xx.get_tp(ghdp)[1]['天盘']
        elif sk[0][1]['地盘刚柔']=='柔':
            ccz=zhiheju_q[sk[2][0]]
        zm = [xx.get_dp(sk[0][1]['天盘'])]*2
    return ['别责',ccz,zm]

def bazhuan(xx,sk,zk,pk):
    # jg = {'甲':'寅','乙':'辰','丙':'巳','丁':'未','戊':'巳','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
    # Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"] 
    zhi=ModList(Zhi)
    zhiq3=dict(zip(zhi,zhi.rerange('寅')))
    zhih3=dict(zip(zhi,zhi.rerange('戌')))
    count_tp = set([x[1]['天盘'] for x in sk])

    if zk==[] and len(count_tp)==2 and jg[sk[0][0]]==sk[2][0]:
        if sk[0][1]['地盘刚柔']=='刚':
            ccz = zhiq3[sk[0][1]['天盘']]
        elif sk[0][1]['地盘刚柔']=='柔':
            ccz = zhih3[sk[1][1]['天盘']]

        zm = [xx.get_dp(sk[0][1]['天盘'])]*2
    return ['八专',ccz,zm]

def fuyin(xx,sk,zk,pk):
    # Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"] 
    # chong = dict(zip(Zhi,ModList(Zhi).rerange('午')))
    # xing = dict(zip(Zhi,"卯戌巳子辰申午丑寅酉未亥"))

    if sk[1][1]['天盘']==sk[1][0]:
        if sk[0][1]['地盘刚柔']=='刚':
            kname='自任'
            ccz = sk[0][1]['天盘']
            zcz = xing[ccz] if xing[ccz] != ccz else sk[2][1]['天盘']
            mcz = xing[zcz] if xing[zcz] != zcz else chong[zcz]
        elif sk[0][1]['地盘刚柔']=='柔':
            
            if zk==[]  :
                kname='自信'
                ccz = sk[2][1]['天盘']
                zcz = xing[ccz] if xing[ccz] != ccz else sk[0][1]['天盘']

            else:
                kname='课'
                ccz = (zk['贼']+zk['克'])[0]
                zcz = xing[ccz] if xing[ccz] != ccz else sk[1][1]['天盘']
            mcz = xing[zcz] if xing[zcz] != zcz else chong[zcz]
        
        if xing[ccz]==ccz:
            kname='杜传'
        zm = [xx.get_dp(zcz),xx.get_dp(mcz)]
    return ['伏吟'+kname,ccz,zm]

def fanyin(xx,sk,zk,pk):
    if zk==[] and sk[1][1]['天盘']==chong[sk[1][0]]:
        kname='反吟井栏'
        rs = RiSha()
        rs.addin()
        ccz = rs.zhi_sha(sk[2][0],'驿马')
        zcz = sk[2][1]['天盘']
        mcz = sk[0][1]['天盘']
    zm = [xx.get_dp(zcz),xx.get_dp(mcz)]
    return [kname,ccz,zm]

def jzm_select(xx,sk):
    sk_d,zk,pk=jzm_help(sk)
    count_tp = set([x[1]['天盘'] for x in sk])
    c_kbs=len(zk)>0 or (len(count_tp)>2 and len(pk)>0)
    c_mx=(zk==[] and pk==[] and len(count_tp)==4)
    c_bz=(zk==[] and pk==[] and len(count_tp)==3)
    c_8z=(zk==[] and len(count_tp)==2 and jg[sk[0][0]]==sk[2][0] and sk[1][0] != sk[1][1]['天盘'] and sk[1][1]['天盘']!=chong[sk[1][0]])
    c_fu=sk[1][1]['天盘']==sk[1][0]
    c_fn=(sk[1][1]['天盘']==chong[sk[1][0]])
    return [c_kbs,c_mx,c_bz,c_8z,c_fu,c_fn]

def xinyinfu(xx):
    xyp =pd.read_csv('贵人落地盘.csv').set_index('idx')
    for x in xx.pan:
        tmp = xx.pan[x]
        tmp['将临类象'] = xyp.loc[x,tmp['天将']]

def get_pan(xx,sk,shh=1):
    xinyinfu(xx)
    sk_d,zk,pk=jzm_help(sk)
    sel = jzm_select(xx,sk)
    if sel[0] and sel[-1]:
        out = kbs(sk_d,zk,pk,shpl=shh)
        out[0]='反吟'
    elif sel[0]:
        out = kbs(sk_d,zk,pk,shpl=shh)
    elif sel[-1]:
        out = fanyin(xx,sk,zk,pk)
    elif sel[-2]:
        out = fuyin(xx,sk,zk,pk)
    elif sel[1]:
        out = maoxing(xx,sk,zk,pk)
    elif sel[2]:
        out = bieze(xx,sk,zk,pk)
    elif sel[3]:
        out = bazhuan(xx,sk,zk,pk)
    return out