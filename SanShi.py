from collections import UserList,OrderedDict,deque,ChainMap,Counter
import pandas as pd

class ModList(UserList):
    
    def get(self,i):
        return self.data[i%len(self.data)]
    
    def rerange(self,el,static=False):
        idx=self.data.index(el)
        tmp1=deque(self.data)
        tmp2=[]
        while tmp1[0]!=el:
            tmp2.append(tmp1.popleft())
        rslt=list(tmp1)+tmp2
        if static:
            self.data=rslt
            return ModList(rslt)
        else:
            return ModList(rslt)
    def reverse(self):
        tmp = self.data.copy()
        tmp.reverse()
        return ModList(tmp)
        
class TDpan():
    def __init__(self,ndx=[],name='',ml=[]):
        self.pan=OrderedDict()
        for i in range(len(ndx)):
            val={};
            try:
                val[name]=ml[i]
                self.pan[ndx[i]]=val
            except IndexError:
                break
                
    def addv(self,name,ls,pos=0,loc=None):
        ndx=ModList(self.pan.keys())
        lx=ModList(ls)
        if loc!=None:
            pos=ndx.index(loc)
        for i in range(len(ndx)):
            try:
                self.pan[ndx.get(i+pos)][name]=lx.get(i)
            except IndexError:
                break
        return self
    def editv(self,name,func,on_name=False):
        for x in self.pan.values():
            if on_name:
                new_name=func(name)
                x[new_name]=x[name]
                x.pop(name)
            else:
                x[name]=func(x[name])
        return self.pan
    def get_name(self,name):
        rslt=ModList()
        for x in self.pan.values():
            rslt.append(x[name])
        return rslt
    
    def rev_get(self,name,kw='index'):
        rslt = OrderedDict()
        for x in self.pan:
            rslt[self.pan[x][name]]={kw:x}
        return rslt
            
#-----------------------以上是基本部件--------------------------
#-----------------------以下是三式------------------------------

class LiuRen(TDpan):#-----------------------六壬-----
    #Zhi=ModList( ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    def __init__(self,yj='子',shi='子'):  
        Zhi=ModList( ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
        super().__init__(Zhi,'地盘五行','水土木木土火火土金金土水')
        super().addv('天盘',Zhi.rerange(yj),loc=shi)
        tmp=OrderedDict(sorted(self.pan.items(),key=lambda x:Zhi.index(x[1]['天盘'])))
        self.tianpan=TDpan(Zhi,'地盘',list(tmp.keys()))
        self.tianpan.addv('天盘五行','水土木木土火火土金金土水')
        self.tianpan.addv('天神名',['神后','大吉','功曹','太冲','天罡','太乙','胜光','小吉','传送','从魁','河魁','登明'])
        self.sync_dp('天盘五行')
        self.sync_dp('天神名')
        self.JiGong={'甲':'寅','乙':'辰','丙':'巳','丁':'未','戊':'巳','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
        
    def tp(self):
        return self.tianpan.pan
    
    def sync_dp(self,name):
        for x in self.pan:
            self.pan[x][name]=self.tianpan.pan[self.pan[x]['天盘']][name]
    
    def add_dungan(self,gan='甲',zhi='子'):
        Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸","X","X"])
        self.addv('地盘遁干',Gan.rerange(gan),loc=zhi)
        self.tianpan.addv('天盘遁干',Gan.rerange(gan),loc=zhi)
        self.sync_dp('天盘遁干')
                                              
        
    def get_dp(self,tpZhi):
        return self.tianpan.pan[tpZhi]['地盘'],self.pan[self.tianpan.pan[tpZhi]['地盘']]
    
    def get_tp(self,dpZhi):
        return dpZhi,self.pan[dpZhi]
    
    def add_guiren(self,gan='甲',zy=0,plan=0):
        # 如果zy是0为昼贵,1为夜贵,plan 决定所用的贵人口诀
        guiren=ModList(['贵人', '腾蛇', '朱雀', '六合', '勾陈', '青龙', '天空', '白虎', '太常', '玄武', '太阴', '天后'])
        Zhi=ModList( ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
        
        pl=[{'甲':('丑','未'),'戊':('丑','未'),'庚':('丑','未'),
             '乙':('子','申'),'己':('子','申'),
            '丙':('亥','酉'),'丁':('亥','酉'),
            '壬':('巳','卯'),'癸':('巳','卯'),'辛':('午','寅')},
            #--------------------------------------------------#
            {'甲':('未','丑'),'戊':('丑','未'),'庚':('丑','未'),
             '乙':('申','子'),'己':('子','申'),
            '丙':('酉','亥'),'丁':('亥','酉'),
            '壬':('卯','巳'),'癸':('巳','卯'),'辛':('寅','午')}]
        nx=0 if self.tianpan.pan[pl[plan][gan][zy]]['地盘'] in "亥子丑寅卯辰" else 1 
        gr=guiren[-1::-1].rerange('贵人') if nx else guiren
        self.tianpan.addv('天将',gr,loc=pl[plan][gan][zy])
        self.sync_dp('天将')
    
    def add_6q(self,gan):
        g5x=dict(zip(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],"木木火火土土金金水水"))
        x5="木火土金水"
        q6=['兄弟','子孙','妻财','官鬼','父母']
        tp=self.tp()
        tmp=[]
        for x in tp:
            tmp.append(q6[x5.index(tp[x]['天盘五行'])-x5.index(g5x[gan])])
        self.tianpan.addv('六亲',tmp)
        self.sync_dp('六亲')
        
        
    def mk_3c(self,tpZhi,flag=0,other=[]):
        rslt=[]
        tp=self.tp()
        cc=self.get_dp(tpZhi)
        if flag:
            return [cc]+other
        zc=self.get_tp(tpZhi)
        mc=self.get_tp(zc[1]['天盘'])
        return [cc,zc,mc]
    
    def mk_4k(self,gan,zhi):
        g5x=dict(zip(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],"木木火火土土金金水水"))
        ggr=dict(zip(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],"刚柔刚柔刚柔刚柔刚柔"))
        zgr=dict(zip(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],"刚柔刚柔刚柔刚柔刚柔刚柔"))
        x5="木火土金水"
        q6=['庙','脱','贼','克','生']
        
        jg=self.JiGong[gan]
        _,k=self.get_tp(jg)
        
        k2g=k.copy()
        k2g['地盘五行']=g5x[gan]
        gpk=gan
        gp=k2g
        gyk,gy=self.get_tp(k2g['天盘'])
        gy=gy.copy()
        zpk,zp=self.get_tp(zhi)
        zp=zp.copy()
        zyk,zy=self.get_tp(zp['天盘'])
        zy=zy.copy()
        
        gp['地盘刚柔']=ggr[gpk]
        gy['地盘刚柔']=zgr[gyk]
        zp['地盘刚柔']=zgr[zpk]
        zy['地盘刚柔']=zgr[zyk]
        
        out = [[gpk,gp],[gyk,gy],[zpk,zp],[zyk,zy]]
        for x in out:
            x[1]['地天关系']=q6[x5.index(x[1]['天盘五行'])-x5.index(x[1]['地盘五行'])]
            x[1]['天盘刚柔']=zgr[x[1]['天盘']]

        return out
    def get_pj(self):
        key = self.pan['子']['天盘']
        name_map=dict(zip(self.pan.keys(),['伏吟','进茹','顺间','顺三交','顺三合','墓覆','反吟','四绝','逆三合','逆三交','逆间','逆茹']))
        return name_map[key]
    

class TaiYi(TDpan):#-------------------太乙------------------#
    def __init__(self):
        TY=ModList(["子", "丑","艮", "寅", "卯", "辰", "巽","巳", "午", "未", "坤","申", "酉", "戌","乾", "亥"])
        name=['地主', '阳德', '和德', '吕申', '高丛', '太阳', '大旲', '大神', '大威', '天道', '大武', '武德','太簇', '阴主', '阴德', '大义']
        self.wp=TDpan(TY,'神名',name)
        self.wp.addv('始步',[8,1,3,1,4,1,9,1,2,1,7,1,6,1,1,1])
        self.wp.addv('积步',[8,0,3,0,4,0,9,0,2,0,7,0,6,0,1,0])
        self.wp.addv('将表',[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
        self.wp.addv('神基表',[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []])
        self.wp.addv('入宫',[8,3,3,3,4,9,9,9,2,7,7,7,6,1,1,1])
        self.np=TDpan([8,3,4,9,2,7,6,1,5],'正宫','子艮卯巽午坤酉乾中')
        self.np.addv('卦名','坎艮震巽离坤兑乾中')
        self.np.addv('将表',[[], [], [], [], [], [], [], [],[]])
        self.np.addv('神基表',[[], [], [], [], [], [], [], [],[]])
        self.jlist={}
        self.shenjilist={}
        
    
    def get_suan(self,start,end):
        tmp=self.wp.pan
        suan=tmp[start]['始步']
        ks=ModList(tmp.keys())
        orig=ks.index(start)
        target=self.np.pan[end]['正宫']
        if start==target:
            return suan
        i=1
        while ks.get(orig+i)!=target:
            suan +=tmp[ks.get(orig+i)]['积步']
            i+=1
        return suan
    
    def walk_in(ml,num,start=None,):
        ls=ml.rerange(start) if start!=None else ml
        orig=ls.index(start) if start!=None else 0
        return ls.get(orig+num-1)
    
    def jiang(self,name,yy=0):
        pd={'太乙':[1,1,1,2,2,2,3,3,3,4,4,4,6,6,6,7,7,7,8,8,8,9,9,9],
           '天目':['申','酉','戌','乾','乾','亥','子','丑','艮','寅','卯','辰','巽','巳','午','未','坤','坤'],
           '计神':['寅','丑','子','亥','戌','酉','申','未','午','巳','辰','卯'],
            '岁君':["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],
            '合神':['丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅'],
           }
        nd={'太乙':[9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1],
           '天目':['寅','卯', '辰', '巽','巽', '巳', '午', '未', '坤', '申', '酉', '戌', '乾', '亥', '子', '丑', '艮','艮'],
           '计神':['申', '未', '午', '巳', '辰', '卯', '寅', '丑', '子', '亥', '戌', '酉'],
            '岁君':["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],
            '合神':['丑', '子', '亥', '戌', '酉', '申', '未', '午', '巳', '辰', '卯', '寅'],
           }
        rslt = nd[name] if yy else pd[name]
        return ModList(rslt)
    
    def jrg(self,name,num,yy=0):
        return TaiYi.walk_in(self.jiang(name,yy),num)
    
    def mu(self,name,num,yy=0):
        shen=ModList(["子", "丑","艮", "寅", "卯", "辰", "巽","巳", "午", "未", "坤","申", "酉", "戌","乾", "亥"])
        dd={'始击':shen.rerange(self.jrg('天目',num,yy))[shen.rerange(self.jrg('计神',num,yy)).index('艮')],
           '定目':shen.rerange(self.jrg('天目',num,yy))[shen.rerange(self.jrg('合神',num)).index(self.jrg('岁君',num))]}
        return dd[name]
    
    def paipan1(self,num,yy=0):
        taiyi=(self.jrg('太乙',num,yy),['理人','理天','理地'][num%3])
        wenchang=self.jrg('天目',num,yy)
        taisui=self.jrg('岁君',num)
        heshen=self.jrg('合神',num)
        jishen=self.jrg('计神',num,yy)
        shiji=self.mu('始击',num,yy)
        dingmu=self.mu('定目',num,yy)
        
        self.np.pan[taiyi[0]]['将表'].append('太乙'+taiyi[1])
        self.wp.pan[self.np.pan[taiyi[0]]['正宫']]['将表'].append('太乙'+taiyi[1])
        self.wp.pan[wenchang]['将表'].append('文昌')
        self.wp.pan[taisui]['将表'].append('岁君')
        self.wp.pan[heshen]['将表'].append('合神')
        self.wp.pan[jishen]['将表'].append('计神')
        self.wp.pan[shiji]['将表'].append('始击')
        self.wp.pan[dingmu]['将表'].append('定目')
        
        self.jlist['太乙' ]=taiyi 
        self.jlist['文昌' ]=wenchang 
        self.jlist['岁君' ]=taisui 
        self.jlist['合神' ]=heshen
        self.jlist['计神' ]=jishen
        self.jlist['始击' ]=shiji
        self.jlist['定目' ]=dingmu
        
        zhusuan=self.get_suan(wenchang,taiyi[0])
        kesuan=self.get_suan(shiji,taiyi[0])
        dingsuan=self.get_suan(dingmu,taiyi[0])
        
        self.jlist['主算']=zhusuan
        self.jlist['客算']=kesuan
        self.jlist['定算']=dingsuan
        s9=[9,1,2,3,4,5,6,7,8]
        self.jlist['主大将']=zhusuan%10 if zhusuan%10!=0 else s9[zhusuan%9]
        self.jlist['客大将']=kesuan%10  if kesuan%10!=0 else s9[kesuan%9]
        self.jlist['定大将']=dingsuan%10 if dingsuan%10!=0 else s9[dingsuan%9]
        zd = self.jlist['主大将']
        kd = self.jlist['客大将']
        dd = self.jlist['定大将']
        self.jlist['主参将']=3*zd%10 if  3*zd%10!=0 else  s9[3*zd%9]
        self.jlist['客参将']=3*kd%10  if  3*kd%10!=0 else   s9[3*kd%9]
        self.jlist['定参将']=3*dd%10 if 3*dd%10!=0 else s9[3*dd%9]
        
        self.np.pan[self.jlist['主大将']] ['将表'].append('主大将')
        self.np.pan[self.jlist['客大将']] ['将表'].append('客大将')
        self.np.pan[self.jlist['定大将']] ['将表'].append('定大将')
        self.np.pan[self.jlist['主参将']] ['将表'].append('主参将')
        self.np.pan[self.jlist['客参将']] ['将表'].append('客参将')
        self.np.pan[self.jlist['定参将']] ['将表'].append('定参将')
        self.jushu = num%72 if num%72!=0 else 72
        self.yy = yy
        self.jishu = num
        
    def sanji(self,name,num):
        zhi=['午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳']
        jd={'君基':ModList([(x,y) for x in zhi for y in range(1,31)]),
           '臣基':ModList([(x,y) for x in zhi for y in range(1,4)]),
           '民基':ModList(zhi).rerange('戌')}
        return jd[name].get(249+num)
    
    def shen(self,name,num):
        chen=ModList(['亥', '午', '寅', '卯', '辰','酉', '申', '子', '巳','戌','未','丑'])
        jd={'四神':ModList([(x,y) for x in chen for y in range(1,4)]),
           '天乙':ModList([(x,y) for x in chen.rerange('酉') for y in range(1,4)]),
           '地乙':ModList([(x,y) for x in chen.rerange('巳') for y in range(1,4)]),
           '直符':ModList([(x,y) for x in chen.rerange('辰') for y in range(1,4)])}
        return jd[name].get(num-1)
    
    def paipan2(self,num):
        junji  =self.sanji('君基',num)
        chenji =self.sanji('臣基',num)
        minji  =self.sanji('民基',num)
        sishen =self.shen('四神',num)
        tianyi =self.shen('天乙',num)
        diyi   =self.shen('地乙',num)
        zhifu  =self.shen('直符',num)
        wufu = ModList([(x,y) for x in [1,3,9,7,5] for y in range(1,46)]).get(num+114)
        
        self.shenjilist['君基']=junji
        self.shenjilist['臣基']=chenji
        self.shenjilist['民基']=minji
        self.shenjilist['四神']=sishen
        self.shenjilist['天乙']=tianyi
        self.shenjilist['地乙']=diyi
        self.shenjilist['直符']=zhifu
        self.shenjilist['五福']=wufu
        
        self.wp.pan[junji[0]]['神基表'].append('君基'+str(junji[1]))
        self.wp.pan[chenji[0]]['神基表'].append('臣基'+str(chenji[1]))
        self.wp.pan[minji]['神基表'].append('民基')
        self.wp.pan[sishen[0]]['神基表'].append('四神'+str(sishen[1]))
        self.wp.pan[tianyi[0]]['神基表'].append('天乙'+str(tianyi[1]))
        self.wp.pan[diyi[0]]['神基表'].append('地乙'+str(diyi[1]))
        self.wp.pan[zhifu[0]]['神基表'].append('直符'+str(zhifu[1]))
        self.np.pan[wufu[0]]['将表'].append('五福'+str(wufu[1]))
    


        
#-----------------------以下是遁甲---------------------------------
class DunJia(TDpan):
    Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])
    Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
    JieQi = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
    dpgan ='戊己庚辛壬癸丁丙乙'
    yongju={'冬至': {'上元': (1, 0), '下元': (4, 0), '中元': (7, 0)},
         '小寒': {'上元': (2, 0), '下元': (5, 0), '中元': (8, 0)},
         '大寒': {'上元': (3, 0), '下元': (6, 0), '中元': (9, 0)},
         '立春': {'上元': (8, 0), '下元': (2, 0), '中元': (5, 0)},
         '雨水': {'上元': (9, 0), '下元': (3, 0), '中元': (6, 0)},
         '惊蛰': {'上元': (1, 0), '下元': (4, 0), '中元': (7, 0)},
         '春分': {'上元': (3, 0), '下元': (6, 0), '中元': (9, 0)},
         '清明': {'上元': (4, 0), '下元': (7, 0), '中元': (1, 0)},
         '谷雨': {'上元': (5, 0), '下元': (8, 0), '中元': (2, 0)},
         '立夏': {'上元': (4, 0), '下元': (7, 0), '中元': (1, 0)},
         '小满': {'上元': (5, 0), '下元': (8, 0), '中元': (2, 0)},
         '芒种': {'上元': (6, 0), '下元': (9, 0), '中元': (3, 0)},
         '夏至': {'上元': (9, 1), '下元': (6, 1), '中元': (3, 1)},
         '小暑': {'上元': (8, 1), '下元': (5, 1), '中元': (2, 1)},
         '大暑': {'上元': (7, 1), '下元': (4, 1), '中元': (1, 1)},
         '立秋': {'上元': (2, 1), '下元': (8, 1), '中元': (5, 1)},
         '处暑': {'上元': (1, 1), '下元': (7, 1), '中元': (4, 1)},
         '白露': {'上元': (9, 1), '下元': (6, 1), '中元': (3, 1)},
         '秋分': {'上元': (7, 1), '下元': (4, 1), '中元': (1, 1)},
         '寒露': {'上元': (6, 1), '下元': (3, 1), '中元': (9, 1)},
         '霜降': {'上元': (5, 1), '下元': (2, 1), '中元': (8, 1)},
         '立冬': {'上元': (6, 1), '下元': (3, 1), '中元': (9, 1)},
         '小雪': {'上元': (5, 1), '下元': (2, 1), '中元': (8, 1)},
         '大雪': {'上元': (4, 1), '下元': (1, 1), '中元': (7, 1)}}
    def __init__(self):
        JZ=ModList([self.Gan.get(i)+self.Zhi.get(i) for i in range(60)])
        self.yuanlist=OrderedDict(zip(JZ,(['上元']*5+['中元']*5+['下元']*5)*4))
        self.shunxu = ModList([1,8,3,4,9,2,7,6,5])
        super().__init__(range(1,10),'卦名','坎坤震巽中乾兑艮离')
        super().addv('宫干','戊己庚辛壬癸丁丙乙')
        super().addv('九星',['蓬柄杓','芮玄戈','冲摇光','辅开阳','禽天衡','心天权','柱天玑','任天璇','英天枢'])
        # self.pan = self.pan.items().sort(by=lambda x:self.shunxu.index(x[0]))
        self.pan = OrderedDict(sorted(self.pan.items(),key=lambda x:self.shunxu.index(x[0])))
        self.zhonggong = self.pan.pop(5)
        self.addv('八门','休生伤杜景死惊开')
        self.shen=ModList(['值符','腾蛇','太阴','六合','白虎','玄武','九地','九天'])
        
        
    def junum(self,jiazi,jieqi):
        return self.yongju[self.JieQi[jieqi]][self.yuanlist[jiazi]]
    
    @classmethod
    def xunshou(cls,jiazi):
        xunshou = "戊己庚辛壬癸"[(cls.Gan.index(jiazi[0])-cls.Zhi.index(jiazi[1]))%12//2]
        return xunshou
    
    def mk_dipan(self,jn,yy,jigong=0):
        dpgan=self.dpgan
        tmp = ModList(self.dpgan).rerange(dpgan[-jn+1])
        pl = tmp.reverse().rerange(dpgan[jn-1]) if yy else tmp
        dipan = TDpan(range(1,10),'宫干',pl)
        dipan.pan = OrderedDict(sorted(dipan.pan.items(),key=lambda x:self.shunxu.index(x[0])))
        zg = dipan.pan.pop(5)
        
        self.jg = 8 if (yy and jigong) else 2
        
        #dipan.pan[self.jg]['宫干']=dipan.pan[self.jg]['宫干']+zg['宫干']
        
        jiuxing = [self.pan[x]['九星'] for x in dipan.pan]
        dipan.addv('九星',jiuxing)
        dipan.pan[self.jg]['九星']+='/禽'
        
        #bamen = [self.pan[x]['八门'] for x in dipan.pan]
        #dipan.addv('八门',bamen)
        return dipan,zg

    def tian_pan(self,dipan,jiazi):
        shigan=jiazi[0]
        xs = DunJia.xunshou(jiazi)
        shigan = xs if shigan=='甲' else shigan
        for gong in dipan.get_name('宫干'):
            xs = gong if xs in gong else xs
            shigan=gong if shigan in gong else shigan
        
        luogong = dipan.rev_get('宫干')[shigan]['index']
        dipan.addv('天盘',dipan.get_name('宫干').rerange(xs),loc=luogong)
        for x in dipan.pan:
            dipan.pan[x]['天盘星']=dipan.pan[dipan.rev_get('宫干')[dipan.pan[x]['天盘']]['index']]['九星']
            
        return dipan.pan[luogong]['天盘星'],luogong
        
    def bamen_pan(self,dipan,zg,jiazi,yy):
        shigan=jiazi[0]
        
        xs = DunJia.xunshou(jiazi)
        shigan = xs if shigan=='甲' else shigan
        
        men = dipan.rev_get('宫干')[xs]['index'] if xs not in zg['宫干'] else 5
        sn = -1 if yy else 1
        step = (sn*self.Gan.index(shigan)+men)%9
        step = step if step else 9
        if step == 5:
            g = zg['宫干']
            tom = dipan.rev_get('宫干')
            for x in tom:
                step = tom[x]['index'] if (g in x) else step
        zs =self.pan[men]['八门'] if men!=5 else self.pan[self.jg]['八门']
        bm = self.get_name('八门').rerange(zs)
        dipan.addv('八门',bm,loc=step)
        return zs,step
    
    def bashen_pan(self,dipan,jiazi,yy):
        shigan=jiazi[0]
        xs = DunJia.xunshou(jiazi)
        shigan = xs if shigan=='甲' else shigan
        for gong in dipan.get_name('宫干'):
            xs = gong if xs in gong else xs
            shigan=gong if shigan in gong else shigan
            
        luogong=dipan.rev_get('天盘')[xs]['index'] if xs not in zg['宫干'] 
        shen = self.shen.reverse().rerange('值符') if yy else self.shen
        dipan.addv('八神',shen,loc=luogong)
        return dipan
    
    def paipan(self,riGZ,jq,shiGZ):
        shigan=shiGZ[0]
        xs = DunJia.xunshou(shiGZ)
        junum,yy=self.junum(riGZ,jq)
        dipan,zg = self.mk_dipan(junum,yy)
        zhishi,zslg=self.tian_pan(dipan,shiGZ)
        zhifu,zflg=self.bamen_pan(dipan,zg,shiGZ,yy)
        self.bashen_pan(dipan,shiGZ,yy)
        
        for gong in dipan.get_name('宫干'):
            xs = gong if xs in gong else xs
            shigan=gong if shigan in gong else shigan
        return dipan,zhishi,zslg,zhifu,zflg,junum,yy
        
        
#-----------------------以上是三式---------------------------------
#-----------------------以下是神煞----------------------------------

class ShenSha(TDpan):
    def __init__(self,gz=0):
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        self.gan=OrderedDict(zip(Gan,[{'禄': '寅'},{'禄': '卯'},{'禄': '巳'},{'禄': '午'},{'禄': '巳'},{'禄': '午'},{'禄': '申'},{'禄': '酉'},{'禄': '亥'},{'禄': '子'}]))
        self.zhi=OrderedDict(zip(Zhi,[{'驿马': '寅'},{'驿马': '亥'},{'驿马': '申'},{'驿马': '巳'},{'驿马': '寅'},{'驿马': '亥'},{'驿马': '申'},{'驿马': '巳'},{'驿马': '寅'},{'驿马': '亥'},{'驿马': '申'},{'驿马': '巳'}]))
        self.pan=self.gan if gz==0 else self.zhi
        self.gz=Zhi+Gan
    
    def gan_sha(self,gan,sha=''):
        return self.gan[gan] if sha=='' else self.gan[gan][sha]
    
    def zhi_sha(self,zhi,sha=''):
        return self.zhi[zhi] if sha=='' else self.zhi[zhi][sha]
    
    def add_gansha(self,name,lst):
        tmp=self.pan
        self.pan=self.gan
        super().addv(name,lst)
        self.pan=tmp
        
    def add_zhisha(self,name,lst):
        tmp=self.pan
        self.pan=self.zhi
        super().addv(name,lst)
        self.pan=tmp
    
    def give_gansha(self,gan):
        tmp=self.gan_sha(gan)
        out=dict()
        for x in self.gz:
            out[x]=[]
            for ss in tmp.keys():
                if tmp[ss]==x:
                    out[x].append(ss)
        return out
    
    def give_zhisha(self,zhi):
        tmp=self.zhi_sha(zhi)
        out=dict()
        for x in self.gz:
            out[x]=[]
            for ss in tmp.keys():
                if tmp[ss]==x:
                    out[x].append(ss)
        return out

class RiSha(ShenSha):
    def addin(self):
        gdf=pd.read_csv('gansha.csv')
        zdf=pd.read_csv('zhisha.csv')
        gdf.apply(lambda x:self.add_gansha(x['name'],x['order']*x['mult']),axis=1)
        zdf.apply(lambda x:self.add_zhisha(x['name'],x['order']*x['mult']),axis=1)
        
    
    def give_zhangsheng(self,gan,mode=0):
        #0不分阴阳火土同,1分阴阳火土同,2不分阴阳水土同,3分阴阳水土同
        zs=ModList(['长生','沐浴','冠带','临官','帝旺','衰','病','死','墓','绝','胎','养'])
        Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
        xs={
        '甲':[dict(zip(Zhi.rerange('亥'),zs))]*4,
        '乙':[dict(zip(Zhi.rerange('亥'),zs)),dict(zip(Zhi.reverse().rerange('午'),zs))]*2,
        '丙':[dict(zip(Zhi.rerange('寅'),zs))]*4,
        '丁':[dict(zip(Zhi.rerange('寅'),zs)),dict(zip(Zhi.reverse().rerange('酉'),zs))]*2,
        '戊':[dict(zip(Zhi.rerange('寅'),zs)),dict(zip(Zhi.rerange('寅'),zs)),dict(zip(Zhi.rerange('申'),zs)),dict(zip(Zhi.rerange('申'),zs))],
        '己':[dict(zip(Zhi.rerange('寅'),zs)),dict(zip(Zhi.reverse().rerange('酉'),zs)),dict(zip(Zhi.rerange('申'),zs)),dict(zip(Zhi.reverse().rerange('卯'),zs))],
        '庚':[dict(zip(Zhi.rerange('巳'),zs))]*4,
        '辛':[dict(zip(Zhi.rerange('巳'),zs)),dict(zip(Zhi.reverse().rerange('子'),zs))]*2,
        '壬':[dict(zip(Zhi.rerange('申'),zs))]*4,
        '癸':[dict(zip(Zhi.rerange('申'),zs)),dict(zip(Zhi.reverse().rerange('卯'),zs))]*2}
        return xs[gan][mode]
        
    
    def give_sha(self,gan,zhi,mode=0):
        self.addin()
        Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸","空","亡"]).rerange(gan)
        Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]).rerange(zhi)
        jz = ModList([Gan[i]+Zhi[i] for i in range(12)])
        gs=self.give_gansha(gan)
        gs['甲'].append('旬仪')
        gs['癸'].append('闭口')
        gs['丁'].append('丁马')
        gs['庚'].append('响动')
        zs=self.give_zhisha(zhi)
        out = {}
        xq=""
        zhangsheng=self.give_zhangsheng(gan,mode)
        for x in zhangsheng:
            zs[x].append('日'+zhangsheng[x])
        for idx in jz:
            out[idx] = zs[idx[1]]+gs[idx[1]]
            if idx[0]!='空' and idx[0]!='亡':
                out[idx].extend(gs[idx[0]])
            if idx[0]=='甲':
                xs = idx
        xq = {'甲子':'亡亥','甲戌':'乙亥','甲申':'戊子','甲午':'庚子','甲辰':'癸丑','甲寅':'亡丑'}
        out[xq[xs]].append('旬奇')
        
        if mode:
            return out
        else:
            for x in out.copy():
                out[x[1]]=out[x]
                out.pop(x)
            return out
    
class YueSha(ShenSha):
    def __init__(self):
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥","子", "丑"]
        
        self.zhi=OrderedDict(zip(Zhi,[{'月破':x} for x in ModList(Zhi).rerange('申')]))
        self.pan=self.zhi
        self.gz=Zhi+Gan
        
        
    def addin(self,file='yue_zhisha.csv'):
        # gdf=pd.read_csv('yue_gansha.csv')
        zdf=pd.read_csv(file)
        # gdf.apply(lambda x:self.add_gansha(x['name'],x['order']*x['mult']),axis=1)
        zdf.apply(lambda x:self.add_zhisha(x['name'],x['order']*x['mult']),axis=1)
        
    def give_sha(self,zhi,mode=0):
        self.addin()
        Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]).rerange(zhi)
        zs=self.give_zhisha(zhi)
        out = {}
        for idx in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]:
            out[idx] = zs[idx]
        
        return out
    
class NianSha(YueSha):
    def __init__(self):
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑","寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",]
        
        self.zhi=OrderedDict(zip(Zhi,[{'岁破':x} for x in ModList(Zhi).rerange('午')]))
        self.pan=self.zhi
        self.gz=Zhi+Gan
        
        
    def addin(self,file='nian_zhisha.csv'):
        super().addin(file)
