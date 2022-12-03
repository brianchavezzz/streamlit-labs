#----------------Librerías----------------#####
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date

#----------------Page----------------#####
st.set_page_config(layout="wide")

#----------------Archivo BD----------------#####
@st.cache
def read_data():
    bd=pd.read_csv("dbase.csv")
    bd['Fecha']=[(dt.strptime(date,"%d/%m/%Y")) for date in bd['Fecha']]
    bd['Fecha'] = bd['Fecha'].dt.date
    return bd
df=read_data()

with st.container():
    st.title('Dashboard Programas Internacionales')


#----------------SIDEBAR--------------#####

filtro_tipo=(df.groupby(by=["Tipo_intercambio"]).count())
filtro_tipo.reset_index(inplace=True)
filtro_tipo=filtro_tipo[(filtro_tipo['Instancia'] > 100)]

tipo=st.sidebar.multiselect(
    'Selecciona el tipo de intercambio:',
    options=filtro_tipo['Tipo_intercambio'].unique(),
    default=filtro_tipo['Tipo_intercambio'].unique()
)

df_selection=df.query(
    "Tipo_intercambio == @tipo"
)

#---------------CAMPUS---------------
unicampus=df_selection['Campus'].unique()
campus=unicampus.tolist()
campus.insert(0,'Global')
opccampus= st.sidebar.selectbox('Campus',campus)
if opccampus!='Global':
    df_selection = df_selection[df_selection['Campus']==opccampus]
    
#---------------ESCUELAS---------------
uniescuelas=df_selection['Escuela'].unique()
escuelas=uniescuelas.tolist()
escuelas.insert(0,'Global')
escu = st.sidebar.selectbox('Escuela',escuelas)
if escu!='Global':
    df_selection = df_selection[df_selection['Escuela']==escu]

#---------------CARRERAS---------------
unicarreras=df_selection['Programa'].unique()
carreras=unicarreras.tolist()
carreras.insert(0,'Global')
carre = st.sidebar.selectbox('Programa',carreras)
if carre!='Global':
    df_selection = df_selection[df_selection['Programa']==carre]

#---------------CALENDARIO---------------
with st.sidebar.form("test_form"):
    dts = st.date_input(label='Rango de fechas: ',
        value=(min(df_selection["Fecha"]), 
        date.today()),
        min_value=(min(df_selection["Fecha"])),
        max_value=(date.today()),
        key='#date_range')

    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            df_selection=df_selection[(df['Fecha'] > dts[0]) & (df['Fecha'] < dts[1])]
        except:
            pass




#----------------KPIS----------------####

nuevo=round((len(df_selection[df_selection.OpcionAsignada==1])/len(df_selection))*100,2)

promedios=round(df_selection['Promedio'].mean(),2)

porc_int=round((len(df_selection[df_selection.Tipo_intercambio=='INT'])/len(df_selection.Tipo_intercambio))*100,2)

left_column,entre_1,centro,entre_2,right_column=st.columns((7,1,7,1,6))


left_column.markdown("<h1 style='text-align: center; color: black; font-size: 1.4rem;'>Alumnos que van a intercambio tradicional</h1>", unsafe_allow_html=True)
left_column.markdown(f"<h1 style='text-align: center; color: blue; font-size: 2.5rem;'>{porc_int}%</h1>", unsafe_allow_html=True)

centro.markdown("<h1 style='text-align: center; color: black; font-size: 1.4rem;'>Promedio general de los alumnos</h1>", unsafe_allow_html=True)
centro.markdown(f"<h1 style='text-align: center; color: blue; font-size: 2.5rem;'>{promedios}</h1>", unsafe_allow_html=True)

right_column.markdown("<h1 style='text-align: center; color: black; font-size: 1.4rem;'>Alumnos en su primera opción</h1>", unsafe_allow_html=True)
right_column.markdown(f"<h1 style='text-align: center; color: blue; font-size: 2.5rem;'>{nuevo}%</h1>", unsafe_allow_html=True)


    
st.markdown("---")

#----------------GRAFICAS----------------#####



zo,ka=st.columns(2)


#---------------BARRAS TIPO DE INTERCAMBIO---------------
sales_by_product_line=(df_selection.groupby(by=["Tipo_intercambio"]).count()[['Instancia']].sort_values(by='Instancia'))
fig_product_sales=px.bar(sales_by_product_line,y='Instancia', x=sales_by_product_line.index,
    labels={
                     "Tipo_intercambio": "Tipo de intercambio",
                     "Instancia": "Num. de alumnos"
                 })
fig_product_sales.update_layout(width=600, height=400,title={
            'text': "Cantidad de alumnos por tipo de intercambio",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

zo.plotly_chart(fig_product_sales)



#---------------PASTEL OPCION ASIGNADA---------------
poo=(df_selection.groupby(by=['OpcionAsignada']).count()[['Instancia']].sort_values(by='Instancia'))
polar = px.pie(poo, names=poo.index, values='Instancia',color=poo.index,color_discrete_sequence= px.colors.sequential.Teal, hole=.3)
polar.update_traces(textposition='inside')
polar.update_layout(width=600, height=400,uniformtext_minsize=8, uniformtext_mode='hide',
title={
            'text': "Oportunidad asignada de entre las seleccionadas por el alumno",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center'})
ka.plotly_chart(polar)



i,d=st.columns((3,2))


#---------------CUADROS / TREEMAP---------------
tree=df_selection.groupby(['Escuela','Programa']).count().reset_index()
fig34 = px.treemap(tree, path=[px.Constant(""), 'Escuela', 'Programa'], values='Matrícula',
color_discrete_sequence= px.colors.sequential.Turbo)
fig34.update_layout(width=600, height=550,margin = dict(t=50, l=25, r=25, b=25),title={
            'text': "Cantidad de intercambios por Escuela",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center'})
i.plotly_chart(fig34)



#---------------TABLA Ranking---------------

box_ranking= d.selectbox('Ranking por:',('Universidad', 'País'))
if box_ranking=='Universidad':
    d.write("Ranking Universidades más seleccionadas")
    primopcion=(df_selection.groupby(by=["Nombre Oportunidad Asignada"]).count()[['Num. de intercambios']].sort_values(by='Num. de intercambios'))
    primopcion.reset_index(inplace=True)
    primopcion=primopcion.sort_values(by='Num. de intercambios', ascending=False)
    primopcion.index = np.arange(1,len(primopcion)+1)
    d.dataframe(primopcion)
elif box_ranking=='País':
    d.write("Ranking país más seleccionado")
    primopcion=(df_selection.groupby(by=["País"]).count()[['Num. de intercambios']].sort_values(by='Num. de intercambios'))
    primopcion.reset_index(inplace=True)
    primopcion=primopcion.sort_values(by='Num. de intercambios', ascending=False)
    primopcion.index = np.arange(1,len(primopcion)+1)
    d.dataframe(primopcion)

#---------------HISTOGRAMA---------------
histo = px.histogram(df_selection,x="Fecha")
histo.update_layout(width=1100, height=500,bargap=0.2,
title={
     'text': "Histograma: Cantidad de alumnos asignados por fecha",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

st.plotly_chart(histo)


#---------------MAPA--------------------
       
lat={"Monterrey":25.65154787891646,"San Luis Potosí":22.128836043371418,"Santa Fe":19.359224760871147,"Ciudad de México":19.284033938535494,
       "Puebla":19.017713542448195,"EGADE Santa Fe":19.359963066421418,"Estado de México":19.593223695694327,"Sinaloa":24.801188336892775,
       "EGADE Monterrey":25.643685799175376,"Cuernavaca":18.805783131403988,"Chihuahua":28.67398812736935,"Querétaro":20.612905261415108,
       "Guadalajara":20.732383309578545,"Toluca":19.26710014630963,"Laguna":25.517162292362404,"Ciudad Juárez":31.717878786240515,"León":21.167188834814137,
       "Zacatecas":22.76132629769481,"Tampico":22.381448059372147,"Sonora Norte":29.16983780991437,"Saltillo":25.448282063914974,"Aguascalientes":21.93292161150363,
       "Central de Veracruz":18.891898003074434,"Morelia":19.656425228538374,"EGAP Monterrey":25.64407367744958,"EGAP Santa Fe":19.38123738230921,"Irapuato":20.686777014191634,
       "Chiapas":16.76487567827367,"Santa Catarina":25.66126470511286,"Valle Alto":25.570265424335883,
       "Eugenio Garza Sada":25.670347902468986,"Eugenio Garza Lagüera":25.617785064684217,"Cumbres":25.733808679622296,
       "Ciudad Obregón":27.531879279104782,"Ciudad Matamoros":25.91696876277183}

lon={"Monterrey":-100.28953788496757,"San Luis Potosí":-101.04031151253082,"Santa Fe":-99.258756616738,"Ciudad de México":-99.13603300716265,
       "Puebla":-98.2419534750116,"EGADE Santa Fe":-99.25825848401253,"Estado de México":-99.2291539140597,"Sinaloa":-107.42135143589503,
       "EGADE Monterrey":-100.32546966216546,"Cuernavaca":-99.22165071803555,"Chihuahua":-106.07759852483846,"Querétaro":-100.40525202891273,
       "Guadalajara":-103.45417784324322,"Toluca":-99.7057669731565,"Laguna":-103.39747711927167,"Ciudad Juárez":-106.39362396865499,"León":-101.71438773316953,
       "Zacatecas":-102.53548057722183,"Tampico":-97.90163965275813,"Sonora Norte":-110.91047826756976,"Saltillo":-100.97529393983477,"Aguascalientes":-102.33977546333317,
       "Central de Veracruz":-96.97914894862247,"Morelia":-101.16390070614996,"EGAP Monterrey":-100.32539890958138,"EGAP Santa Fe":-99.18669422134872,"Irapuato":-101.39480492049103,
       "Chiapas":-93.20094202878686,"Santa Catarina":-100.43066772378764,"Valle Alto":-100.24967677868463,
       "Eugenio Garza Sada":-100.3567186347237,"Eugenio Garza Lagüera":-100.27501271028787,"Cumbres":-100.41594557753257,
       "Ciudad Obregón":-109.94442547433854,"Ciudad Matamoros":-97.56929747765045}
       
promedio_hotel=df_selection.groupby(by=["Campus"]).count()
promedio_hotel.reset_index(inplace=True)
promedio_hotel["lat"]=promedio_hotel["Campus"].map(lat)
promedio_hotel["lon"]=promedio_hotel["Campus"].map(lon)

mapa = px.scatter_mapbox(promedio_hotel, lat="lat", lon="lon", color='Num. de intercambios',size="Num. de intercambios",
              color_continuous_scale=px.colors.sequential.Bluered,size_max=20, zoom=4,width=1100, height=500)
mapa.update_layout(mapbox_style="open-street-map",title='Mapa: Cantidad de intercambios por campus')
st.plotly_chart(mapa)


#streamlit run 2_reto_individual.py