import streamlit as st
import pandas as pd
import json 
import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine,text
from pandas.io import sql
import pymysql
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu


icon = Image.open("C:\\Users\\vijay\\Downloads\\phonepe_name.jpg")
st.image(icon,caption='Iamge',use_column_width=True)
st.title('Phonepe Pulse Data Visualization')

mytitle2=st.selectbox('***Select***', ['agg_trans', 'agg_user', 'map_trans','map_user','top_trans','top_user'])
st.write('**You selected**:',mytitle2 )

col1, col2 = st.columns(2)
with col1:
    Year = st.selectbox(
        '***Select an option from Year***',
        ('2018', '2019', '2020','2021','2022')
    )

with col2:
    Quarter = st.selectbox(
        '***Select an option from  Quarter***',
        ('1', '2', '3','4')
    )

st.write('You selected:',Year, 'from Year and', Quarter, 'from Quarter.')


fitter_val =st.selectbox('**Select**', ['Transaction_count', 'Transaction_amount','Pincode','Registered_users','Registered_user','App_opens','Count','Amount','Brands','Count','Percentage'])
st.write('**You selected**:',fitter_val )

# mytitle3 =st.selectbox('**Select**', ['Transaction_count','Count'])
# st.write('**You selected**:', mytitle3 )


plots=st.sidebar.radio('Select Plot', ['Scatter Plot'],horizontal=True)

# sumint_val=
sub_botton=st.sidebar.button('Get '+plots)

# agg_user	State	Year	Quarter	Brands	 Count	Percentage
# agg_trans	State	Year	Quarter	Transaction_type	Transaction_count	Transaction_amount
						
# map_trans	State	Year	Quarter	District	Count	Amount
# map_user	State	Year	Quarter	District	Registered_user	App_opens
						
# top_user	State	Year	Quarter	Pincode	Registered_users	
# top_trans	State	Year	Quarter	Pincode	Transaction_count	Transaction_amount



sql=f'select * from {mytitle2} where year={Year} and quarter={Quarter}'

engine = create_engine("mysql+pymysql://root:Gvk886723@localhost:3306/phonepe_pulsar",pool_size=1000, max_overflow=2000)
mysql_df=pd.read_sql_query(sql,engine.connect(), index_col=None,chunksize=None)


st.write(mysql_df)



fig= px.choropleth(
mysql_df,
geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
featureidkey='properties.ST_NM',
locations='State',
# hover_data='Transaction_count',
color=fitter_val,
color_continuous_scale='orRd'
)
fig.update_geos(fitbounds="locations") # To show-up the Indian boundaries
st.plotly_chart(fig)

def scatterplot(mysql_df):
        if fitter_val=='Transaction_type':
            fin_filter_val='Transaction_amount'
        if fitter_val=="Amount":
            fin_filter_val='Amount'
        data = [dict(
            type = 'scatter',
            x = mysql_df['State'],
            y = mysql_df[fin_filter_val],
            mode = 'markers',
            transforms = [dict(
                type = 'groupby',
                groups = mysql_df['State'],
               )]
        )]

        fig_dict = dict(data=data)
        pio.show(fig_dict, validate=False)
        st.plotly_chart(fig_dict)
        
        
mytitle3 = st.selectbox('***Select this if scatter Plot***', mysql_df["State"].unique())
if sub_botton:
    if plots=='Line Graph':
        fig = px.line(mysql_df, x='State', y=fin_filter_val)
        fig.show()
        
        
if sub_botton:
    if plots=='Scatter Plot':
                mysql_df = mysql_df.loc[mysql_df['State'] == mytitle3] 
            
           
#                 mysql_df = mysql_df.query("State" == mytitle3)
                scatterplot(mysql_df)
# mysql_df = mysql_df.loc[mysql_df['State'] == mytitle3]            
 
# df_grouped = mysql_df.groupby('state')['amount'].sum().reset_index() fig = px.scatter(df_grouped, x='state', y='amount')
# #check for caps 'State' st.plotly_chart(fig)

    





  
