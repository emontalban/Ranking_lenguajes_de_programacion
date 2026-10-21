# 📊 Plantilla del reto · Mi primera app de datos con Streamlit

Plantilla para los equipos del taller **«De los datos a la web»** (Fundación Somos F5).

👉 **Empezad por aquí: [RETO.md](RETO.md)**, la ficha del reto con las fases, los niveles y la rúbrica.
⭐ **Nivel avanzado:** [DESPLIEGUE_RAILWAY.md](DESPLIEGUE_RAILWAY.md), para publicar la app en internet.

## Crear el repo del equipo

Una persona del equipo pulsa **Use this template → Create a new repository** (arriba a la derecha) y añade al resto como colaboradoras en **Settings → Collaborators**.

## Arrancar en local

```bash
cd <directorio-del-proyecto/reto>
python -m venv .venv
```

- **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
- **macOS / Linux:** `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
streamlit run app.py o nombre del archivo de tu app

```

La plantilla arranca con un dataset de ejemplo (movilidad ficticia en Madrid). Vuestro trabajo es sustituirlo por el vuestro.

## Estructura

```
├── app.py                  ← la app: editad el bloque CONFIGURACIÓN y los TODO
├── datos/
│   └── ejemplo_movilidad.csv  ← poned aquí vuestro CSV
├── requirements.txt        ← librerías (streamlit, pandas)
├── railway.json            ← comando de arranque para Railway (no tocar)
├── .python-version         ← versión de Python para Railway (no tocar)
├── RETO.md                 ← ficha del reto
└── DESPLIEGUE_RAILWAY.md   ← guía de publicación
```

## Nuestra app

> Completad esta sección al terminar.

- **Equipo:**
- **Pregunta que responde:**
- **Dataset y fuente:**
- **Enlace público (si la habéis publicado):**
- **Qué mejoraríamos:**
