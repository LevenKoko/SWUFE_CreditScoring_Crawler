import streamlit as st
import pandas as pd

# markdown
st.markdown('最新分展示')

# 设置网页标题
st.title('金融科技建模大赛——最新分展示')

def highlight_greater(s):
    return ['background-color: yellow' if s['maxScore'] > s['newScore'] + 5e-5 else '' for _ in s]

df = pd.read_csv('./new.csv')
styled_df = df.style.apply(highlight_greater, axis=1)

st.table(styled_df)