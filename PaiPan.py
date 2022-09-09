import sxtwl
from collections import UserList,OrderedDict,deque,Counter
import pendulum as pdlm
from SanShi import LiuRen,TDpan,ModList,TaiYi,ShenSha,RiSha,YueSha,NianSha,DunJia
from JZMpp import mkLiuRen,get_pan
import pandas as pd

def ty_js(pdd=pdlm.now().date(),pds=pdlm.now().time(),shiji=1):
    pdorig=pdlm.date(1804,5,14)
    day = sxtwl.fromSolar(pdd.year, pdd.month, pdd.day)
    shiGZ=day.getHourGZ(pds.hour)
    
    jiri = (pdd-pdorig).days
    jishu = jiri*12+shiGZ.dz+1 if shiji else jiri+1
    
    return jishu
def get_dungan(g,z):
    Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸","空","亡"])
    Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    dg_map=OrderedDict(zip(Zhi.rerange(z),Gan.rerange(g)))
    return dg_map
    

def get_jq(pdd=pdlm.now()):
    day = sxtwl.fromSolar(pdd.year, pdd.month, pdd.day)
    for x in range(0,16):
        if day.before(x).hasJieQi():
            return day.before(x).getJieQi()

def get_yuejiang(pdd=pdlm.now()):
    Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    yuejiang_map = [Zhi.reverse().rerange('丑')[i//2] for i in range(24)]
    return yuejiang_map[get_jq(pdd)]

def get_4z(pdd=pdlm.now().date(),pds=pdlm.now().time(),sep=1):
    day = sxtwl.fromSolar(pdd.year, pdd.month, pdd.day)

    yTG = day.getYearGZ()
    #月干支
    mTG = day.getMonthGZ()
    #日干支
    dTG  = day.getDayGZ() if pds.hour<23 else day.after(1).getDayGZ()
    #时干支,传24小时制的时间，分早晚子时
    sTG = day.getHourGZ(pds.hour)
    
    rslt={'年':(yTG.tg,yTG.dz),'月':(mTG.tg,mTG.dz),'日':(dTG.tg,dTG.dz),'时':(sTG.tg,sTG.dz)}
    
    Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])
    Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    out={}
    for x in rslt:
        g=Gan[rslt[x][0]]
        z=Zhi[rslt[x][1]]
        out[x] = (g,z) if sep else g+z
    return out
    

def paipan_csh(pdd=pdlm.now().date(),pds=pdlm.now().time(),sj=1):
    bazi1 = get_4z(pdd,pds)
    bazi2 = get_4z(pdd,pds,sep=0)
    jq=get_jq(pdd)
    yuejiang=get_yuejiang(pdd)
    tyjs = ty_js(pdd,pds,shiji=sj)
    return bazi1,bazi2,jq,yuejiang,tyjs

def xingnian(gz='丁卯',fm=1,pdd=pdlm.now().date()):
    xn = get_4z(pdd,sep=0)['年']
    Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])
    Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    jz = ModList([Gan.get(i)+Zhi.get(i) for i in range(60)]).rerange(gz)
    xngnn = jz.rerange('丙寅') if fm else jz.reverse().rerange('壬申')
    
    return xngnn[jz.index(xn)]
    

    

class HePan(TDpan):
    def __init__(self,bazi,jq,yuejiang,tyjs):
        self.bazi1=bazi[0]
        self.bazi2=bazi[1]
        self.jq,self.yuejiang,self.tyjs = jq,yuejiang,tyjs
        hpi_z= ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
        hpi_gong= ModList([1,8,3,4,9,2,7,6])
        hpi_yu = ModList(['乾','艮','巽','坤','中'])
        super().__init__(hpi_z+hpi_gong+hpi_yu,"idx",list(range(1,13))+[21,28,23,24,29,22,27,26]+[31,32,33,34,35])
        
        self.zhi_p=TDpan()
        self.gong_p=TDpan()
        self.yu_p=TDpan()
        
        self.zhi_p.pan=OrderedDict([x for x in self.pan.items() if x[0] in hpi_z])
        self.gong_p.pan=OrderedDict([x for x in self.pan.items() if x[0] in hpi_gong])
        self.yu_p.pan=OrderedDict([x for x in self.pan.items() if x[0] in hpi_yu])
        
        self.ty = TaiYi()
        self.ty.paipan1(self.tyjs,yy=self.jq>11)
        self.ty.paipan2(self.tyjs)
        
        for z in self.pan:
            self.pan[z]['乙盘将']=[]
            self.pan[z]['乙盘神']=[]
    
    def add_6r(self,sh=0,gr=1):
        self.lr,self.sk = mkLiuRen(self.yuejiang,self.bazi1['时'][1],self.bazi1['日'][0],self.bazi1['日'][1],zhouye=(self.bazi1['时'][1] in "酉戌亥子丑寅"),guiren_plan=gr)
        fy=get_pan(self.lr,self.sk,shh=sh)
        self.ke_name = fy[0]
        self.chuan = self.lr.mk_3c(fy[1],flag=1 if len(fy)>2 else 0,other=fy[2] if len(fy)>2 else [])
        df=pd.read_csv('三传名称.csv').set_index('idx')
        df = df.apply(lambda x:x.str.split('\r\n'))

        if self.lr.get_pj() in df.index:
            pj = self.lr.get_pj()
            fayong = self.chuan[0][1]['天盘']
            self.chuan_name = df.loc[pj,fayong][1]
        else:
            self.chuan_name = ""
 
        
        self.zhi_p.addv('天盘',self.lr.get_name('天盘'))
        self.zhi_p.addv('天遁',self.lr.get_name('天盘遁干'))
        self.zhi_p.addv('地遁',self.lr.get_name('地盘遁干'))
        self.zhi_p.addv('天将',self.lr.get_name('天将'))
        self.zhi_p.addv('六亲',self.lr.get_name('六亲'))
        self.zhi_p.addv('类象',self.lr.get_name('将临类象'))
    
    def add_ty(self):
        ty2hp=OrderedDict(zip(self.ty.np.pan.keys(),[1,8,3,4,9,2,7,6,'中']))
        wp =self.ty.wp.pan
        np =self.ty.np.pan
        #self.ty2djp = self.ty.sync_np()
        for gn in wp :
            self.pan[gn]['乙盘将'].extend(wp[gn]['将表'])
            self.pan[gn]['乙盘神'].extend(wp[gn]['神基表'])
            
        for gn in np :
            self.pan[ty2hp[gn]]['乙盘将'].extend(np[gn]['将表'])
    
    def add_dj(self):
        dj=DunJia()
        self.djp,self.zhishi,self.zslg,self.zhifu,self.zflg,self.djn,self.djn_yy=dj.paipan(self.bazi2['日'],self.jq,self.bazi2['时'])
        djpan=self.djp.pan
        self.gong_p.addv('甲盘',self.djp.get_name('宫干'))
        self.gong_p.addv('天盘',self.djp.get_name('天盘'))
        self.gong_p.addv('九星',self.djp.get_name('天盘星'))
        self.gong_p.addv('八门',self.djp.get_name('八门'))
        self.gong_p.addv('八神',self.djp.get_name('八神'))
    def get(self,idx,name):
        return self.pan[idx][name]