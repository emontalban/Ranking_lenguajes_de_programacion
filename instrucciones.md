# Instrucciones del explorador de lenguajes de programación

## 1. Qué hace la aplicación

`app.py` muestra el uso de lenguajes de programación según los datos resumidos de las encuestas de Stack Overflow. Permite elegir un año, varios países y varios perfiles de personas encuestadas. Con esa selección calcula indicadores, un ranking y una gráfica de evolución.



### Si ya existe el entorno `venv`

Instala las dependencias y ejecuta la aplicación:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

### Si instalas el proyecto desde cero

Necesitas Python instalado. El archivo `.python-version` del proyecto indica Python 3.12. Comprueba que está disponible:

```powershell
py -3.12 --version
```

Crea un entorno virtual para mantener las dependencias del proyecto separadas:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

`requirements.txt` solicita `streamlit>=1.50,<2` y `pandas>=2.2`. Streamlit construye la interfaz web; pandas lee y transforma las tablas.

No hace falta activar el entorno: los comandos usan directamente su intérprete. Mantén PowerShell abierto mientras utilizas la app. Abre la dirección que muestre Streamlit, normalmente `http://localhost:8501`. Para detenerla, pulsa `Ctrl+C` en esa terminal.

Para ejecutar la plantilla de movilidad en lugar de la app principal:

```powershell
.\venv\Scripts\python.exe -m streamlit run app_ejemplo.py
```

## 3. Archivos principales

| Archivo | Contenido |
| --- | --- |
| `app.py` | Aplicación de lenguajes con filtros y gráficos. |
| `app_ejemplo.py` | Plantilla didáctica con datos de movilidad y tareas TODO. |
| `datos/lenguajes_por_año_pais_perfil.csv` | Datos resumidos que utiliza la app principal. |
| `datos/ejemplo_movilidad.csv` | Datos de la plantilla. |
| `requirements.txt` | Dependencias que instala pip. |
| `.python-version` | Versión de Python indicada para el proyecto. |
| `railway.json` | Comando de arranque para Railway. |

## 4. Cómo utilizar los filtros

1. Elige el **año del ranking** en la barra lateral. Por defecto aparece el más reciente.
2. Selecciona uno o varios **países**. Si no seleccionas ninguno, se incluyen todos.
3. Selecciona uno o varios **perfiles**. Si no seleccionas ninguno, se incluyen todos.
4. Consulta los indicadores y las barras del año elegido.
5. En **Lenguajes que quieres comparar**, selecciona las líneas del gráfico de evolución. Inicialmente se proponen los tres primeros del ranking.
6. Abre las secciones desplegables para consultar las tablas.

Los países y perfiles afectan al ranking, los indicadores, la evolución y la tabla final. El año elegido afecta al ranking y sus indicadores; la evolución conserva todos los años disponibles. El selector de lenguajes afecta únicamente a la evolución. Si lo dejas vacío, aparece un mensaje para elegir algún lenguaje.

La sección «Conoce tus datos» muestra una vista previa del conjunto validado, antes de aplicar los filtros de la barra lateral.

## 5. Explicación de `app.py`, función y bloque por bloque

El archivo define una sola función propia: `leer_csv()`. El resto del código se ejecuta de arriba abajo y utiliza funciones de Streamlit y métodos de pandas. A continuación se explica siguiendo el mismo orden del archivo.

### 5.1. Importaciones

```python
from pathlib import Path
import pandas as pd
import streamlit as st
```

- `Path` permite construir y comprobar rutas de archivos.
- `pd` es el nombre abreviado de pandas. Un `DataFrame` es una tabla con filas y columnas.
- `st` es el nombre abreviado de Streamlit, que muestra textos, controles, tablas y gráficos.

### 5.2. Configuración

| Variable | Para qué sirve |
| --- | --- |
| `TITULO`, `DESCRIPCION`, `FUENTE` | Textos de presentación. |
| `MODO_CARGA` | `"repo"` lee el archivo del proyecto; `"subir"` permite cargarlo desde la web. |
| `CARPETA` | Carpeta donde está guardado `app.py`. |
| `RUTA_CSV` | Ruta del archivo de lenguajes. |
| `SEPARADOR` | Carácter que separa los campos del CSV: una coma. |
| `CODIFICACION` | Codificación de lectura: `utf-8-sig`, que admite la marca BOM de UTF-8. |
| `COLUMNA_FILTRO` | Nombre de la columna de país en el CSV. |
| `COLUMNA_NUMERICA` | Nombre de la columna de porcentaje. |
| `COLUMNA_GRUPO` | Nombre de la columna de lenguaje. |
| `ANIO_INICIAL` | Primer año admitido: 2017. |
| `COLUMNAS` | Lista de columnas obligatorias. |

`Path(__file__).resolve().parent` obtiene la carpeta del script como ruta absoluta. El operador `/` une esa carpeta con `datos` y con el nombre del CSV.

El archivo debe contener estas columnas, salvo los tres nombres que se pueden adaptar mediante la configuración:

| Columna | Significado |
| --- | --- |
| `año` | Edición de la encuesta. |
| `pais` | País de las personas encuestadas. |
| `perfil` | Categoría de perfil de las personas encuestadas. |
| `lenguaje` | Lenguaje seleccionado. |
| `personas` | Personas de ese año, país y perfil que seleccionaron ese lenguaje. |
| `respuestas_grupo` | Total de respuestas del grupo formado por año, país y perfil. Se repite en sus filas de lenguajes. |
| `porcentaje` | Porcentaje de uso recogido en el resumen. La app lo vuelve a calcular al agregar grupos. |

### 5.3. Presentación de la página

- `st.set_page_config()` establece el título de la pestaña, el icono y el diseño ancho con `layout="wide"`.
- `st.title()` muestra el título principal.
- `st.write()` muestra la pregunta que responde la aplicación.
- `st.caption()` muestra textos secundarios, como la fuente y el periodo disponible.

### 5.4. Función `leer_csv(origen, modificacion=None)`

```python
@st.cache_data
def leer_csv(origen, modificacion=None):
    return pd.read_csv(origen, sep=SEPARADOR, encoding=CODIFICACION)
```

**Qué recibe:** `origen`, que puede ser una ruta o un archivo subido, y `modificacion`, un argumento opcional con la fecha de modificación del archivo local.

**Qué hace:** `pd.read_csv()` lee el CSV utilizando el separador y la codificación configurados.

**Qué devuelve:** un `DataFrame` con los datos.

El decorador `@st.cache_data` guarda el resultado para reutilizarlo en las siguientes ejecuciones con los mismos argumentos. `modificacion` no se usa dentro de la función: sirve para que cambie la clave de caché cuando cambia la fecha de modificación del archivo local.

### 5.5. Carga de datos y control de errores

En modo `"subir"`, `st.file_uploader()` muestra un control para elegir un CSV. Mientras no haya archivo, `st.info()` muestra un aviso y `st.stop()` detiene esa ejecución.

En modo `"repo"`, `RUTA_CSV.exists()` comprueba que existe el archivo. `RUTA_CSV.stat().st_mtime` obtiene su fecha de modificación y la pasa a `leer_csv()` junto a la ruta.

Si el modo no es válido, se muestra un error. El bloque `try/except` también captura errores de acceso, codificación, formato de CSV y archivos sin contenido legible. `st.error()` presenta el mensaje y `st.stop()` evita continuar con datos que no se han podido cargar.

### 5.6. Comprobación de columnas y datos

La lista `faltan` compara las columnas obligatorias con `df.columns`. Si falta alguna, la app muestra cuáles faltan, cuáles existen y detiene la ejecución.

Después realiza estas operaciones:

| Operación | Qué hace en este código |
| --- | --- |
| `df.rename(columns=...)` | Normaliza los nombres configurables a `pais`, `porcentaje` y `lenguaje`. |
| `df.empty` | Comprueba si la tabla no tiene datos. |
| `pd.to_numeric(..., errors="coerce")` | Convierte año, personas, respuestas y porcentaje a números. Los valores no convertibles pasan a ausentes. |
| `isna().any().any()` | Detecta si hay al menos un valor ausente en las columnas obligatorias. |
| `astype(int)` | Convierte el año a entero. |
| `df[df["año"] >= ANIO_INICIAL]` | Conserva únicamente los años desde 2017. |
| `copy()` | Crea una copia de la tabla seleccionada. |
| `min()` y `max()` | Obtienen los extremos del periodo disponible. |
| `duplicated([...]).any()` | Detecta filas repetidas para la misma combinación de año, país, perfil y lenguaje. |

Estas comprobaciones no constituyen una validación completa del CSV: el código no comprueba, por ejemplo, que todos los denominadores sean positivos o que sean iguales dentro de cada grupo. El archivo resumido debe respetar esas condiciones para que los cálculos tengan sentido.

### 5.7. Conocer los datos

`st.expander()` crea una sección que se puede abrir y cerrar. Dentro:

- `len(df)` cuenta las filas.
- `df["año"].nunique()` cuenta los años diferentes.
- `df.head(10)` selecciona las primeras diez filas.
- `st.dataframe(..., hide_index=True)` muestra la tabla sin el índice de pandas.

### 5.8. Filtros de año, países y perfiles

`st.sidebar.header()` pone un encabezado en la barra lateral.

Para preparar las opciones, `unique()` obtiene los valores distintos, `tolist()` los convierte en una lista y `sorted()` los ordena. En los años, `reverse=True` coloca primero el más reciente.

`st.sidebar.selectbox()` permite elegir un año. `st.sidebar.multiselect()` permite elegir varios países o perfiles. El argumento `help` añade la explicación de cada filtro.

La app copia `df` en `datos_grupo`. Si se han elegido países, aplica:

```python
datos_grupo = datos_grupo[datos_grupo["pais"].isin(paises)]
```

`isin()` comprueba si cada país pertenece a la lista seleccionada. Los corchetes conservan las filas donde la condición es verdadera. Después se aplica el mismo procedimiento con los perfiles: una fila debe cumplir ambos filtros si los dos tienen selección.

Los bloques `if paises:` e `if perfiles:` hacen que una lista vacía incluya todas las opciones de ese filtro. Si la combinación no devuelve datos, la app muestra un aviso y se detiene.

`", ".join(...)` une las opciones seleccionadas en un texto. Ese texto se guarda en `contexto` para indicar qué grupo se está mostrando.

### 5.9. Agregación y cálculo del porcentaje

Primero se calcula el total de respuestas de cada año:

```python
totales = (
    datos_grupo.drop_duplicates(["año", "pais", "perfil"])
    .groupby("año")["respuestas_grupo"].sum()
)
```

- `drop_duplicates()` conserva una fila por año, país y perfil. Así no se suma el mismo denominador una vez por cada lenguaje.
- `groupby("año")` reúne los grupos del mismo año.
- `sum()` suma sus respuestas.

Después, `groupby(["año", "lenguaje"], as_index=False)["personas"].sum()` suma las personas de cada lenguaje y año entre los países y perfiles elegidos. `as_index=False` mantiene año y lenguaje como columnas. El resultado se llama `historico`.

`historico["año"].map(totales)` asigna a cada fila el total de respuestas de su año. Finalmente:

```python
historico["porcentaje"] = (
    100 * historico["personas"] / historico["respuestas_grupo"]
).round(2)
```

`round(2)` redondea a dos decimales. Por ejemplo, 250 personas de 1.000 respuestas representan un 25 %. El cálculo utiliza las personas y los denominadores agregados; no hace una media simple de los porcentajes de los países.

Una persona puede seleccionar varios lenguajes, así que sus porcentajes no tienen por qué sumar 100 %. Los totales corresponden a cada edición: no representan personas únicas entre todos los años.

`filtrado` conserva las filas de `historico` cuyo año coincide con el seleccionado. Si ese año no tiene datos para el grupo elegido, se muestra un aviso y se detiene la ejecución.

### 5.10. Indicadores del resumen

`sort_values(["porcentaje", "lenguaje"], ascending=[False, True])` ordena el ranking por porcentaje descendente y, en caso de empate, por nombre ascendente.

`ranking.iloc[0]` obtiene la primera fila, que se guarda en `lider`. `ranking["respuestas_grupo"].iloc[0]` obtiene el denominador del año: se toma una vez porque se repite en las filas del ranking. `int()` lo convierte en entero para mostrarlo.

`st.columns(3)` crea tres columnas y cada llamada a `metric()` muestra un indicador: respuestas, lenguaje líder y porcentaje del líder. Las cadenas con prefijo `f` insertan variables en el texto; `:,.0f` sería un número sin decimales con separadores, `:,` aplica separadores al entero usado aquí y `:.2f` muestra dos decimales en el porcentaje.

`st.write()` genera una frase con el resultado. Si hay menos de 30 respuestas, `st.caption()` muestra una nota sobre el tamaño del grupo.

### 5.11. Gráfico de barras

```python
top_10 = ranking.head(10).set_index("lenguaje")[["porcentaje"]]
```

`head(10)` toma hasta diez lenguajes. `set_index("lenguaje")` utiliza sus nombres como etiquetas. `[["porcentaje"]]` conserva esa columna como tabla. `rename()` cambia el encabezado a `Uso (%)`.

`st.bar_chart(top_10, sort=False)` dibuja las barras respetando el orden del ranking.

### 5.12. Gráfico de evolución

`st.multiselect()` muestra los lenguajes disponibles en `historico`. `default=ranking["lenguaje"].head(3).tolist()` propone inicialmente los tres primeros del ranking actual.

Si hay lenguajes elegidos, `isin(seleccion)` conserva sus filas. Después:

```python
evolucion = datos_evolucion.pivot(
    index="año", columns="lenguaje", values="porcentaje"
)
```

`pivot()` reorganiza la tabla: cada fila es un año, cada columna es un lenguaje y cada celda contiene el porcentaje.

`reindex(sorted(df["año"].unique()))` añade al índice todos los años disponibles en el conjunto validado. Los años sin datos para una combinación quedan como valores ausentes; no se rellenan con cero.

`evolucion.index.astype(str)` convierte los años a etiquetas de texto. `evolucion.index.name = "Año"` asigna un nombre al índice. `st.line_chart()` dibuja las líneas y un `st.expander()` permite abrir la tabla de porcentajes.

### 5.13. Tabla del ranking

Un `st.expander()` contiene un `st.dataframe()` con las columnas año, lenguaje, personas y porcentaje de `ranking`. Muestra todos los lenguajes del ranking filtrado, aunque las barras solo muestren los diez primeros.

### 5.14. Fuente y contexto

`st.markdown()` muestra el enlace a Stack Overflow Developer Survey. `st.caption()` explica que las opciones y las personas participantes pueden cambiar entre ediciones, por lo que la comparación es descriptiva.

### 5.15. Qué ocurre cuando se cambia un filtro

Streamlit vuelve a ejecutar el script de arriba abajo cuando cambia un control. Los controles proporcionan sus valores actuales y el código vuelve a filtrar, agregar y dibujar los resultados. La lectura del archivo puede reutilizarse gracias a `@st.cache_data`.

## 6. Relación con `app_ejemplo.py`

Ambos archivos siguen los pasos de carga, comprobación, exploración, filtros, indicadores, gráficos y tabla. La app principal añade al final la fuente y el contexto.

La plantilla tiene una función `leer_csv(origen)` que también usa `pd.read_csv()` y `@st.cache_data`, pero no recibe la fecha de modificación. Su filtro usa una columna categórica, sus indicadores cuentan registros y calculan una media con `mean()`, y su gráfico agrupa por una categoría para mostrar esa media.

En `app.py`, los datos ya son recuentos resumidos de encuestas: por eso se suman personas y denominadores y se recalculan porcentajes. También se incorporan los filtros por país y perfil y la evolución temporal. Los comentarios `TODO` de la plantilla son ejercicios pendientes, no instrucciones que Python ejecute.

## 7. Problemas habituales

| Mensaje o situación | Qué revisar |
| --- | --- |
| No se reconoce `py` o `python` | Comprueba que Python esté instalado y disponible desde la terminal. |
| No existe `venv\Scripts\python.exe` | Crea el entorno desde la carpeta del proyecto. |
| `ModuleNotFoundError` | Instala `requirements.txt` con el intérprete de `venv`. |
| No se encuentra el CSV | Comprueba `RUTA_CSV` y que el archivo esté dentro de `datos`. |
| Faltan columnas | Comprueba los encabezados, sus acentos y el separador. Debe ser el CSV resumido. |
| Error al leer el archivo | Revisa `SEPARADOR`, `CODIFICACION` y el contenido del CSV. |
| Valores vacíos o números incorrectos | Corrige los campos obligatorios del archivo. |
| Filas repetidas | Revisa las combinaciones de año, país, perfil y lenguaje. |
| No hay datos para la selección | Cambia el año, el país o el perfil; vacía países y perfiles para incluirlos todos. |
| Una línea tiene datos ausentes | El grupo no tiene un valor para ese lenguaje y año; no significa un uso del 0 %. |

Para cambiar de dataset, adapta la configuración y conserva el significado de las columnas requeridas. Cambiar solo el nombre o la ruta del archivo no permite utilizar un CSV con una estructura diferente.
