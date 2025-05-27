# import necessary libraries
import re
import nltk
from bs4 import BeautifulSoup
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from germalemma import GermaLemma
from text_chunker import TextChunker

## _____________________________________________________________________________________________________________
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# ------------------------------------------------------------------------
lemmatizer_en = WordNetLemmatizer()
lemmatizer_de = GermaLemma()

## _____________________________________________________________________________________________________________
def preprocess_texts(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r'[^a-zA-ZäöüÄÖÜß\s]', ' ', text)

    try:
        language = detect(text)
    except:
        language = 'unknown'

    tokens = nltk.word_tokenize(text)

    if language == 'en':
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words]
        tokens = [lemmatizer_en.lemmatize(t) for t in tokens]

    elif language == 'de':
        stop_words = set(stopwords.words('german'))
        tokens = [t for t in tokens if t not in stop_words]
        tokens = [lemmatizer_de.find_lemma(t, 'N') or t for t in tokens]  # Default POS: NOUN
    else:
        tokens = [t for t in tokens if len(t) > 1]

    text = ' '.join(tokens).lower()

    return text

## _____________________________________________________________________________________________________________
def chunk_texts(text, max_length=300):
    chunker = TextChunker(maxlen=max_length)
    return list(chunker.chunk(text))

## _____________________________________________________________________________________________________________
# test if working
if __name__ == '__main__':
    text = preprocess_texts("Die Katzen liefen schnell durch den Garten.")
    print(text)
    print(chunk_texts(text, max_length=1000))
