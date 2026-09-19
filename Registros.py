import streamlit as st
import pyodbc
from datetime import date, datetime

# -----------------------------------------------------------------
# CONEXIÓN A SQL SERVER
# -----------------------------------------------------------------
# Recomendado: guarda estos datos en .streamlit/secrets.toml (ver
# ejemplo más abajo) en lugar de escribirlos aquí directamente.
def get_connection():
    conn_str = (
        f"DRIVER={{{st.secrets['sql']['driver']}}};"
        f"SERVER={st.secrets['sql']['server']};"
        f"DATABASE={st.secrets['sql']['database']};"
        f"UID={st.secrets['sql']['user']};"
        f"PWD={st.secrets['sql']['password']};"
    )
    return pyodbc.connect(conn_str)


def guardar_registro(nombre: str, fecha: date, hora: str):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO registros (nombre, fecha, hora)
            VALUES (?, ?, ?)
            """,
            nombre, fecha, hora
        )
        conn.commit()
    finally:
        conn.close()


# -----------------------------------------------------------------
# INTERFAZ
# -----------------------------------------------------------------
st.set_page_config(page_title="Registro de datos", page_icon="📝")
st.title("📝 Registro de datos")

with st.form("form_registro", clear_on_submit=True):
    nombre = st.text_input("Nombre")
    fecha = st.date_input("Fecha", value=date.today())
    hora = st.time_input("Hora", value=datetime.now().time())

    enviado = st.form_submit_button("Guardar")

    if enviado:
        if not nombre.strip():
            st.error("El nombre no puede estar vacío.")
        else:
            try:
                guardar_registro(nombre.strip(), fecha, hora.strftime("%H:%M:%S"))
                st.success(f"Registro guardado: {nombre} — {fecha} — {hora}")
            except Exception as e:
                st.error(f"Error al guardar en la base de datos: {e}")