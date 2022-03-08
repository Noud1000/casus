#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[13]:


color_vaccine_map = {'COM':'rgb(255,0,0)', 'UNK':'rgb(0,255,0)', 'JANSS':'rgb(0,0,255)', 'MOD':'rgb(255,140,0)', 'AZ':'rgb(255,20,147)', 'NVXD' : 'rgb(0,0,0)'}


# In[2]:


st.title('casus 2')


# In[ ]:


st.subheader('data import')


# In[3]:


data = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv')


# In[4]:


data = data.drop(['Region','FirstDoseRefused'], axis=1)
data['NumberDosesReceived'] = data['NumberDosesReceived'].fillna(0)
data['NumberDosesExported'] = data['NumberDosesExported'].fillna(0)
data.drop(data[data['TargetGroup']!= 'ALL'].index, inplace =True)


# In[6]:


data = data.assign(Sum = lambda x: x.groupby('ReportingCountry')["FirstDose"].cumsum())
data = data.assign(TotalFirstDoseVaccinated = lambda x: x.groupby(['YearWeekISO','ReportingCountry'])["Sum"].transform('max'))


# In[26]:


InputCountry = st.sidebar.selectbox('Select Country', ('NL', 'BE', 'DE'))


# In[11]:


CountrySelect = data[data['ReportingCountry']==InputCountry]


# In[12]:


st.dataframe(CountrySelect)


# In[ ]:


st.subheader('verschillende Vaccines')


# In[14]:


fig = px.bar(data_frame = CountrySelect, 
             x ='Vaccine',
             y= 'NumberDosesReceived',
            color = 'Vaccine', color_discrete_map = color_vaccine_map)

#fig.show()
st.write(fig)


# In[34]:


st.subheader('geimporteerd en geëxporteerde doses')


# In[20]:


NumberDoses = st.selectbox('Received/Exported', ('NumberDosesReceived','NumberDosesExported' ))


# In[21]:


fig = px.bar(data_frame = CountrySelect, 
             x ='YearWeekISO',
             y= NumberDoses,
            color='Vaccine', color_discrete_map = color_vaccine_map
            )

#fig.show()
st.write(fig)


# In[24]:


st.subheader('gebruikte vaccinaties')


# In[32]:


NumberOfDose = ['FirstDose', 'SecondDose', 'DoseAdditional1']

slider = st.select_slider('number of dose', options = NumberOfDose )


# In[33]:


fig = px.bar(data_frame = CountrySelect, 
             x ='YearWeekISO',
             y= slider,
            color='Vaccine', color_discrete_map = color_vaccine_map)

#fig.show()
st.write(fig)


# In[ ]:




