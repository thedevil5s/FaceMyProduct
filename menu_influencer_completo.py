
import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title='🖼️ IA Generador de Productos', layout='centered')
st.title('🖼️ Generador de Imagen con Prompt Personalizado')

st.markdown('Sube una imagen de tu producto o escena y escribe manualmente el prompt que deseas que DALL·E utilice.')

# API Key
openai_api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI", type="password")
if openai_api_key:
    openai_client = openai.OpenAI(api_key=openai_api_key)

# Imagen
uploaded_file = st.file_uploader("📷 Sube la imagen de referencia (jpg/png)", type=["jpg", "jpeg", "png"])

# Prompt personalizado
custom_prompt = st.text_area("✍️ Escribe tu prompt manualmente (en inglés para mejores resultados)", height=200)

if uploaded_file and openai_api_key and custom_prompt:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen original", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("🎯 Generar imagen"):
        with st.spinner("Generando imagen con IA..."):
            try:
                chat_response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": custom_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    max_tokens=400
                )
                interpreted_prompt = chat_response.choices[0].message.content
                st.success("✅ Prompt interpretado por GPT")
                st.text_area("🧠 Prompt final usado:", value=interpreted_prompt, height=180)

                dalle_response = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=interpreted_prompt,
                    size="1024x1024",
                    response_format="url"
                )
                image_url = dalle_response.data[0].url
                st.image(image_url, caption="🖼️ Imagen generada por IA", use_container_width=True)

                image_data = requests.get(image_url).content
                st.download_button("📥 Descargar imagen", data=image_data, file_name="imagen_generada.jpg", mime="image/jpeg")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("🔼 Sube una imagen, coloca tu API Key y escribe el prompt para comenzar.")
