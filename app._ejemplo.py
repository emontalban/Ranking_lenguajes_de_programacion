# ============================================================
#  PLANTILLA DEL RETO · Mi primera app de datos con Streamlit
#  Ejecutar:  streamlit run app.py
#
#  Cómo usarla:
#   1. Edita SOLO el bloque "CONFIGURACIÓN" para conectar vuestro CSV.
#   2. Cuando funcione, resolved los TODO (están ordenados por nivel).
#   3. Ejecuta, guarda, recarga. Si algo falla, lee el mensaje de error.
# ============================================================
import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# CONFIGURACIÓN · cambiad estos valores
# ------------------------------------------------------------
TITULO = "🚲 Mi explorador de datos"
DESCRIPCION = "Cambiad esta frase: ¿qué pregunta responde vuestra app?"
FUENTE = "Datos de ejemplo (sintéticos). Indicad aquí de dónde vienen vuestros datos."

# ¿Cómo carga la app los datos? Decididlo en equipo:
#   "repo"  -> el CSV vive en la carpeta datos/ (la app arranca sola; recomendado si vais a publicarla)
#   "subir" -> la persona usuaria sube el CSV con un botón cada vez que abre la app
MODO_CARGA = "repo"
RUTA_CSV = "datos/ejemplo_movilidad.csv"

# Muchos CSV españoles usan ";" como separador y "latin-1" como codificación.
# Si veis una sola columna o caracteres raros (Ã±), cambiad estos dos valores.
SEPARADOR = ","
CODIFICACION = "utf-8"

# Nombres EXACTOS de las columnas de vuestro CSV
COLUMNA_FILTRO = "medio_transporte"   # categórica: con ella se filtra
COLUMNA_NUMERICA = "satisfaccion"     # numérica: con ella se calculan medias
COLUMNA_GRUPO = "distrito"            # categórica: con ella se agrupa el gráfico

# ------------------------------------------------------------
# A partir de aquí, el motor de la app
# ------------------------------------------------------------
st.set_page_config(page_title="Mi app de datos", page_icon="📊", layout="wide")

st.title(TITULO)
st.write(DESCRIPCION)
st.caption(FUENTE)


@st.cache_data
def leer_csv(origen):
    return pd.read_csv(origen, sep=SEPARADOR, encoding=CODIFICACION)


# 1. Cargar los datos
if MODO_CARGA == "subir":
    archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])
    if archivo is None:
        st.info("Sube un CSV para empezar.")
        st.stop()
    df = leer_csv(archivo)
else:
    df = leer_csv(RUTA_CSV)

# 2. Comprobar que las columnas de la configuración existen
faltan = [c for c in (COLUMNA_FILTRO, COLUMNA_NUMERICA, COLUMNA_GRUPO) if c not in df.columns]
if faltan:
    st.error(f"Estas columnas no están en el CSV: {faltan}")
    st.write("Las columnas disponibles son:", list(df.columns))
    st.dataframe(df.head())
    st.stop()

if not pd.api.types.is_numeric_dtype(df[COLUMNA_NUMERICA]):
    st.error(f"La columna '{COLUMNA_NUMERICA}' no es numérica. Elegid otra en la CONFIGURACIÓN.")
    st.stop()

# 3. Conocer los datos
with st.expander("👀 Conoce tus datos", expanded=False):
    st.write(f"Filas: {len(df)} · Columnas: {len(df.columns)}")
    st.dataframe(df.head(10))

# 4. Filtro en la barra lateral
st.sidebar.header("Filtros")
opciones = sorted(df[COLUMNA_FILTRO].dropna().unique())
seleccion = st.sidebar.multiselect(COLUMNA_FILTRO, options=opciones, default=opciones)

# TODO (nivel 2): añadid un segundo filtro con otra columna categórica
#   y combinadlo con el primero usando &  (mirad app.py de la demo Pulso Digital).

filtrado = df[df[COLUMNA_FILTRO].isin(seleccion)]

if filtrado.empty:
    st.warning("No hay datos con esta selección. Marcad alguna opción más.")
    st.stop()

# 5. Indicadores
st.subheader("Resumen")
col1, col2 = st.columns(2)
col1.metric("Registros", len(filtrado))
col2.metric(f"Media de {COLUMNA_NUMERICA}", f"{filtrado[COLUMNA_NUMERICA].mean():,.1f}")

# TODO (nivel 1): cambiad las etiquetas de los indicadores por textos que entienda cualquiera
# TODO (nivel 2): añadid un tercer indicador (máximo, mínimo, suma, % de algo...)

# 6. Gráfico
st.subheader(f"{COLUMNA_NUMERICA} medio por {COLUMNA_GRUPO}")
resumen = (
    filtrado.groupby(COLUMNA_GRUPO)[COLUMNA_NUMERICA]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(resumen, sort=False)  # sort=False respeta nuestro orden (de mayor a menor)

# TODO (nivel 2): añadid un segundo gráfico (st.line_chart si tenéis fechas,
#   st.scatter_chart para relacionar dos columnas numéricas...)
# TODO (nivel 3): escribid con st.write una frase que explique qué se ve en el gráfico
#   y que cambie con los filtros (por ejemplo, qué grupo tiene la media más alta).

# 7. Tabla con los datos filtrados
with st.expander("Ver los datos filtrados"):
    st.dataframe(filtrado, hide_index=True)
