import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Menu+Influencer IA Adaptativa", layout="centered")
st.title("🧠 Imagen automática por producto + influencer")

st.markdown("Sube una imagen de tu producto. Detectamos qué es y generamos una imagen profesional con IA, con o sin influencer.")

openai_api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI", type="password")
if openai_api_key:
    openai_client = openai.OpenAI(api_key=openai_api_key)

uploaded_file = st.file_uploader("📷 Sube la imagen del producto (jpg/png)", type=["jpg", "jpeg", "png"])

generation_type = st.radio("¿Qué deseas generar?", ["✨ Imagen mejorada del producto", "🤳 Imagen con avatar influencer"])

avatar_prompts = {
    "Luna": "Luna is a Colombian woman with long black straight hair, medium skin tone, wearing a beige bomber jacket and jeans. She is seated in a cozy café with warm brick walls and wooden furniture. She is holding the product described below with a soft confident smile.",
    "Nico": "Nico is a young Colombian man with curly dark brown hair, medium tanned skin, white t-shirt and linen pants. He is in a tropical café terrace with rustic details. He is casually holding the product described below.",
    "Valentina": "Valentina is a blonde woman with fair skin wearing a white blazer and jeans. She is sitting in a bright minimal café holding the product. She looks confident and friendly.",
    "Chef Juan": "Chef Juan is a mature man with gray hair, tan skin, and a white chef coat. He is in a rustic kitchen, presenting the product as a proud chef.",
    "Sofi": "Sofi is a teenager with pink streaks in her hair, pastel clothes, and light skin. She’s smiling in a colorful café while holding the product playfully."
}

if generation_type == "🤳 Imagen con avatar influencer":
    avatar_selected = st.selectbox("Selecciona un avatar:", list(avatar_prompts.keys()))
else:
    avatar_selected = None

if uploaded_file and openai_api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Imagen original", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("🎯 Generar imagen automática"):
        with st.spinner("Analizando imagen y generando..."):
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres un experto en fotografía de productos y publicidad. Tu tarea es analizar la imagen y completar las siguientes variables del prompt: product_type, surface_type, background_type y detalles visibles como toppings, color o forma."},
                        {"role": "user", "content": [
                            {"type": "text", "text": "Analiza esta imagen y describe las siguientes variables:\n1. product_type\n2. surface_type\n3. background_type\n4. detalles"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    max_tokens=400
                )
                fields = response.choices[0].message.content

                avatar_prefix = avatar_prompts[avatar_selected] + " " if avatar_selected else ""

                final_prompt = f"""{avatar_prefix}
Create a realistic professional photo of a {fields}.
The item should retain its original shape, texture, and color.
Use natural lighting, soft shadows, vertical framing.
Photorealistic and suitable for Instagram or a digital menu."""

                st.text_area("📄 Prompt generado:", value=final_prompt.strip(), height=250)

                dalle_response = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=final_prompt,
                    size="1024x1024",
                    response_format="url"
                )
                image_url = dalle_response.data[0].url
                st.image(image_url, caption="🖼️ Imagen generada por IA", use_container_width=True)
                image_data = requests.get(image_url).content
                st.download_button("📥 Descargar imagen", data=image_data, file_name="imagen_generada.jpg", mime="image/jpeg")

            except Exception as e:
                st.error(f"❌ Error: {e}")
else:
    st.info("🔼 Sube una imagen, coloca tu API Key y selecciona una opción para comenzar.")
