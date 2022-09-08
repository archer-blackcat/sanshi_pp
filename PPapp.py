import streamlit as st
import pendulum as pdlm
from PaiPan import paipan_csh,HePan
import pandas as pd
from st_aggrid import AgGrid

st.set_page_config(layout="wide",page_title="嘿喵排盘")

JieQi = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
grff = ['甲戊庚牛羊','甲羊戊庚牛']
def change6r():
    hp.add_6r(gr=grff.index(st.session_state['choice']))
    
st.set_page_config(layout="wide")
with st.sidebar:
    pp_date=st.date_input("排盘日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time=st.time_input("排盘时间",pdlm.now(tz='Asia/Shanghai').time())
    
    # btn1=st.button('排盘')
    # if btn1:
    #     pdd = pdlm.datetime(pp_date.year,pp_date.month,pp_date.day,pp_time.hour,pp_time.minute)
    op = st.selectbox('贵人方法',grff,index=1)
    


bazi1,bazi2,jq,yuejiang,tyjs = paipan_csh(pp_date,pp_time)
hp = HePan([bazi1,bazi2],jq,yuejiang,tyjs)
hp.add_6r(gr=grff.index(op))
hp.add_ty()
hp.add_dj()


with st.sidebar:    
    st.write(
        pd.DataFrame({
         '年柱': [bazi1['年'][0],bazi1['年'][1]],
         '月柱': [bazi1['月'][0],bazi1['月'][1]],
         '日柱': [bazi1['日'][0],bazi1['日'][1]],
         '时柱': [bazi1['时'][0],bazi1['时'][1]],},index=['干','支']))
    
    st.write(f"节气:{JieQi[jq]},月将:{yuejiang}")
    st.write(f"太乙局数：{'阴' if hp.ty.yy else '阳'}{hp.ty.jushu},遁甲局数：{'阴' if hp.djn_yy else '阳'}{hp.djn}")
    
    
    


co_name=['巽辰卯寅艮',['巳',4,3,8,'丑'],['午',9,'中',1,'子'],['未',2,7,6,'亥'],'坤申酉戌乾']
def mk_df(hp):
    df = pd.DataFrame(hp.pan)
    df.loc['乙盘神']=df.loc['乙盘神'].apply(lambda x:",".join(x))
    df.loc['乙盘将']=df.loc['乙盘将'].apply(lambda x:",".join(x))
    df.columns=[str(x) for x in df.columns]
    df.loc['上神']=df.fillna('').apply(lambda x:str(x.loc['天遁'])+str(x.loc['天盘']))
    df.loc['宫位']=df.fillna('').apply(lambda x:x.loc['地遁']+x.name if (x.loc['地遁']+x.name) not in "123456789" else x.loc['甲盘'])
    return df


tdp,lrp,qmp = st.tabs([' 合盘 ',' 六壬 ',' 奇门 '])
with tdp:
    df = mk_df(hp)
    tyinfo = []
    tyj = hp.ty.jlist
    for x in list(tyj.keys())[:10]:
        word = tyj[x]
        if x == '太乙':
            tyg = hp.ty.np.pan[word[0]]['卦名']
            tyinfo.append( "**太乙**："+tyg+word[1]+";  ")
        else:
            tyinfo.append(f"**{x}**:{word};")
            
    st.write(*tyinfo)
    cols = st.columns(5)
    for i in range(5):
        for name in co_name[i]:
            pf = pd.DataFrame(df[str(name)].astype(str)).copy()
            infos = ['上神','宫位']
            
            if name in hp.zhi_p.pan:
                infos += ['天将','六亲']

            if name in hp.gong_p.pan:
                infos += ['八神','八门','九星']
               

            if name == '中':
                pf.loc['值使']=hp.zhishi+str(hp.zslg)
           
                pf.loc['值符']=hp.zhifu +str(hp.zflg)
          
                infos+=['值使','值符']

            pf = pf.loc[infos+['乙盘神','乙盘将']]

            with cols[i]:
                AgGrid(pf)

with lrp:
    tynp = hp.ty.np.pan
    pp = hp.zhi_p.pan
    for x in tynp:
        k = tynp[x]['正宫']
        if k in pp:
            jb=tynp[x]['将表']
            pp[k]['乙盘将']=jb
    df = mk_df(hp)
    kw = ['天将','上神','宫位','类象','乙盘将','乙盘神']
    chuan=hp.chuan
    
   
    for x in chuan:
       
        st.write(x[1]['六亲'],"  ",f"_{x[1]['天盘遁干']}_",f"**{x[1]['天盘']}**",x[1]['天将'],f":{x[1]['将临类象']}；；",",".join(hp.get(x[0],'乙盘将')),",".join(hp.get(x[0],'乙盘神')))
    
    st.caption(hp.ke_name+","+hp.lr.get_pj()+","+hp.chuan_name)
    
    #col_k = st.columns(4)
    # for i in [3,2,1,0]:
    #     with col_k[i]:
    #         ke = hp.sk[i]
    tjname=dict(zip(['贵人', '腾蛇', '朱雀', '六合', '勾陈', '青龙', '天空', '白虎', '太常', '玄武', '太阴', '天后'],"贵蛇雀合勾龙空虎常玄阴后"))
    st.write(*[tjname[ke[1]['天将']] for ke in hp.sk][-1::-1])
    st.write(*[ke[1]['天盘'] for ke in hp.sk][-1::-1])
    st.write(*[ke[0] for ke in hp.sk[-1::-1]])
    

    
    AgGrid(df["巳 午 未 申".split()].loc[kw])
    AgGrid(df["辰 巽 坤 酉".split()].loc[kw])
    AgGrid(df["卯 艮 乾 戌".split()].loc[kw])
    AgGrid(df["寅 丑 子 亥".split()].loc[kw])
    
with qmp:
    st.write(f"值使:{hp.zhishi+str(hp.zslg)}",f"值符:{hp.zhifu +str(hp.zflg)}")
    kw = ['九星','八神','上神','宫位','八门','乙盘将','乙盘神']
    AgGrid(df["4 9 2".split()].loc[kw])
    AgGrid(df["3 中 7".split()].loc[kw])
    AgGrid(df["8 1 6".split()].loc[kw])
#     st.dataframe(df["4 9 2".split()].loc[kw].astype(str),width=600)
#     st.dataframe(df["3 中 7".split()].loc[kw].astype(str),width=600)
#     st.dataframe(df["8 1 6".split()].loc[kw].astype(str),width=600)
    
        
                

        
    


   
