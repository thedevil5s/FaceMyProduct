import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title='Menu+Influencer AI', layout='centered')
st.title('🖼️ Menu+Influencer AI – Genera imágenes de productos mejoradas o con influencers')

st.markdown('Sube una imagen de tu producto y elige si deseas mejorar su presentación visual o mostrarlo con un avatar influencer.')

openai_api_key = st.text_input('🔑 Ingresa tu API Key de OpenAI', type='password')
if openai_api_key:
    openai_client = openai.OpenAI(api_key=openai_api_key)

uploaded_file = st.file_uploader('📷 Sube la imagen del producto (jpg/png)', type=['jpg', 'jpeg', 'png'])

generation_type = st.radio('¿Qué deseas generar?', ['✨ Imagen mejorada del producto', '🤳 Imagen con avatar influencer'])

avatar_prompts = {'Luna': 'A high-resolution vertical photo of a beautiful Colombian woman named Luna, with long straight black hair and medium skin tone, sitting in a cozy coffee shop with warm brick walls and wooden furniture. She is wearing a beige bomber jacket and jeans. She smiles gently while holding a creamy chocolate frappe with whipped cream and syrup in a clear branded cup that says “Café Ancestral”. The image has natural lighting, soft shadows, and professional Instagram-style composition.', 'Nico': 'A stylish vertical 4K photo of a young Colombian man named Nico, with curly dark brown hair and medium tanned skin. He is sitting at a rustic wooden café table on a terrace with plants in the background. He wears a white t-shirt and light linen pants. He is smiling while holding a tropical fruit drink in a clear plastic cup with a straw. The image is lit with natural soft daylight, perfect for social media or menu photography.', 'Valentina': 'A clean and professional photo of a confident Colombian woman named Valentina. She has fair skin, straight blonde hair, and wears a white blazer and light jeans. She is sitting at a bright modern café table with minimal decor. She is smiling and holding a dessert-style latte or frappe in a clear cup with whipped cream. The scene is light, modern, and professionally styled with soft highlights.', 'Chef Juan': 'A 4K vertical image of a mature man named Juan, with gray hair, medium tanned skin, and a kind smile. He wears a traditional white chef coat and stands proudly in a rustic kitchen with wooden shelves and warm ambient lighting. He holds a traditional Colombian pastry on a ceramic plate, presenting it toward the camera. The image is sharp, warm, and styled like a food magazine feature.', 'Sofi': 'A vibrant vertical portrait of a cheerful teenage girl named Sofi, with pastel pink streaks in her long hair and light skin tone. She is wearing colorful pastel clothes, standing in a playful candy-themed café. She is holding a sweet dessert drink topped with cream and sprinkles in a fun, branded cup. The setting is full of color and energy, perfect for TikTok or Instagram aesthetic.'}

avatar_selected = None
if generation_type == '🤳 Imagen con avatar influencer':
    avatar_selected = st.selectbox('Selecciona un avatar influencer:', list(avatar_prompts.keys()))
    final_prompt = avatar_prompts[avatar_selected]
else:
    final_prompt = '''Analyze the uploaded photo and generate a professional image of the same food item. Keep the product’s shape, size, texture, and color. Based on what type of item it is (bread, rice, dessert, drink, etc.), place it in a realistic and fitting environment: for bread, use warm wooden surfaces and bakery ambiance; for rice or meals, use ceramic plates and restaurant-style background; for drinks, use café settings. Natural light, soft shadows, vertical format. Do not alter the product itself.'''

if uploaded_file and openai_api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen original', use_container_width=True)
    buffered = io.BytesIO()
    image.save(buffered, format='JPEG')
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    if st.button('🎯 Generar imagen'):
        with st.spinner('Generando imagen con IA...'):
            try:
                chat_response = openai_client.chat.completions.create(
                    model='gpt-4o',
                    messages=[
                        {'role': 'user', 'content': [
                            {'type': 'text', 'text': final_prompt},
                            {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}}
                        ]}
                    ],
                    max_tokens=400
                )
                prompt = chat_response.choices[0].message.content
                st.success('✅ Prompt generado con éxito')
                st.text_area('📄 Prompt generado', value=prompt, height=200)

                dalle_response = openai_client.images.generate(
                    model='dall-e-3',
                    prompt=prompt,
                    size='1024x1024',
                    response_format='url'
                )
                image_url = dalle_response.data[0].url
                st.image(image_url, caption='🖼️ Imagen generada por IA', use_container_width=True)
                image_data = requests.get(image_url).content
                st.download_button('📥 Descargar imagen', data=image_data, file_name='imagen_generada.jpg', mime='image/jpeg')
            except Exception as e:
                st.error(f'Error: {e}')
else:
    st.info('🔼 Sube una imagen y coloca tu API Key para comenzar.')
