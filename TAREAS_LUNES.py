#SUBIR ESTA CON SU ARCHIVO CSV
#streamlit run TAREAS_LUNES.py

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

opcion= st.selectbox('SELECCIONAR TAREA: ',('TAREA_2','TAREA_3','TAREA_4'))

if opcion=='TAREA_2':
    url = "https://raw.githubusercontent.com/jeaggo/tc3068/master/Superstore.csv "
    data = pd.read_csv(url)

    st.title('Visualización de analítica de datos para WalMart USA')
    st.subheader('Tema 2')
    st.text('Predicción de ventas de productos de línea blanca en el noroeste de los Estados Unidos. ')

    radio_op=st.radio("Ship Mode:",
            data['Ship Mode'].unique())
    data = data[data["Ship Mode"]==radio_op]

    selectbox_op= st.selectbox('Category',data['Category'].unique())
    data = data[data["Category"]==selectbox_op]

    slider_op = st.slider('Discount:', min(data['Discount']), max(data['Discount']))
    data = data[data["Discount"]==slider_op]

    st.dataframe(data)




if opcion=='TAREA_3':
    url = "https://raw.githubusercontent.com/jeaggo/tc3068/master/Superstore.csv "
    data = pd.read_csv(url)

    st.title('Visualización de analítica de datos para WalMart USA')
    st.subheader('Tema 3')
    st.text('Predicción de ventas de productos de línea blanca en el noroeste de los Estados Unidos. ')

    poo=(data.groupby(by=['Region','Category']).sum()[['Sales']].sort_values(by='Sales'))
    poo=poo.reset_index()
    fig=px.bar(poo, x='Region', y="Sales", color='Category', title="Total de ventas por región")
    st.plotly_chart(fig)

    fig2 = px.pie(data, values='Quantity', names='Ship Mode', title='Cantidad por modo de envío')
    st.plotly_chart(fig2)

    fig3 = px.histogram(data, x="Sub-Category",title='Cantidad de registros por sub-categoría')
    st.plotly_chart(fig3)




if opcion=='TAREA_4':
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



    st.map(data,9,False)


