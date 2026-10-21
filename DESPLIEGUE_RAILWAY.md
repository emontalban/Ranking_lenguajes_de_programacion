# ⭐ Nivel avanzado: publicad vuestra app en internet con Railway

**Para equipos que ya tienen la app mínima funcionando · unos 15 minutos · una cuenta por equipo**

Ahora mismo vuestra app vive en `localhost`: solo existe en vuestro ordenador. Desplegarla significa que un servidor en internet ejecuta el mismo código y os da una URL pública que cualquiera puede abrir, también desde el móvil.

```
Código en GitHub  →  Railway lo descarga  →  instala requirements.txt  →  arranca streamlit  →  URL pública
```

## Antes de empezar: comprobad esto

- [ ] `streamlit run app.py` funciona en vuestro ordenador **sin errores**.
- [ ] Usáis `MODO_CARGA = "repo"` y el CSV está **dentro de `datos/`** y subido a GitHub. (Con `"subir"` también funciona, pero quien abra la app tendrá que subir el CSV.)
- [ ] Los datos son públicos: si el repo es público, el CSV también lo será.
- [ ] Todo está subido a GitHub: `git add . && git commit -m "App lista" && git push`.
- [ ] El repo tiene subido `requirements.txt`, `railway.json` y `.python-version` (vienen en la plantilla: **no los borréis**).

> 👤 **¿Quién crea la cuenta?** La persona que creó el repositorio del equipo en GitHub (la propietaria). Railway solo puede leer los repos de la cuenta con la que os registráis.

## Paso 1 · Crear la cuenta (2 min)

1. Entrad en [railway.com](https://railway.com) → **Login** → **Continue with GitHub**.
2. Autorizad a Railway y aceptad las condiciones.
3. Os asigna el plan de prueba gratuito. Las condiciones actuales están en [railway.com/pricing](https://railway.com/pricing): en octubre de 2026 son 30 días y 5 $ de crédito, sin tarjeta. Una app como la nuestra consume muy poco.

## Paso 2 · Crear el proyecto desde GitHub (3 min)

1. En el panel: **New Project** (o **+ New**) → **Deploy from GitHub repo**.
2. La primera vez os pedirá **Configure GitHub App**: elegid *Only select repositories*, marcad el repo del equipo y guardad.
3. Volved a Railway y seleccionad el repo. Se crea un **servicio** y empieza el primer despliegue.

## Paso 3 · Esperar al build (3-5 min)

Pulsad sobre el servicio → pestaña **Deployments** → **View logs**.

- **Build logs:** Railway detecta Python, lee `.python-version` e instala lo que hay en `requirements.txt`.
- **Deploy logs:** arranca la app con el comando de `railway.json`:

  ```
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
  ```

  - `$PORT` es el puerto que Railway asigna.
  - `0.0.0.0` permite conexiones desde fuera del servidor.
  - `headless` evita que Streamlit intente abrir un navegador.

Cuando veáis algo como `You can now view your Streamlit app in your browser` y el despliegue en verde (**Active**), la app está en marcha.

## Paso 4 · Generar la URL pública (1 min)

1. En el servicio: **Settings → Networking → Public Networking → Generate Domain**.
2. Si os pregunta el puerto, escribid el que aparece en los Deploy Logs (la línea `URL: http://0.0.0.0:XXXX`).
3. Railway os da una dirección del tipo `https://app-equipo-xxxx.up.railway.app`.

Abridla en el navegador y en el móvil. 🎉 **¡Vuestra app ya está en internet!**

## Paso 5 · Actualizar la app

Cada `git push` a la rama `main` vuelve a desplegar la app automáticamente. Cambiad el título, haced push y mirad cómo se actualiza en uno o dos minutos.

## Cuando acabe el taller

Para no gastar el crédito de prueba: servicio → **Settings** → abajo del todo, **Delete Service** (o borrad el proyecto entero en *Project Settings → Danger*). El código sigue a salvo en GitHub.

## Si algo falla

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| El build falla con `No module named ...` | Falta la librería en `requirements.txt` | Añadidla (una por línea), push |
| `FileNotFoundError` en los Deploy Logs | El CSV no está subido o la ruta tiene mayúsculas distintas | Linux distingue `Datos.csv` de `datos.csv`: revisad `RUTA_CSV` y haced push del CSV |
| La URL muestra *Application failed to respond* | La app no escucha en el puerto de Railway | Comprobad que `railway.json` sigue en la raíz; en **Settings → Deploy → Custom Start Command** pegad el comando del paso 3 |
| La URL pide un puerto o no carga | Puerto del dominio distinto al de la app | En **Networking**, editad el dominio y poned el puerto de los Deploy Logs |
| No aparece vuestro repo en Railway | Railway no tiene permiso | Repetid **Configure GitHub App** y marcad el repo, o crea la cuenta la propietaria del repo |
| `Trial expired` / sin crédito | Se acabó la prueba | Avisad a la docente: la app sigue funcionando en local |

📚 Más información: [docs.railway.com](https://docs.railway.com)
