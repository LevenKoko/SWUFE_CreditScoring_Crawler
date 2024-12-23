import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)


refresh_interval = 30 * 1000
st_autorefresh(interval=refresh_interval, key="data_refresh")

# 设置网页标题
st.title('金融科技建模大赛——最新分展示')
st.markdown("比赛地址：[点击跳转](https://match.creditscoring.cn/#/SingleItem?id=21)")
st.text('站点收集了从12月9日17时30分开始的提交数据。')
st.text('高亮的行表示了个人历史最高成绩高于最新成绩的选手。 ')
st.markdown('---')
st.markdown('**upd 12.23 12:03** - 比赛已截止，爬虫后端停止运行。')


def highlight_greater(s):
    return ['background-color: yellow' if s['maxScore'] > s['newScore'] + 5e-5 else '' for _ in s]

df = pd.read_csv('./data/new.csv')
styled_df = df.style.apply(highlight_greater, axis=1)

st.dataframe(
    styled_df,
    column_config={
        "listScore": st.column_config.LineChartColumn(
            "History Scores", y_min=0.7777777, y_max=0.799999
        ),
    },
    height=1500,
    width=1400,
    hide_index=True,
)