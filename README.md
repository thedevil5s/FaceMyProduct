
# Menu+Influencer AI

Una aplicación web creada con Streamlit que permite a los usuarios:

- Subir una imagen de su producto (bebida, comida, accesorio).
- Elegir si desean mejorar visualmente la imagen o agregar un avatar influencer.
- La IA analiza la imagen usando GPT-4o y genera un prompt.
- Se genera automáticamente una nueva imagen profesional con DALL·E 3.
- El usuario puede descargar la imagen final lista para redes sociales.

## Características

- ✅ Subida de imagen sencilla
- ✅ Opción de mejora visual o con influencer
- ✅ 5 avatares realistas predefinidos
- ✅ Generación automática vía OpenAI GPT-4o + DALL·E 3
- ✅ Descarga directa de imagen final

## Cómo usar

1. Subir este proyecto a un repositorio de GitHub.
2. Ir a [Streamlit Cloud](https://streamlit.io/cloud) y conectar el repositorio.
3. Establecer `menu_influencer_completo.py` como archivo principal.
4. ¡Listo! La app estará publicada online.

## Requisitos

- Una clave API de OpenAI con acceso a:
  - GPT-4 Vision (`gpt-4-vision-preview`)
  - DALL·E 3 (`dall-e-3`)
  - openai>=1.0.0


## Instalación local

```bash
pip install -r requirements.txt
streamlit run menu_influencer_completo.py
```

---

Desarrollado con ❤️ para emprendedores visuales.
