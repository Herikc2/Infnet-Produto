import streamlit run uber_pickups.py as st
from PIL import Image
import requests

#para rodar: streamlit run app.py

image = Image.open('logo.png')
st.image(image, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

# Título da página
st.title('Classificação de produtos')

# Adicione um campo de texto
user_input = st.text_input('Descrição produto:', placeholder='Digite um nome de produto...')

# Verifique se o botão foi pressionado
if st.button('Classificar'):

    # local da API
    url = 'http://127.0.0.1:5000/api/produtos'
    parametros = {
        'produto': user_input
    }
    response = requests.get(url, params=parametros)

    if response.status_code == 200:
        # Converter a resposta JSON em um dicionário Python
        data = response.json()

        # Agora você pode acessar os dados da resposta como um dicionário
        st.write("Produto:", data['dados']['produto'], ' deve ser classificado como ', data['dados']['classificacao'])
    else:
        st.write("A chamada à API falhou com código de resposta:", response.status_code)    

    # Exiba o texto digitado pelo usuário
    # st.write('O produto (', user_input, ') é classificado como', 'Papelaria')