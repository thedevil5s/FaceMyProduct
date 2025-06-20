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

avatar_prompts = {'Luna': 'A vertical 4K photo of a Colombian woman influencer with long straight black hair, medium skin tone, wearing a beige bomber jacket and jeans. She is in a cozy café with wooden furniture and brick walls, holding a creamy beverage in a clear cup with whipped cream. The scene is softly lit, Instagram-style, and naturally composed.', 'Nico': 'A vertical 4K image of a relaxed Colombian man with curly hair and medium brown skin, wearing a white t-shirt and linen pants. He is seated outdoors at a cozy café, holding a refreshing red fruit drink with lime in a clear plastic cup. The atmosphere is tropical, modern, and styled for social media.', 'Valentina': 'A high-resolution image of a blonde influencer woman with fair skin, wearing a white blazer and jeans. She is seated at a minimalistic café, holding a dessert drink or stylish coffee. Bright background, clean look, Instagram-friendly.', 'Chef Juan': 'A 4K image of a mature man with tanned skin and gray hair, wearing a chef coat, in a rustic kitchen setting. He is holding a pastry or a traditional item in a professional and friendly manner. Warm light and clean visual aesthetic.', 'Sofi': 'A vibrant image of a young teenage girl with pink streaks in her hair, light skin, and pastel-colored clothing. She is in a colorful café environment, holding a sweet treat or drink. The vibe is playful, influencer-style, with soft lighting.'}

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
