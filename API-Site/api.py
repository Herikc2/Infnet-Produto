import unicodedata
import re
import string
import nltk

from flask import Flask, request, jsonify
from pickle import load
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#para rodar flask --app api run

app = Flask(__name__)

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Carregando catboost
pickle_model = open(r'models/catboost.pkl', 'rb')
catboost = load(pickle_model)
pickle_model.close()

# Carregando TF-IDF
pickle_tfidf = open(r'models/tfidf_catboost.pkl', 'rb')
tfidf = load(pickle_tfidf)
pickle_tfidf.close()

# Carregando LabelEncoder
pickle_labelEncoder = open(r'models/label_encoder.pkl', 'rb')
le = load(pickle_labelEncoder)
pickle_labelEncoder.close()

# pyspellchecker
spell = SpellChecker(language='pt')

def pyspellchecker(text):
    word_list = word_tokenize(text, language = 'portuguese')
    word_list_corrected = []
    for word in word_list:
        if word in spell.unknown(word_list) and len(word) > 3:
            word_corrected = spell.correction(word)
            if word_corrected == None:
                word_list_corrected.append(word)
            else:
                word_list_corrected.append(word_corrected)
        else:
            word_list_corrected.append(word)
    text_corrected = " ".join(word_list_corrected)
    return text_corrected

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def limpar_texto(text):
   text = str(text)

    # Remover caracteres non-ascii
   text = ''.join(caracter for caracter in text if ord(caracter) < 128)

    # Convertendo para lower case
   text = text.lower()

    # Removendo pontuação por expressão regular
   regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
   text = regex.sub(' ', str(text))

   text = re.sub('[^A-Za-z ]+', '', text)

    # Carregando stopwords em português
   portuguese_stops = set(stopwords.words('portuguese'))

    # Removendo stopwords em português
    # Mantendo somente palavras que não são consideradas stopwords
   text = ' '.join(palavra for palavra in text.split() if palavra not in portuguese_stops)

    # Remover palavras com menos de 2 caracteres
   words = text.split()
   text = [word for word in words if len(word) > 2 or word == ' ']
   text = ' '.join(text)

    # Corrigindo erros gramaticais
   text = pyspellchecker(text)

    # Criando a estrutura baseada em uma wordnet para lemmatization
   wordnet_lemmatizer = WordNetLemmatizer()
   # Aplicando Lemmatization
   text = ' '.join(wordnet_lemmatizer.lemmatize(palavra) for palavra in text.split())

    # Remover palavras com menos de 2 caracteres residuais
   words = text.split()
   text = [word for word in words if len(word) > 2 or word == ' ']
   text = ' '.join(text)

   text = strip_accents(text)

   return text

def previsao(text):
    classification = ''

    X = limpar_texto(text)

    X_tfidf = tfidf.transform([X])

    raw_classfication = catboost.predict(X_tfidf)[0][0]

    classification = le.inverse_transform([raw_classfication])[0]

    return classification

# Rota para obter todos os dados
@app.route('/api/produtos', methods=['GET'])

def obter_produtos():
    produto = request.args.get('produto')

    # aqui vamos rodar a rede
    classificacao = previsao(produto)

    dados = {"produto": produto, "classificacao": classificacao}

    return jsonify({"dados": dados})

if __name__ == '__main__':
    app.run(debug=True)