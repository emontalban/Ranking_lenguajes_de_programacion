# 🚀 Reto por equipos: de un dataset a vuestra propia app

**Equipos de 4-5 personas · Streamlit + Python**

Sois un equipo de producto de datos. Vuestra misión: elegir un dataset, formular **una pregunta clara** y construir una app interactiva con Streamlit que ayude a otras personas a responderla.

No buscamos la app más compleja. Buscamos una app que **funcione**, **responda a una pregunta** y que **cualquiera pueda usar** sin que se la expliquéis.

---



## 0. Antes de empezar (5 min, dentro de la fase 1)

cd app-equipo-<nombre>
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1   ·   macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

✅ **Primer hito:** la plantilla arranca con los datos de ejemplo (movilidad ficticia).

---

## 1. Roles

| Rol | Qué hace |
| --- | --- |
| 💻 Programa | Escribe el código y ejecuta la app. **Es la única que hace `git push` en ese turno.** |
| 🔎 Explora | Conoce las columnas, propone preguntas, comprueba que los números tienen sentido. |
| 🎨 Diseña | Títulos, etiquetas, orden de los elementos, que se entienda a la primera. |
| 🧪 Prueba | Usa la app como una usuaria más: cambia filtros, busca errores, deja todo vacío. |
| 📣 Comunica | Anota decisiones y errores, y prepara la mini demo final. |

---

## 2. Las fases

| Tiempo | Fase | Entregable |
| --- | --- | --- |
| 0–10 | **Elegir tema, dataset y pregunta** | Dataset descargado + una pregunta escrita |
| 10–20 | **Entender los datos** | Respuestas a las 5 preguntas de abajo |
| 20–45 | **Construir la app mínima** | La app funciona con **vuestro** CSV |
| 45–65 | **Mejorar** (y, si vais rápido, **publicar en Railway**) | Al menos dos mejoras |
| 65–75 | **Prueba cruzada**: otro equipo usa vuestra app | Una mejora a partir de su feedback |
| 75–90 | **Mini demos** (2 min por equipo) | Presentación |

### Fase 1 · Elegid tema, dataset y pregunta (10 min)

Elegid un tema que os motive: cultura, movilidad, medioambiente, consumo, empleo, salud pública, deporte, turismo… El dataset lo decidís vosotras. Algunas fuentes fiables:

- [datos.gob.es](https://datos.gob.es) · catálogo de datos abiertos de España
- [Portal de datos abiertos del Ayuntamiento de Madrid](https://datos.madrid.es)
- [INE](https://www.ine.es) · estadísticas oficiales (botón de descarga en CSV)
- [Kaggle Datasets](https://www.kaggle.com/datasets) · requiere cuenta
- [Our World in Data](https://ourworldindata.org) · datos internacionales, descarga CSV en cada gráfico

**Requisitos del dataset**

- En formato **CSV** (o fácil de convertir a CSV).
- Con al menos **una columna de categorías** (para filtrar) y **una columna numérica** (para calcular).
- Manejable: entre 50 y 100.000 filas, y menos de 25 MB (GitHub rechaza archivos de más de 100 MB).
- **Sin datos personales** de personas identificables.
- Con **fuente** conocida: la tendréis que citar en la app.

> ⏱️ No busquéis el dataset perfecto. Como máximo para este paso se estiman unos 15 mins.

### Fase 2 · Entended los datos (10 min)

Antes de programar, responded en equipo:

1. ¿Qué representa **una fila**?
2. ¿Qué significan las columnas que vais a usar?
3. ¿Cuáles son **numéricas** y cuáles **categóricas**?
4. ¿Hay valores vacíos o raros?
5. ¿Qué **gráfico** ayudaría a responder vuestra pregunta?

Truco: con `MODO_CARGA = "repo"`, la sección **«Conoce tus datos»** de la app ya os enseña las primeras filas.

### Fase 3 · Construid la app mínima (25 min)

**¿Cómo carga la app los datos? Lo decidís vosotras** (en `app.py`, variable `MODO_CARGA`):

| Opción | Cómo | Ventaja | Inconveniente |
| --- | --- | --- | --- |
| `"repo"` | Copiáis el CSV en la carpeta `datos/` y ponéis su nombre en `RUTA_CSV` | La app arranca sola, también publicada en internet | El CSV queda en el repo (solo datos públicos) |
| `"subir"` | La persona usuaria sube el CSV con un botón | Sirve para cualquier CSV con esas columnas | Hay que subir el archivo cada vez que se abre la app |

Pasos:

1. Copiad vuestro CSV en `datos/` (si elegís `"repo"`).
2. En el bloque **CONFIGURACIÓN** de `app.py`, cambiad `TITULO`, `DESCRIPCION`, `FUENTE` y los nombres de las tres columnas.
3. Si veis una sola columna enorme o letras raras (`Ã±`), cambiad `SEPARADOR = ";"` y/o `CODIFICACION = "latin-1"`.
4. Guardad y recargad la app en el navegador.

**La app mínima tiene:** título y descripción propios · vuestro dataset · una métrica útil · un gráfico relacionado con la pregunta · un filtro · la tabla de datos filtrados · la fuente citada.

### Fase 4 · Mejorad (20 min) — elegid **al menos dos**

**Nivel 1 · Que se entienda**
- Etiquetas de los indicadores en lenguaje claro (no nombres de columnas).
- Un texto corto que explique cómo leer el gráfico.

**Nivel 2 · Que haga más cosas**
- Un segundo filtro combinado con el primero (`&`).
- Un tercer indicador (máximo, mínimo, suma, porcentaje…).
- Un segundo gráfico: `st.line_chart` si hay fechas, `st.scatter_chart` para relacionar dos números.

**Nivel 3 · Que vaya más lejos**
- Una frase automática que cambie con los filtros («La media más alta es la de *X* con *Y*»).
- Organizar la app en pestañas con `st.tabs`.
- Describir vuestra app a [Lovable](https://lovable.dev) y comparar lo que genera con lo que habéis hecho.

**⭐ Nivel avanzado · Publicadla en internet con Railway**
Solo si la app mínima ya funciona. Seguid **[DESPLIEGUE_RAILWAY.md](DESPLIEGUE_RAILWAY.md)**: una cuenta por equipo, unos 15 minutos. Al final tendréis un enlace `https://….up.railway.app` para enseñarlo en la mini demo.

### Fase 5 · Prueba cruzada (10 min)

Intercambiad el ordenador (o el enlace de Railway) con otro equipo. Sin explicarles nada, observad:

- ¿Entienden qué muestra la app?
- ¿Los filtros funcionan? ¿Los números cambian cuando deben?
- ¿Qué pasa si quitan todas las opciones del filtro?
- ¿Pueden responder vuestra pregunta usando la app?

Haced **al menos una mejora** a partir de lo que observéis.

### Fase 6 · Mini demo (2 min por equipo)

1. **La pregunta:** ¿qué queríais averiguar?
2. **Los datos:** ¿qué dataset y de dónde viene?
3. **La app en vivo:** un filtro, una métrica y un gráfico.
4. **El hallazgo:** ¿qué habéis descubierto?
5. **Lo siguiente:** ¿qué haríais con 30 minutos más?

---

## 3. ¿Está listo? (rúbrica)

| Criterio | Puntos |
| --- | --- |
| La app se ejecuta y carga vuestro dataset | 2 |
| Tiene una métrica relevante y un gráfico | 2 |
| Tiene un filtro que funciona (y no se rompe si se vacía) | 2 |
| Responde a una pregunta clara y cita la fuente | 2 |
| Todo el equipo sabe explicar qué hace y qué mejoraría | 2 |
| **Total** | **10** |
| ⭐ Bonus: la app está publicada en Railway y funciona desde el móvil | +1 |

---

## 4. Si os bloqueáis

Antes de llamar a la formadora, el equipo responde: **¿qué intentábamos hacer?, ¿qué esperábamos que pasara?, ¿qué dice el error y en qué línea?**

| Mensaje | Causa probable | Solución |
| --- | --- | --- |
| `streamlit: command not found` | El entorno virtual no está activado | Activadlo y repetid `pip install -r requirements.txt` |
| `FileNotFoundError` | La ruta del CSV no coincide | Revisad `RUTA_CSV` y que el archivo esté en `datos/` |
| «Estas columnas no están en el CSV» | Nombre de columna mal escrito | Copiad el nombre exacto de la lista que muestra la app |
| Todo sale en una sola columna | El CSV usa `;` | `SEPARADOR = ";"` |
| Letras raras (`Ã±`, `Ã³`) | Codificación distinta | `CODIFICACION = "latin-1"` |
| «La columna no es numérica» | Números con coma decimal (`3,5`) | Añadid `decimal=","` en `pd.read_csv` o elegid otra columna |
| `IndentationError` | Espacios mal alineados | Revisad la línea indicada: 4 espacios por nivel |

**Chuleta**

```python
# Segundo filtro combinado
otra = st.sidebar.multiselect("Distrito", options=sorted(df["distrito"].unique()), default=sorted(df["distrito"].unique()))
filtrado = df[df[COLUMNA_FILTRO].isin(seleccion) & df["distrito"].isin(otra)]

# Indicador nuevo
st.metric("Máximo", filtrado[COLUMNA_NUMERICA].max())

# Contar registros por categoría
st.bar_chart(filtrado[COLUMNA_GRUPO].value_counts())

# Línea temporal (si tenéis una columna de fecha)
df["fecha"] = pd.to_datetime(df["fecha"])
st.line_chart(filtrado.groupby("fecha")[COLUMNA_NUMERICA].mean())
```

Documentación: [docs.streamlit.io](https://docs.streamlit.io) · Código de referencia: `app.py` de la demo **Pulso Digital**.

---

> **Recordad:** no hace falta saberlo todo de Python. Lo importante es terminar con una app que hayáis construido, entendido y probado en equipo.
