import paho.mqtt.client as paho
import time
import streamlit as st
import json

# Global variables
values = 0.0
act1 = "OFF"
message_received = ""

# Callback functions
def on_publish(client, userdata, result):
    st.success("El dato ha sido publicado con éxito") 
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.info(f"Mensaje recibido: {message_received}")

# MQTT Configuration
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("dodovainilla")
client1.on_message = on_message

# Streamlit UI
st.set_page_config(page_title="MQTT Control Dashboard", layout="centered")

st.title("MQTT Control Dashboard 🚀")
st.markdown("Controla el dispositivo a través de MQTT utilizando los controles a continuación.")

# Display status
status_container = st.container()
with status_container:
    st.subheader("Estado del dispositivo:")
    if act1 == "ON":
        st.success("El dispositivo está ENCENDIDO")
    else:
        st.warning("El dispositivo está APAGADO")

# Control buttons
st.divider()
st.subheader("Control del dispositivo")
col1, col2 = st.columns(2)

with col1:
    if st.button('Encender', key='on_button'):
        act1 = "ON"
        client1 = paho.Client("dodovainilla")                           
        client1.on_publish = on_publish                          
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        ret = client1.publish("datossss1", message)
        st.success("Dispositivo ENCENDIDO")

with col2:
    if st.button('Apagar', key='off_button'):
        act1 = "OFF"
        client1 = paho.Client("dodovainilla")                           
        client1.on_publish = on_publish                          
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        ret = client1.publish("datossss1", message)
        st.warning("Dispositivo APAGADO")

# Slider for analog value
st.divider()
st.subheader("Control del valor analógico")
values = st.slider('Selecciona el rango de valores', 0.0, 100.0, step=1.0)
st.write(f'Valor seleccionado: {values}')

if st.button('Enviar valor analógico', key='analog_button'):
    client1 = paho.Client("dodovainilla")                           
    client1.on_publish = on_publish                          
    client1.connect(broker, port)   
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("datossss2", message)
    st.success("Valor analógico enviado")

# Display received messages
st.divider()
st.subheader("Mensajes recibidos")
if message_received:
    st.info(message_received)
else:
    st.write("No se han recibido mensajes aún.")





