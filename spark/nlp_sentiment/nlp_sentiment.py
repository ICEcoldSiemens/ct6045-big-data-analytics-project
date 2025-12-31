import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# Loads Pig output cleaned Amazon review data
df = pd.read_csv('piggy_amazon_data.csv',
    header=None,
    names = ['polarity', 'full_review']
)

df['full_review'] = df['full_review'].fillna('') # Will deal with empty reviews

# Text-processing to eliminate filler words (is, the, and) + reduction to meaningful words
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocessing(text):
    text = text.lower() # makes text lowercase
    text = re.sub(r'[^a-z\s]', '',text) # removes punctuation and numbers

    # Begins tokenization and stopword removal process
    tokens = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return ' '.join(tokens)

df['cleaned_review'] = df['full_review'].apply(preprocessing)

# Will keep 50 words from vocabulary in dataset + will only look at single words
vectorizer = TfidfVectorizer(max_features=50, ngram_range=(1,1))
X = vectorizer.fit_transform(df['cleaned_review'])
feature_name = vectorizer.get_feature_names_out()
vectorizer_scores = X.mean(axis=0).A1
vectorizer_df = pd.DataFrame({
    "WORD": feature_name,
    "TF-IDF_SCORE": vectorizer_scores
}).sort_values(by="TF-IDF_SCORE", ascending=False)

wc = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate_from_frequencies(dict(zip(vectorizer_df["WORD"], vectorizer_df["TF-IDF_SCORE"])))

plt.figure(figsize=(12,6))
plt.imshow(wc.to_image(), interpolation="bilinear")
plt.title("Word Cloud (TF-IDF)")
plt.axis("off")
plt.show()

# Presents a word frequency bar chart based on TF-IDF values
plt.figure(figsize=(10,5))
plt.bar(vectorizer_df["WORD"], vectorizer_df["TF-IDF_SCORE"])
plt.title("Top Ten Frequent Words In The Amazon Review Dataset")
plt.xlabel("WORDS")
plt.ylabel("TF-IDF_SCORE")
plt.xticks(rotation = 45, ha="right")
plt.tight_layout()
plt.show()




