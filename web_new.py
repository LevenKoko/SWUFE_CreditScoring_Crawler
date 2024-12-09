import streamlit as st
import pandas as pd

# markdown
st.markdown('最新分展示')

# 设置网页标题
st.title('金融科技建模大赛——最新分展示')

df = pd.read_csv('./new.csv')
st.table(df)
