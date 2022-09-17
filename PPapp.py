import streamlit as st
import pendulum as pdlm
from PaiPan import paipan_csh,HePan,xingnian
from SanShi import RiSha,YueSha,NianSha,ModList
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder,ColumnsAutoSizeMode
from HuangJi import cegui_shu,gz2gua,bian_gua,najia_G,najia_Z

st.set_page_config(layout="wide",page_title="嘿喵排盘")

JieQi = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
Gan = ModList(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])
Zhi = ModList(["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"])
JiaZi = ModList([Gan.get(i)+Zhi.get(i) for i in range(60)])

grff = ['甲戊庚牛羊','甲羊戊庚牛']
def change6r():
    hp.add_6r(gr=grff.index(st.session_state['choice']))
    

with st.sidebar:
    pp_date=st.date_input("排盘日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time=st.time_input("排盘时间",pdlm.now(tz='Asia/Shanghai').time())
    pp_bm = st.selectbox('本命',JiaZi,index=3)
    pp_nn = st.selectbox('性别',['乾','坤'],index=0)
    
    # btn1=st.button('排盘')
    # if btn1:
    #     pdd = pdlm.datetime(pp_date.year,pp_date.month,pp_date.day,pp_time.hour,pp_time.minute)
    op = st.selectbox('贵人方法',grff,index=0)
    


bazi1,bazi2,jq,yuejiang,tyjs = paipan_csh(pp_date,pp_time)
hp = HePan([bazi1,bazi2],jq,yuejiang,tyjs)
hp.add_6r(gr=grff.index(op))
hp.add_ty()
hp.add_dj()
xngn = xingnian(pp_bm,{'乾':1,'坤':0}[pp_nn],pp_date)

with st.sidebar:    
    st.write(
        pd.DataFrame({
         '年柱': [bazi1['年'][0]+'\n'+(str(najia_G[bazi1['年'][0]])),bazi1['年'][1]+'\n'+(str(najia_Z[bazi1['年'][1]]))],
         '月柱': [bazi1['月'][0]+'\n'+(str(najia_G[bazi1['月'][0]])),bazi1['月'][1]+'\n'+(str(najia_Z[bazi1['月'][1]]))],
         '日柱': [bazi1['日'][0]+'\n'+(str(najia_G[bazi1['日'][0]])),bazi1['日'][1]+'\n'+(str(najia_Z[bazi1['日'][1]]))],
         '时柱': [bazi1['时'][0]+'\n'+(str(najia_G[bazi1['时'][0]])),bazi1['时'][1]+'\n'+(str(najia_Z[bazi1['时'][1]]))],
         '行年': [xngn[0]+'\n'+(str(najia_G[xngn[0]])),xngn[1]+'\n'+(str(najia_Z[xngn[1]]))]},index=['干','支']))
    
    st.write(f"节气:{JieQi[jq]},月将:{yuejiang}")
    st.write(f"太乙局数：{'阴' if hp.ty.yy else '阳'}{hp.ty.jushu},遁甲局数：{'阴' if hp.djn_yy else '阳'}{hp.djn}")
    typ = HePan([bazi1,bazi2],jq,yuejiang,paipan_csh(sj=0)[-1])
    typ.add_ty()
    st.write(typ.ty.jlist)
    
    
    
    

co_name=['巽辰卯寅艮',['巳',4,3,8,'丑'],['午',9,'中',1,'子'],['未',2,7,6,'亥'],'坤申酉戌乾']
def mk_df(hp):
    df = pd.DataFrame(hp.pan)
    df.loc['乙盘神']=df.loc['乙盘神'].apply(lambda x:",".join(x))
    df.loc['乙盘将']=df.loc['乙盘将'].apply(lambda x:",".join(x))
    df.columns=[str(x) for x in df.columns]
    df.loc['上神']=df.fillna('').apply(lambda x:str(x.loc['天遁'])+str(x.loc['天盘']))
    df.loc['宫位']=df.fillna('').apply(lambda x:x.loc['地遁']+x.name if (x.loc['地遁']+x.name) not in "123456789" else x.loc['甲盘'])
    return df

st.write('皇极纳甲:',gz2gua(bazi1),'变',bian_gua(*gz2gua(bazi1)),'轨数：',cegui_shu(*gz2gua(bazi1),gxh=1,cgxh=1),'策数：',cegui_shu(*gz2gua(bazi1),gxh=0,cgxh=0))

tdp,lrp,qmp,test = st.tabs([' 合盘 ',' 六壬 ',' 奇门 ','测试'])


with tdp:
    df = mk_df(hp)
    tf = pd.DataFrame()
    for x in df.columns:
        dx=df[x].fillna('')
        tianjiang = dx['天将']+dx['八神']
        tianpan = dx['上神']
        dipan = dx['宫位']
        men = dx['类象']+dx['八门']
        xing = dx['九星']+dx['六亲']
        ypj =dx['乙盘将']
        yps = dx['乙盘神']
        tf[x]=pd.Series([tianpan,dipan,tianjiang,men,xing,ypj,yps])

    
    tyinfo = []
    tyj = hp.ty.jlist
    for x in list(tyj.keys()):
        word = tyj[x]
        dd = lambda x : hp.ty.wp.pan[tyj[x]]['入宫'] if tyj[x] in hp.ty.wp.pan else ''
        if x == '太乙':
            tyg = hp.ty.np.pan[word[0]]['卦名']
            tyinfo.append("**太乙**："+tyg+str(word[0])+word[1]+";  ")
        else:
            
            tyinfo.append(f"**{x}**:{word}{dd(x)};")
#         else:
#             tyinfo.append(f"**{x}**:{word};")
            
    st.write(*tyinfo)
    row_grp = ["巽 巳 午 未 坤",
                "辰 4 9 2 申",
                "卯 3 中 7 酉",
                "寅 8 1 6 戌",
                "艮 丑 子 亥 乾"]
    for grp in row_grp:
        gg = tf[grp.split()]
        gopnb = GridOptionsBuilder.from_dataframe(gg)
        gopnb.configure_default_column(lockVisible=True,suppressMovable=True)

        stgr = [x for x in grp.split() if x in "123456789"]
        gopnb.configure_columns(column_names=stgr,cellStyle={'backgroundColor': '#cc99cc'})

        grid_options = gopnb.build()
        ag = AgGrid(gg,grid_options,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW )

    

with lrp:
    lr_con=st.container()
    col_l,col_r1,col_r2 = lr_con.columns(3)
    
    rs=RiSha()
    ys = YueSha()
    ns = NianSha()
    ns.addin()
    ys.addin()
    hs={}
    for x in '子丑寅卯辰巳午未申酉戌亥':
        hs[x] =  rs.give_sha(*bazi1['日'])[x]+ys.give_sha(bazi1['月'][1])[x]+ns.give_sha(bazi1['年'][1])[x]
    
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
    
            
    with col_l:
        for x in chuan:

            st.write(x[1]['六亲'],"  ",f"_{x[1]['天盘遁干']}_",f"**{x[1]['天盘']}**",
                     x[1]['天将'],f":{x[1]['将临类象']}；；",",".join(hp.get(x[0],'乙盘将')),",".join(hp.get(x[0],'乙盘神')))

        st.caption(hp.ke_name+","+hp.lr.get_pj()+","+hp.chuan_name)
        tjname=dict(zip(['贵人', '腾蛇', '朱雀', '六合', '勾陈', '青龙', '天空', '白虎', '太常', '玄武', '太阴', '天后'],"贵蛇雀合勾龙空虎常玄阴后"))
        st.write(*[tjname[ke[1]['天将']] for ke in hp.sk][-1::-1])
        st.write(*[ke[1]['天盘'] for ke in hp.sk][-1::-1])
        st.write(*[ke[0] for ke in hp.sk[-1::-1]])
    
        
    
    with col_r1:
        st.text(hp.write_lr())
    with col_r2.expander('神煞'):
        for x in "子丑寅卯辰巳午未申酉戌亥":
            st.write(f"**{x}**",','.join(hs[x]))
    
    row_grp=["巳 午 未 申",
            "辰 巽 坤 酉",
            "卯 艮 乾 戌",
            "寅 丑 子 亥"]
    for grp in row_grp:
        gg = df[grp.split()].loc[kw]
        gopnb = GridOptionsBuilder.from_dataframe(gg)
        gopnb.configure_default_column(lockVisible=True,suppressMovable=True)
        xx=[x for x in grp if x in xngn+pp_bm]
                
        gopnb.configure_columns(column_names=xx,cellStyle={'backgroundColor': '#9F79EE'})
        nms = [x.split() for x in grp]
        tmp =[]
        nms = [tmp.extend(x) for x in nms]
        gopnb.configure_columns(column_names=tmp,headerName='')

        grid_options = gopnb.build()
        ag = AgGrid(gg,grid_options,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW )


with qmp:
    df = mk_df(hp)
    st.write(f"值使:{hp.zhishi+str(hp.zslg)}",f"值符:{hp.zhifu +str(hp.zflg)}")
    kw = ['九星','八神','上神','宫位','八门','乙盘将','乙盘神']
    row_grp=["4 9 2",
            "3 中 7",
            "8 1 6"]

    for grp in row_grp:
        gg = df[grp.split()].loc[kw]
        gopnb = GridOptionsBuilder.from_dataframe(gg)
        gopnb.configure_default_column(lockVisible=True,suppressMovable=True)
        


        grid_options = gopnb.build()
        ag = AgGrid(gg,grid_options,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW )


with test:
    st.text(hp.write_lr())
        
    


   
