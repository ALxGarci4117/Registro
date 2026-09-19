import streamlit as st
import pymssql
from datetime import date, datetime

# -----------------------------------------------------------------
# CONEXIÓN A SQL SERVER
# -----------------------------------------------------------------
def get_connection():
    return pymssql.connect(
        server=st.secrets["sql"]["server"],
        port=str(st.secrets["sql"].get("port", 1433)),
        user=st.secrets["sql"]["user"],
        password=st.secrets["sql"]["password"],
        database=st.secrets["sql"]["database"],
        timeout=10,
        login_timeout=10,
    )


def guardar_registro(nombre, fecha, hora):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO super_alejandro (nombre, fecha, hora) VALUES (%s, %s, %s)",
            (nombre, fecha.strftime("%Y-%m-%d"), hora),
        )
        conn.commit()
    finally:
        conn.close()


def obtener_ultimos(n=10):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT TOP {int(n)} nombre, fecha, hora FROM super_alejandro ORDER BY id DESC"
        )
        return cursor.fetchall()
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
            st.success(f"Guardado: {nombre} — {fecha} — {hora.strftime('%H:%M:%S')}")
        except Exception as e:
            st.error("No se pudo guardar el registro.")
            st.exception(e)

st.divider()

# ---- Verificación: ver lo que ya está en la tabla ----
if st.button("Ver últimos 10 registros"):
    try:
        filas = obtener_ultimos(10)
        if filas:
            st.table(
                [{"Nombre": f[0], "Fecha": str(f[1]), "Hora": str(f[2])} for f in filas]
            )
        else:
            st.info("La tabla está vacía todavía.")
    except Exception as e:
        st.error("No se pudo leer la tabla.")
        st.exception(e)

# ---- Diagnóstico de conexión ----
with st.expander("🔧 Probar conexión"):
    if st.button("Probar ahora"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            conn.close()
            st.success("Conexión exitosa.")
            st.code(version)
        except Exception as e:
            st.error("Falló la conexión.")
            st.exception(e)
