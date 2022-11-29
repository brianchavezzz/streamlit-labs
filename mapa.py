import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Visualización de Mapas')
st.subheader('Tema 4')
st.text('Viajes de Uber en la ciudad de Nueva York con filtros por hora. ')

@st.cache 

def load_data(nrows): 
        data = pd.read_csv("probartarea3.csv", nrows=nrows) 

        lowercase = lambda x: str(x).lower() 

        data.rename(lowercase, axis='columns', inplace=True) 

        data=data.dropna()

        data['date/time'] = pd.to_datetime(data['date/time']) 

        data["hora"]=[(hora.hour) for hora in data["date/time"]]

        return data 

data = load_data(10000) # probar con 100, 1000, etc


dts = st.slider('Rango de fechas: ',
            0,23,4
            )

data=data[(data['hora'] == dts)]



mapa = px.scatter_mapbox(data, lat="lat", lon="lon",size_max=13, zoom=10,width=900, height=450)
mapa.update_coloraxes(colorbar_tickfont_size=10)
mapa.update_layout(mapbox_style="open-street-map")
mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
st.plotly_chart(mapa)