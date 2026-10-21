# ============================================================
# APP DEL RETO · Adaptada siguiendo los pasos de app_ejemplo.py
# Ejecutar: .\venv\Scripts\python.exe -m streamlit run app.py
# 1. Configurar el CSV. 2. Comprobar los datos. 3. Usar los filtros.
# ============================================================
from pathlib import Path

import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# CONFIGURACIÓN · como en app_ejemplo.py
# ------------------------------------------------------------
TITULO = "💻 Explorador de lenguajes de programación"

DESCRIPCION = (
    "¿Cómo ha evolucionado el uso de los lenguajes de programación "
    "a lo largo de los años disponibles, según las encuestas de Stack Overflow?"
)
FUENTE = (
    "Fuente: encuestas anuales de Stack Overflow. "
    "Los resultados representan a las personas encuestadas."
)

MODO_CARGA = "repo"  # "repo": CSV del proyecto; "subir": elegir un CSV
CARPETA = Path(__file__).resolve().parent
RUTA_CSV = CARPETA / "datos" / "lenguajes_por_año_pais_perfil.csv"
SEPARADOR = ","
CODIFICACION = "utf-8-sig"
COLUMNA_FILTRO = "pais"
COLUMNA_NUMERICA = "porcentaje"
COLUMNA_GRUPO = "lenguaje"
ANIO_INICIAL = 2017

COLUMNAS = [
    "año",
    COLUMNA_FILTRO,
    "perfil",
    COLUMNA_GRUPO,
    "personas",
    "respuestas_grupo",
    COLUMNA_NUMERICA
]


# ------------------------------------------------------------
# PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Lenguajes de programación",
    page_icon="💻",
    layout="wide"
)

st.title(TITULO)
st.write(DESCRIPCION)

st.caption(FUENTE)


# ------------------------------------------------------------
# 1. CARGAR LOS DATOS
# ------------------------------------------------------------
# La fecha de modificación permite actualizar la caché
# cuando sustituimos el CSV.
@st.cache_data
def leer_csv(origen, modificacion=None):
    return pd.read_csv(origen, sep=SEPARADOR, encoding=CODIFICACION)


try:
    if MODO_CARGA == "subir":
        archivo = st.file_uploader("Sube el CSV de lenguajes resumido", type=["csv"])
        if archivo is None:
            st.info("Sube un CSV para empezar.")
            st.stop()
        df = leer_csv(archivo)
    elif MODO_CARGA == "repo":
        if not RUTA_CSV.exists():
            st.error(f"No encuentro el CSV: {RUTA_CSV.name}. Guárdalo en datos/.")
            st.stop()
        df = leer_csv(str(RUTA_CSV), RUTA_CSV.stat().st_mtime)
    else:
        st.error('MODO_CARGA debe ser "repo" o "subir" en CONFIGURACIÓN.')
        st.stop()
except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
    st.error(f"No se ha podido leer el CSV. Revisa el separador y la codificación: {error}")
    st.stop()


# ------------------------------------------------------------
# 2. COMPROBAR LAS COLUMNAS Y LOS DATOS
# ------------------------------------------------------------
faltan = [columna for columna in COLUMNAS if columna not in df.columns]

if faltan:
    st.error(f"Faltan estas columnas: {faltan}")
    st.write("Columnas disponibles:", list(df.columns))
    st.stop()

# Usamos los nombres internos del resumen en el resto del motor.
df = df.rename(columns={
    COLUMNA_FILTRO: "pais",
    COLUMNA_NUMERICA: "porcentaje",
    COLUMNA_GRUPO: "lenguaje"
})

if df.empty:
    st.warning("El archivo no contiene datos.")
    st.stop()

# Comprobamos las columnas numéricas.
for columna in ["año", "personas", "respuestas_grupo", "porcentaje"]:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

if df[["año", "pais", "perfil", "lenguaje", "personas", "respuestas_grupo", "porcentaje"]].isna().any().any():
    st.error("Hay valores vacíos o números incorrectos. Revisa el CSV.")
    st.stop()

df["año"] = df["año"].astype(int)
# Excluimos las ediciones antiguas aunque se vuelva a cargar el CSV original.
df = df[df["año"] >= ANIO_INICIAL].copy()
if df.empty:
    st.warning(f"No hay datos desde {ANIO_INICIAL} en el archivo.")
    st.stop()

st.caption(f"Periodo disponible: {df['año'].min()}–{df['año'].max()}.")

if df.duplicated(["año", "pais", "perfil", "lenguaje"]).any():
    st.error("Hay filas repetidas para el mismo año, país, perfil y lenguaje.")
    st.stop()


# ------------------------------------------------------------
# 3. CONOCER LOS DATOS
# ------------------------------------------------------------
with st.expander("👀 Conoce tus datos"):
    st.write(
        "Los datos originales se agrupan por año, país y perfil. "
        "Los filtros permiten elegir qué países y perfiles reúne el ranking."
    )
    st.write(
        f"Filas: {len(df):,} · "
        f"Años disponibles: {df['año'].nunique()}"
    )
    st.dataframe(df.head(10), hide_index=True)


# ------------------------------------------------------------
# 4. FILTROS EN LA BARRA LATERAL
# ------------------------------------------------------------
st.sidebar.header("🔎 Filtros")

# Mostramos primero el año más reciente.
años = sorted(df["año"].unique().tolist(), reverse=True)
año = st.sidebar.selectbox("Año del ranking", años)

paises = st.sidebar.multiselect(
    "Países", options=sorted(df["pais"].unique().tolist()),
    help="Deja la selección vacía para incluir todos los países."
)
perfiles = st.sidebar.multiselect(
    "Perfiles", options=sorted(df["perfil"].unique().tolist()),
    help="Deja la selección vacía para incluir todos los perfiles."
)
st.sidebar.caption("Sin selección en un filtro se incluyen todas sus opciones.")

# Aplicamos ambos filtros antes de sumar personas y respuestas.
datos_grupo = df.copy()
if paises:
    datos_grupo = datos_grupo[datos_grupo["pais"].isin(paises)]
if perfiles:
    datos_grupo = datos_grupo[datos_grupo["perfil"].isin(perfiles)]

if datos_grupo.empty:
    st.warning("No hay datos para estos países y perfiles. Cambia los filtros.")
    st.stop()

contexto = (
    (", ".join(paises) if paises else "Todos los países")
    + " · "
    + (", ".join(perfiles) if perfiles else "Todos los perfiles")
)
# Cada grupo repite su denominador en todos sus lenguajes.
# Sumamos una sola vez cada grupo y recalculamos el porcentaje anual.
totales = (
    datos_grupo.drop_duplicates(["año", "pais", "perfil"])
    .groupby("año")["respuestas_grupo"].sum()
)
historico = datos_grupo.groupby(["año", "lenguaje"], as_index=False)["personas"].sum()
historico["respuestas_grupo"] = historico["año"].map(totales)
historico["porcentaje"] = (
    100 * historico["personas"] / historico["respuestas_grupo"]
).round(2)
filtrado = historico[historico["año"] == año].copy()

if filtrado.empty:
    st.warning("No hay datos para esta selección.")
    st.stop()

# ------------------------------------------------------------
# 5. INDICADORES · mejoras de nivel 1 y 2
# ------------------------------------------------------------
ranking = filtrado.sort_values(
    ["porcentaje", "lenguaje"],
    ascending=[False, True]
)

lider = ranking.iloc[0]

# Este total se repite en cada lenguaje del mismo grupo.
# Lo tomamos una sola vez: NO sumamos todas las filas.
total_personas = int(ranking["respuestas_grupo"].iloc[0])

st.subheader(f"Resumen de {año}")
st.caption(contexto)

col1, col2, col3 = st.columns(3)

col1.metric("Personas que respondieron", f"{total_personas:,}")
col2.metric("Lenguaje líder del grupo", lider["lenguaje"])
col3.metric("Uso del lenguaje líder", f"{lider['porcentaje']:.2f} %")

st.write(
    f"En este grupo, **{lider['lenguaje']}** encabeza el ranking "
    f"con un **{lider['porcentaje']:.2f} %** de uso."
)

if total_personas < 30:
    st.caption(
        "El grupo tiene menos de 30 respuestas: "
        "los resultados pueden variar mucho con pocas personas."
    )


# ------------------------------------------------------------
# 6. GRÁFICOS · ranking y evolución (mejora de nivel 2)
# ------------------------------------------------------------
st.subheader("📊 Los 10 lenguajes con mayor porcentaje de uso")

top_10 = ranking.head(10).set_index("lenguaje")[["porcentaje"]]
top_10 = top_10.rename(columns={"porcentaje": "Uso (%)"})

st.bar_chart(top_10, sort=False)

st.caption(
    "Cada barra muestra el porcentaje de personas del grupo "
    "que seleccionó ese lenguaje. Una persona puede seleccionar varios, "
    "por lo que los porcentajes no tienen que sumar 100 %."
)


# ------------------------------------------------------------
# Segundo gráfico: evolución durante los años disponibles
# ------------------------------------------------------------
st.subheader("📈 Evolución del uso")

st.write(
    "Este gráfico utiliza los países y perfiles seleccionados "
    "durante todos los años disponibles."
)

opciones = sorted(historico["lenguaje"].unique().tolist())

# Seleccionamos inicialmente los tres primeros del ranking actual.
seleccion = st.multiselect(
    "Lenguajes que quieres comparar",
    options=opciones,
    default=ranking["lenguaje"].head(3).tolist()
)

if not seleccion:
    st.info("Selecciona al menos un lenguaje para ver su evolución.")
else:
    datos_evolucion = historico[
        historico["lenguaje"].isin(seleccion)
    ]

    # Una columna por lenguaje y una fila por año.
    evolucion = datos_evolucion.pivot(
        index="año",
        columns="lenguaje",
        values="porcentaje"
    )

    # Conservamos los años sin datos como valores ausentes.
    # No los sustituimos por cero.
    evolucion = evolucion.reindex(sorted(df["año"].unique()))

    # Convertimos los años en etiquetas para mostrarlos sin decimales.
    evolucion.index = evolucion.index.astype(str)
    evolucion.index.name = "Año"

    st.line_chart(evolucion)

    with st.expander("Ver los porcentajes de la evolución"):
        st.dataframe(evolucion)

st.caption(
    "Los valores del gráfico están expresados en porcentaje. "
    "Un dato ausente no significa un uso del 0 %."
)


# ------------------------------------------------------------
# 7. TABLA FILTRADA
# ------------------------------------------------------------
with st.expander("📋 Ver los datos del ranking"):
    st.dataframe(
        ranking[
            ["año", "lenguaje", "personas", "porcentaje"]
        ],
        hide_index=True
    )


# ------------------------------------------------------------
# 8. FUENTE Y CONTEXTO
# ------------------------------------------------------------
st.markdown(
    "**Fuente:** [Stack Overflow Developer Survey]"
    "(https://survey.stackoverflow.co/)"
)

st.caption(
    "La encuesta incluye lenguajes de programación, scripting y marcado. "
    "Las opciones y las personas participantes pueden cambiar entre años; "
    "la comparación es descriptiva."
)
