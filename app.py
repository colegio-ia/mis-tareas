import streamlit as st
import pandas as pd
from datetime import datetime
from github import Github
import json

# 1. CONFIGURACIÓN (Asegúrate de tener el GITHUB_TOKEN en los Secrets de Streamlit)
TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "colegio-ia/mis-tareas" 
FILE_PATH = "registro_tareas.json"

# Conexión con GitHub
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# Configuración de la página
st.set_page_config(page_title="Asistente de Tareas Equipo", layout="centered")

st.title("📝 Registro de tareas diarias")
# Mensaje dinámico según la hora
hora_actual = datetime.now().hour
if hora_actual >= 16: # A partir de las 4 PM
    st.warning("⚠️ ¡No olvides registrar tus tareas antes de terminar el día!")
st.write("Anotá lo que hiciste hoy para que el equipo esté al tanto.")

# 2. FUNCIONES PARA MANEJAR DATOS EN LA NUBE
def cargar_datos_desde_github():
    try:
        file_content = repo.get_contents(FILE_PATH)
        return json.loads(file_content.decoded_content.decode()), file_content.sha
    except:
        return [], None

def guardar_en_github(nueva_tarea):
    datos, sha = cargar_datos_desde_github()
    datos.append(nueva_tarea)
    contenido_final = json.dumps(datos, indent=4)
    if sha:
        repo.update_file(FILE_PATH, "Nueva tarea registrada", contenido_final, sha)
    else:
        repo.create_file(FILE_PATH, "Primer registro", contenido_final)

# 3. FORMULARIO DE ENTRADA
with st.form("form_tareas", clear_on_submit=True):
    usuario = st.selectbox("¿Quién eres?", ["CDP", "Equipo", "Otro"])
    descripcion = st.text_area("¿Qué hiciste hoy?")
    destino = st.selectbox("¿A qué equipo hay que pasarle esto?", ["Comunicación", "Administración"])
    
    submit = st.form_submit_button("Guardar Tarea")

if submit and descripcion:
    tarea = {
        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Usuario": usuario,
        "Tarea": descripcion,
        "Destino": destino
    }
    # Aquí es donde ocurre la magia: se guarda en GitHub para todos
    guardar_en_github(tarea)
    st.success("¡Tarea guardada en el servidor! Dale a 'Actualizar' para verla.")

# 4. MOSTRAR HISTORIAL COMPARTIDO
st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("📋 Tareas Registradas")
with col2:
    if st.button("🔄 Actualizar"):
        st.rerun()

# Leemos los datos directamente de GitHub para que todos vean lo mismo
tareas_totales, _ = cargar_datos_desde_github()

if tareas_totales:
    # Mostramos los datos (lo más nuevo arriba)
    df = pd.DataFrame(tareas_totales)
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
    
    # Botón para descargar y mandármelo a mí
    texto_resumen = str(tareas_totales)
    st.download_button("Descargar resumen", texto_resumen, file_name="tareas_hoy.txt")
else:
    st.info("Aún no hay tareas registradas en el servidor.")


