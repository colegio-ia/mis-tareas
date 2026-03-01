import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Asistente de Tareas Equipo", layout="centered")

st.title("📝 Registro de Tareas Diarias")
st.write("Registrá lo que hiciste hoy para que el equipo esté al tanto.")

# Base de datos simulada (En una app real usaríamos una base de datos externa, 
# pero para empezar, Streamlit mantiene los datos en la sesión)
if 'tareas' not in st.session_state:
    st.session_state.tareas = []

# Formulario de entrada
with st.form("form_tareas", clear_on_submit=True):
    usuario = st.selectbox("¿Quién eres?", ["Lorena", "Carlos", "Otro"])
    descripcion = st.text_area("¿Qué hiciste hoy?")
    destino = st.selectbox("¿A qué equipo hay que pasarle esto?", ["Comunicación", "Administración"])
    
    submit = st.form_submit_button("Guardar Tarea")

if submit and descripcion:
    nueva_tarea = {
        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Usuario": usuario,
        "Tarea": descripcion,
        "Destino": destino
    }
    st.session_state.tareas.insert(0, nueva_tarea)
    st.success("¡Tarea guardada con éxito!")

# Mostrar historial
st.divider()
st.subheader("📋 Tareas del Día")
if st.session_state.tareas:
    df = pd.DataFrame(st.session_state.tareas)
    st.table(df)
else:
    st.info("Aún no hay tareas registradas hoy.")

# Botón para copiar todo (Para pasármelo a mí)
if st.session_state.tareas:
    texto_resumen = str(st.session_state.tareas)
    st.download_button("Descargar resumen para la IA", texto_resumen, file_name="tareas_hoy.txt")


