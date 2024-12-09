import streamlit as st
import pandas as pd

# markdown
st.markdown('最高分展示')

# 设置网页标题
st.title('金融科技建模大赛——最高分展示')



df = pd.read_csv('./high.csv')
st.table(df)


'''
streamlit run st-demo.py
'''