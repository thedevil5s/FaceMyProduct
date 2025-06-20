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

avatar_selected = None
if generation_type == '🤳 Imagen con avatar influencer':
    avatar_selected = st.selectbox('Selecciona un avatar influencer:', list(['Luna', 'Nico', 'Valentina', 'Chef Juan', 'Sofi']))
    avatar_prompt = {'Luna': 'Create a 4K vertical image of a Colombian influencer with long straight black hair, medium skin tone, wearing a beige bomber jacket and jeans. She is smiling and holding the exact product from the reference photo with one or both hands, standing in a cozy café with wooden furniture and brick walls. Maintain realism and lighting style for Instagram.', 'Nico': 'Create a 4K vertical image of a young Colombian man with medium brown skin, curly hair, white t-shirt, and linen pants. He is seated in a rustic outdoor café, holding the exact product from the reference photo. Natural light, relaxed posture, influencer-style photo.', 'Valentina': 'Create a 4K vertical image of a blonde woman influencer with fair skin, wearing a white blazer and jeans, sitting in a clean minimal coffee shop, smiling while holding the same product from the original image. Bright background, natural aesthetic.', 'Chef Juan': 'Create a 4K vertical image of a mature man with gray hair and tan skin wearing a white chef coat, standing in a rustic kitchen while presenting the exact same product from the original photo. Studio light, professional chef posture.', 'Sofi': 'Create a 4K vertical image of a cheerful teenage girl with pink streaks in her hair and light skin, wearing pastel colors, smiling and holding the same product from the image. Background: candy café or colorful aesthetic. Fun, influencer style.'}[avatar_selected]
else:
    avatar_prompt = '''Create a realistic professional image using the uploaded photo as reference. Preserve the exact shape, color, and details of the main product (e.g., bread, drink, dessert). Enhance the background and environment to match the product type: for bread use a warm wooden table and artisan bakery ambiance; for drinks, use café-style indoor lighting or a refreshing outdoor setup. Maintain clean aesthetics, soft shadows, natural light, and make the product stand out for advertising or menu use. Do not change the product’s identity. Format vertical, Instagram-ready.'''

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
                            {'type': 'text', 'text': avatar_prompt},
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
