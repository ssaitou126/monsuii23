import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import streamlit as st
import lxml
import json

# 年月日時設定
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(tzinfo=None)
nowday = now.strftime('%Y%m01')
nowyear = now.strftime('%Y')
thismonth = datetime.datetime(now.year, now.month, 1)
lastmonth = thismonth + datetime.timedelta(days=-1)
lastday = lastmonth.strftime('%Y%m01')
diff = now-thismonth
difday = diff.days
difsec = diff.seconds
diftime = int((difday*24)+(difsec/60/60))

# 河川名リスト
url = json.load(open('urls.json','r'))
rivernamelist = [
    url['junisyo'],url['ougida'],url['takanosu'],url['futatui'],url['yonaisawa'],url['osarube']
    ]

# 月日数設定
mnlst31 = ['01','03','05','07','08','10','12']
mnlst30 = ['04','06','09','11']
mnlst28 = ['02']

# 月日数設定関数
def setday(whm):
    mnpat = whm[4:6]
    if mnpat in mnlst31:
        dysnum = 31
    elif mnpat in mnlst30:
        dysnum = 30
    elif mnpat in mnlst28:
        dysnum = 28
    else:
        pass
    return dysnum

# ラジオボタンの設定
monthselector = st.sidebar.radio('月選択',('今月','先月'))
if monthselector == '今月':
    activelist = [i.replace('datelabel',nowday).replace('yearlabel' ,nowyear) for i in rivernamelist]
    dys = setday(nowday)
    idx = diftime-1
elif monthselector == '先月':
    activelist = [i.replace('datelabel',lastday).replace('yearlabel' ,nowyear) for i in rivernamelist]
    dys = setday(lastday)
    idx = dys*24-1

# タイトル
'### 米代川月間水位'

# グラフ描画関数
def grfdrw(z):
    dfs = pd.read_html(z)
    df = dfs[1].iloc[2:dys+2,1:].replace(['^(?![+-]?(?:\d+\.?\d*|\.\d+)).+$'],'NaN',regex=True)
    arr = np.array(df,dtype=float).ravel()
    grf = pd.Series(arr)
    smin = grf.min()
    smax = grf.max()
    if grf[idx] == 'NaN':
        srct = grf[idx-1]
    else :
        srct = grf[idx]
    rivername1 = dfs[0].iloc[1,3]
    rivername2 = dfs[0].iloc[1,1]

    headertxt = f'{rivername1}　{rivername2}  　　最大=　{smax}m　　最小=　{smin}m　　直近=　{srct}m'
    st.write(headertxt)

    x = [*range(0,dys*24)]
    fig = plt.figure(figsize=(10,2))
    plt.plot(grf)
    plt.fill_between(x,grf,smin-0.2,color='c',alpha=0.2)
    plt.xticks(np.arange(0, dys*24, 24),np.arange(1,dys+1))
    plt.ylim(smin-0.2,smax+0.2)
    plt.grid()
    st.pyplot(fig)

# チェックボックスの設定
st.sidebar.write('川選択')
riv1 = st.sidebar.checkbox('十二所')
if riv1 :
    grfdrw(activelist[0])
riv2 = st.sidebar.checkbox('扇田')
if riv2 :
    grfdrw(activelist[1])
riv3 = st.sidebar.checkbox('鷹の巣')
if riv3 :
    grfdrw(activelist[2])
riv4 = st.sidebar.checkbox('二ツ井')
if riv4 :
    grfdrw(activelist[3])
riv5 = st.sidebar.checkbox('米内沢')
if riv5 :
    grfdrw(activelist[4])
riv6 = st.sidebar.checkbox('小猿部川')
if riv6 :
    grfdrw(activelist[5])

# ホームページへのリンク
link1 = '[AyuZyのホームページ](https://sites.google.com/view/ayuzy)'
st.sidebar.markdown(link1, unsafe_allow_html=True)
st.text('※国土交通省水文水質データベースのデータを利用して表示しています')