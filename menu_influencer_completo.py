
import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Menu+Influencer AI", layout="centered")
st.title("🖼️ Menu+Influencer AI – Genera imágenes de productos mejoradas o con influencers")

st.markdown("Sube una imagen de tu producto y elige si deseas mejorar su presentación visual o mostrarlo con un avatar influencer.")

openai_api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI", type="password")
uploaded_file = st.file_uploader("📷 Sube la imagen del producto (jpg/png)", type=["jpg", "jpeg", "png"])

generation_type = st.radio("¿Qué deseas generar?", ["✨ Imagen mejorada del producto", "🤳 Imagen con avatar influencer"])

avatar_selected = None
avatar_prompt = ""
if generation_type == "🤳 Imagen con avatar influencer":
    avatar_options = {
        "Luna": "A young woman with long straight black hair, medium skin tone, wearing a beige bomber jacket and jeans, standing confidently in a trendy café. She is holding the product described in the image.",
        "Nico": "A relaxed young man with curly hair, medium brown skin, wearing a white t-shirt and linen pants, sitting in a cozy outdoor terrace. He is holding the product described in the image.",
        "Valentina": "A confident professional woman with blonde hair and light skin, wearing a white blazer and jeans, sitting at a minimalist table. She is holding the product described in the image.",
        "Chef Juan": "A middle-aged man with tanned skin and gray hair, wearing a white chef uniform, standing in a rustic kitchen. He is holding the product described in the image.",
        "Sofi": "A cheerful teenage girl with pink-streaked hair, light skin, wearing pastel-colored clothes, standing in a candy-themed café. She is holding the product described in the image."
    }
    avatar_selected = st.selectbox("Selecciona un avatar influencer:", list(avatar_options.keys()))
    avatar_prompt = avatar_options[avatar_selected]

if uploaded_file and openai_api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen original", use_column_width=True)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("🎯 Generar imagen"):
        with st.spinner("Generando imagen con IA..."):
            try:
                base_prompt = "Describe esta imagen y genera un prompt para una imagen de producto en estilo profesional. Formato vertical, fondo bonito, luz cálida, lista para redes sociales."                     if generation_type == "✨ Imagen mejorada del producto"                     else f"Describe esta imagen y genera un prompt para una imagen realista de {avatar_prompt} Luz cálida, formato vertical estilo Instagram."

                gpt_response = openai.ChatCompletion.create(
                    model="gpt-4-vision-preview",
                    api_key=openai_api_key,
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": base_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    max_tokens=400
                )
                prompt = gpt_response.choices[0].message.content
                st.success("✅ Prompt generado con éxito")
                st.text_area("📄 Prompt generado", value=prompt, height=200)

                dalle_response = openai.Image.create(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    api_key=openai_api_key,
                    response_format="url"
                )
                image_url = dalle_response["data"][0]["url"]
                st.image(image_url, caption="🖼️ Imagen generada por IA", use_column_width=True)

                image_data = requests.get(image_url).content
                st.download_button("📥 Descargar imagen", data=image_data, file_name="imagen_generada.jpg", mime="image/jpeg")

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("🔼 Sube una imagen y coloca tu API Key para comenzar.")
