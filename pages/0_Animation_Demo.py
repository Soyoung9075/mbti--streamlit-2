
import numpy as np
import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="MBTI 통계", page_icon="📹")
st.markdown("# MBTI 통계")
st.sidebar.header("MBTI 통계")


url = "https://github.com/Soyoung9075/mbti--streamlit/raw/main/MBTI_MATCHING.xlsx"
response = requests.get(url)
response.raise_for_status()

data = pd.read_excel(BytesIO(response.content), sheet_name= "Sheet2")


# 가장 많은 MBTI
df_grouped = data.groupby('mbti')['Name'].count().reset_index()
max_number = df_grouped['Name'].max()
most_freq_mbti = df_grouped.loc[df_grouped['Name'] == max_number]['mbti'].tolist()
def list_to_str(mbti_list):
    # Join the elements of the list into a single string separated by commas
    return ', '.join(mbti_list)

# 가장 적은 MBTI
min_number = df_grouped['Name'].min()
least_freq_mbti = df_grouped.loc[df_grouped['Name'] == min_number]['mbti'].tolist()


with st.container(border = True):

    st.metric(label = "가장 많은 MBTI", value = list_to_str(most_freq_mbti)) 
    st.metric(label = "가장 적은 MBTI", value = list_to_str(least_freq_mbti))

data['Type_1']=data['mbti'].str[0]
data['Type_2']=data['mbti'].str[1]
data['Type_3']=data['mbti'].str[2]
data['Type_4']=data['mbti'].str[3]
data['Type_5'] = data['Type_2'] + data['Type_3']

def mbti_type_plot(data, Type, y_label):
    
    df_type = data.groupby(Type)['mbti'].count().reset_index()
    df_type.columns = ['Type', 'Count']

    fig = px.bar(df_type, x = "Type", y = "Count",
          labels={"Count": "Count","Type": y_label},
          template="simple_white")
    fig.update_layout(width=500, height= 300)
    colors = ['red' if val > 16 else 'green' for val in df_type['Count']] 
    fig.update_traces(marker_color=colors)
    return fig

col1, col2 = st.columns(2)

with col1 : 
    col1.plotly_chart(mbti_type_plot(data, 'Type_1', 'E vs I'), use_container_width=True, height = 5)

with col2 :
    col2.plotly_chart(mbti_type_plot(data, 'Type_2', 'N vs S'), use_container_width=True)

col3, col4 = st.columns(2)

with col3 :
    col3.plotly_chart(mbti_type_plot(data, 'Type_3', 'F vs T'),use_container_width=True)

with col4 :
    col4.plotly_chart(mbti_type_plot(data, 'Type_4', 'P vs J'),use_container_width=True)
    
        