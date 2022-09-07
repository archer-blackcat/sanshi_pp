import streamlit as st
import pendulum as pdlm
from SanShi import LiuRen,TDpan,ModList,TaiYi,ShenSha,RiSha,YueSha,NianSha,DunJia
from collections import UserList,OrderedDict
from JZMpp import mkLiuRen,get_pan
from PaiPan import paipan_csh
import pandas as pd


JieQi = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]

rs=RiSha()

with st.sidebar:
    pp_date=st.date_input("排盘日期",pdlm.now())
    pp_time=st.time_input("排盘时间",pdlm.now())
    pdd=pdlm.now()
    btn1=st.button('排盘')
    if btn1:
        pdd = pdlm.datetime(pp_date.year,pp_date.month,pp_date.day,pp_time.hour,pp_time.minute)

bazi1,bazi2,jq,yuejiang,tyjs = paipan_csh(pdd)
lr,sk = mkLiuRen(yuejiang,bazi1['时'][1],bazi1['日'][0],bazi1['日'][1],zhouye=(bazi1['时'][1] in "酉戌亥子丑寅"),guiren_plan=1)
dj=DunJia()
djp,b1,b2,b3,b4=dj.paipan(bazi2['日'],jq,bazi2['时'])
ty = TaiYi()
ty.paipan1(tyjs,yy=jq>11)
ty.paipan2(tyjs)

with st.sidebar:    
    st.write(
        pd.DataFrame({
         '年柱': [bazi1['年'][0],bazi1['年'][1]],
         '月柱': [bazi1['月'][0],bazi1['月'][1]],
         '日柱': [bazi1['日'][0],bazi1['日'][1]],
         '时柱': [bazi1['时'][0],bazi1['时'][1]],},index=['干','支']))
    
    st.write({'节气':JieQi[jq],'月将':yuejiang})
    for x in ['主算','客算','定算']:
        st.write(f"{x}:{ty.jlist[x]}")
    
        
    
con0 = st.container()
con1 = st.container()
con2 = st.container()
con3 = st.container()
con4 = st.container()

col00,col01,col02,col03,col04=con0.columns(5)
col10,col11,col12,col13,col14=con1.columns(5)
col20,col21,col22,col23,col24=con2.columns(5)
col30,col31,col32,col33,col34=con3.columns(5)
col40,col41,col42,col43,col44=con4.columns(5)

cols={0:[col00,col01,col02,col03,col04],
      1:[col10,col11,col12,col13,col14],
      2:[col20,col21,col22,col23,col24],
      3:[col30,col31,col32,col33,col34],
      4:[col40,col41,col42,col43,col44]}

qimen_map = {1:(3,2),8:(3,1),3:(2,1),4:(1,1),9:(1,2),2:(1,3),7:(2,3),6:(3,3),5:(2,2)}

zhi_map = dict(zip("子丑寅卯辰巳午未申酉戌亥乾艮巽坤",
                   [(4,2),(4,1),(3,0),(2,0),(1,0),(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(4,3),(4,4),(4,0),(0,0),(0,4)]))

ty2dj=OrderedDict(zip(ty.np.pan.keys(),[1,8,3,4,9,2,7,6,5]))

for gong in djp.pan:
    idx,idy=qimen_map[gong]
    pos = cols[idx][idy]
    ctx = djp.pan[gong]
    pos.write("--------------")
    pos.write(ctx['八神'])
    pos.write(ctx['天盘星'])
    pos.write(ctx['天盘'])
    pos.write(ctx['宫干'])
    pos.write(ctx['八门'])
    pos.write("--------------")
    
for zhi in lr.pan:
    idx,idy = zhi_map[zhi]
    pos = cols[idx][idy]
    ctx = lr.pan[zhi]
    pos.write("--------------")
    # ['天将','天盘遁干','天盘','六亲','地盘遁干']
    pos.write(ctx['天将']+"||"+ctx['六亲'])
    pos.write(ctx['天盘遁干']+ctx['天盘'])
    pos.write(ctx['地盘遁干']+zhi)
    pos.write("--------------")
    
ydx,ydy =qimen_map[ty2dj[ty.jlist['太乙'][0]]]
ypos = cols[ydx][ydy]
ypos.write('太乙/'+ty.jlist['太乙'][1])

for k in ty.jlist:
    if k not in ['太乙','主算','客算','定算']:
        if ty.jlist[k] in zhi_map:
            idx,idy = zhi_map[ty.jlist[k]]
            pos = cols[idx][idy]
            pos.write(k)
            
        if ty.jlist[k] in qimen_map:
            idx,idy = qimen_map[ty2dj[ty.jlist[k]]]
            pos = cols[idx][idy]
            pos.write(k)
            
sjl = ty.shenjilist

for k in sjl:
    if k == '民基':
        sjl['民基']=(sjl['民基'],1)
    if sjl[k][0] in zhi_map:
        idx,idy = zhi_map[sjl[k][0]]
        pos = cols[idx][idy]
        pos.write(k+str(sjl[k][1]))

    if sjl[k][0] in qimen_map:
        idx,idy = qimen_map[ty2dj[sjl[k][0]]]
        pos = cols[idx][idy]
        pos.write(k+str(sjl[k][1]))

   