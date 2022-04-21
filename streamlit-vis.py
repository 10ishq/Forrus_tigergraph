
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import json
import pyTigerGraph as tg
from branca import element as b
import folium
import random
import plotly.graph_objects as go

data = {"Gateway":1}
for i in range(30):
    newNode = "Node "+str(i)
    data[newNode] = {
            "Temperature":random.randint(25, 45),
            "Humidity":random.randint(50, 100),
            "Smoke":random.randint(0, 2),
            "Fire":random.randint(0, 2),
            "Location":str(24+random.random())+','+str(44+random.random()),
            "Battery":random.randint(0, 100)
        }
#  print(data["Gateway"]["Node 1"])

# nodes = []
# Temperature = []
# Humidity = []
# Smoke = []
# Fire = []
# Location = []
# Battery = []

# for i in range(30):
#     nodevalue = "Node "+str(i)
#     Temperature.append(data[nodevalue]["Temperature"])
#     Humidity.append(data[nodevalue]["Humidity"])
#     Smoke.append(data[nodevalue]["Smoke"])
#     Fire.append(data[nodevalue]["Fire"])
#     Location.append(data[nodevalue]["Location"])
#     Battery.append(data[nodevalue]["Battery"])

# print(Battery)

graphDomain=''
graphPass=''
if 'graphDomain' not in st.session_state:
    st.session_state['graphDomain']=''
if 'graphPass' not in st.session_state:
    st.session_state['graphPass']=''
if 'networkVisbool' not in st.session_state:
    st.session_state['networkVisbool']='0'
if 'Longi' not in st.session_state:
    st.session_state['Longi']=[]
if 'Lati' not in st.session_state:
    st.session_state['Lati']=[]
if 'coords' not in st.session_state:
    st.session_state['coords']=[]
if 'tempAvgWT' not in st.session_state:
    st.session_state['tempAvgWT']=[]
if 'humAvgWT' not in st.session_state:
    st.session_state['humAvgWT']=[]
if 'battAvgWT' not in st.session_state:
    st.session_state['battAvgWT']=[]
if 'smoke' not in st.session_state:
    st.session_state['smoke']=[]
if 'fire' not in st.session_state:
    st.session_state['fire']=[]
if 'temperature' not in st.session_state:
    st.session_state['temperature']=[]
if 'humidity' not in st.session_state:
    st.session_state['temperature']=[]
if 'battery' not in st.session_state:
    st.session_state['temperature']=[]

selected = option_menu(
        menu_title = "Forrus",
        options =["TigerGraph Connection Setup","Network Visualization", "Heat Map Visualization","Node Dashboard"],
        icons=["gear","diagram-3","geo","bar-chart-fill"],
        menu_icon="tree-fill",
        default_index=0,
        orientation="horizontal"
        
    )
nodes = []
Temperature = []
Humidity = []
Smoke = []
Fire = []
Location = []
Battery = []
Lati=[]
Longi=[]
coords=[]



def connect_to_graph():
    

    print(graphDomain +" "+graphPass)
    conn = tg.TigerGraphConnection(host=graphDomain, password=graphPass, gsqlVersion="3.0.5", useCert=True)
    conn.graphname = "forrus"
    conn.apiToken = conn.getToken(conn.createSecret())
    data={}
    nodes={}
    nodeChild={}

    allData= conn.runInterpretedQuery("""
    INTERPRET QUERY () FOR GRAPH forrus {
    start = {Node.*};
    result= SELECT d FROM start:s -(has_node_data)- Data:d;

    PRINT result;
    }

    """,{})
    dataDic=allData[0]['result']
    # print(type(json.dumps(allData)))
    # print(type(allData))
    for d in dataDic:
        dataNode=str(d['v_id'])
        data[dataNode]=d['attributes']
    print(len(data))
    print((data))

    for i in range(1,len(data)+1):
        Temperature.append(int(data[str(i)]['temperature']))
        Humidity.append(int(data[str(i)]['humidity']))
        Fire.append(int(data[str(i)]['fire']))
        Smoke.append(int(data[str(i)]['smoke']))
        locationSplit=str(data[str(i)]['location']).split(',')
        Lati.append(float(locationSplit[0]))
        Longi.append(float(locationSplit[1]))
        Battery.append(int(data[str(i)]['battery']))
    print(Lati)
    print(Longi)



    dataDic= conn.runInterpretedQuery("""
    INTERPRET QUERY () FOR GRAPH forrus {
        start = {Node.*};
        result= SELECT d FROM start:s -(has_node_data)- Data:d;

    PRINT result;
    }

    """,{})
    dataDic=allData[0]
    dataList=dataDic["result"]
    childs=[]
    # print(type(json.dumps(allData)))
    # print(type(allData))
    for d in dataList:
        dataNode=d['v_id']
        childs.append(dataNode)
    print(sorted(childs))
    
    for i in range(len(childs)):
        latlonlist=[]
        latlonlist.append(Lati[i])
        latlonlist.append(Longi[i])
        coords.append(latlonlist)

        

    print(coords)
    s=0
    for t in (Temperature):
        s=s+t 
    s=s/len(Temperature)
    normalized=[]
    for i in range(len(Temperature)):
        normalized.append(Temperature[i]/s)
    st.session_state.tempAvgWT=normalized

    s=0
    for t in (Humidity):
        s=s+t 
    s=s/len(Humidity)
    normalized=[]
    for i in range(len(Humidity)):
        normalized.append(Humidity[i]/s)
    st.session_state.humAvgWT=normalized

    s=0
    for t in (Battery):
        s=s+t 
    s=s/len(Battery)
    normalized=[]
    for i in range(len(Battery)):
        normalized.append(Battery[i]/s)
    st.session_state.battAvgWT=normalized

    st.session_state.Lati=Lati
    st.session_state.cords=coords
    st.session_state.Longi=Longi
    st.session_state.temperature=Temperature
    st.session_state.humidity=Humidity
    st.session_state.battery=Battery
    st.session_state.fire=Fire
    st.session_state.smoke=Smoke

    

def display_dashboard():
    st.bar_chart[Temperature]



if selected == "TigerGraph Connection Setup":
    st.title(f"You are in {selected}")
    st.session_state.graphDomain= st.text_area("Enter Graph Domain", "")
    graphDomain= st.session_state.graphDomain
    st.markdown(f"my domain is = {graphDomain}")


    st.session_state.graphPass= st.text_area("Enter Graph Password", "")
    graphPass=st.session_state.graphPass
    st.markdown(f"my password is = {graphPass}")

    st.button("Connect to Graph",on_click=connect_to_graph)
    
    
    


if (selected == "Network Visualization" and len(st.session_state.Lati)>0) :
    st.title(f"You are doing {selected}")
    
    st.session_state.networkVisbool='1'
    fig=b.Figure(width=550,height=350)

    fig5=b.Figure(height=550,width=750)
    m=folium.Map(location=[st.session_state.Lati[0], st.session_state.Longi[0]],zoom_start=14)
    #folium.Marker(location=[st.session_state.Lati[1], st.session_state.Longi[1]],popup='Default popup Marker1',tooltip='Click here to see Popup').add_to(m)
    # folium.Marker(location=[st.session_state.Lati[2], st.session_state.Longi[2]],popup='<strong>Marker3</strong>',tooltip='<strong>Click here to see Popup</strong>').add_to(m)
    # folium.Marker(location=[st.session_state.Lati[3], st.session_state.Longi[3]],popup='<h3 style="color:green;">Marker2</h3>',tooltip='<strong>Click here to see Popup</strong>').add_to(m)
    # folium.Marker(location=[st.session_state.Lati[4], st.session_state.Longi[4]],popup='<h3 style="color:green;">Marker2</h3>',tooltip='<strong>Click here to see Popup</strong>').add_to(m)

    coords_1=[[28.695800, 77.244721],[28.645800, 77.214721]]
    coords_2=[[28.695800, 77.244721],[28.655800, 77.274721]]
    # line_1=folium.vector_layers.PolyLine([cords[]],popup='<b>Path of Vehicle_1</b>',tooltip='Vehicle_1',color='blue',weight=10).add_to(m)
    # line_1=folium.vector_layers.PolyLine(coords[1],popup='<b>Path of Vehicle_1</b>',tooltip='Vehicle_1',color='blue',weight=10).add_to(m)
    for i in range (len(st.session_state.Lati)):
        folium.Marker(location=[st.session_state.Lati[i], st.session_state.Longi[i]],popup='<h3 style="color:green;">Marker2</h3>',tooltip='<strong>Click here to see Popup</strong>').add_to(m)

    for i in range(len(st.session_state.Lati)):
        line_1=folium.vector_layers.PolyLine([[st.session_state.Lati[0],st.session_state.Longi[0]],[st.session_state.Lati[i],st.session_state.Longi[i]]],popup='<b>Path of Vehicle_1</b>',tooltip='Vehicle_1',color='blue',weight=10).add_to(m)
    fig5.add_child(m)

    folium_static(m)


if selected == "Heat Map Visualization":

    st.title(f"You are visualising {selected}")

    mode=st.radio("Heat map for ",('Temperature','Humidity'))

    if mode == 'Temperature':

        m = folium.Map([st.session_state.Lati[0],st.session_state.Longi[0]],  zoom_start=15)
        newHeatList=[]
        
        for i in range(len(st.session_state.Lati)):
            newHeatList.append([st.session_state.Lati[i],st.session_state.Longi[i], st.session_state.tempAvgWT[i]])
        #for i in range(5):
        print(newHeatList)
        HeatMap(newHeatList).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        folium.LayerControl().add_to(m)
        # HeatMap([[28.645800, 77.214721, 1]]).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        # folium.LayerControl().add_to(m)
        folium_static(m)

    if mode == 'Humidity':
        m = folium.Map([st.session_state.Lati[0],st.session_state.Longi[0]],  zoom_start=15)
        newHeatList=[]
        
        for i in range(len(st.session_state.Lati)):
            newHeatList.append([st.session_state.Lati[i],st.session_state.Longi[i], st.session_state.humAvgWT[i]])
        #for i in range(5):
        print(newHeatList)
        HeatMap(newHeatList).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        folium.LayerControl().add_to(m)
        # HeatMap([[28.645800, 77.214721, 1]]).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        # folium.LayerControl().add_to(m)
        folium_static(m)



if selected == "Node Dashboard":
    if 'nodeValue' not in st.session_state:
        st.session_state['nodeValue']=1

    st.title(f"You are viewing individual {selected}")
    st.number_input(label="input node ID",min_value=1,max_value=len(st.session_state.tempAvgWT),value=st.session_state.nodeValue)
    st.markdown(f"selected node is = {st.session_state.nodeValue}")

    col1, col2,  = st.columns(2)
    with col1:
        fig = go.Figure()
        fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.temperature[st.session_state.nodeValue-1],
        title = {'text': "Temperature in Celsius"},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        fig = go.Figure()
        fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.humidity[st.session_state.nodeValue-1],
        title = {'text': "Humidity in %"},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        st.plotly_chart(fig,use_container_width=True)
    
    col3, col4,  = st.columns(2)
    
    with col3:
        fig = go.Figure()
        fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.fire[st.session_state.nodeValue-1],
        title = {'text': "Fire binary "},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        st.plotly_chart(fig,use_container_width=True)

    with col4:
        fig = go.Figure()
        fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.battery[st.session_state.nodeValue-1],
        title = {'text': "Battery in %"},
        domain = {'x': [0, 1], 'y': [0, 1]}))
        st.plotly_chart(fig,use_container_width=True)
