import re
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.feature_extraction.text import TfidfVectorizer

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

vectorizer = TfidfVectorizer(max_features=50, ngram_range=(1,1))
X_vectorize = vectorizer.fit_transform(df["cleaned_review"])
Y = df["polarity"]

# Enable Truncated SVD for PCA conversion
svd = TruncatedSVD(n_components=2, random_state=42)
X_svd = svd.fit_transform(X_vectorize)
print("Variance: ", svd.explained_variance_ratio_.sum())

# PCA applied to TF-IDF feature space to reduce dimensionality (2D Visualisation)
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_svd)
plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=Y,
    cmap ="coolwarm",
    alpha=0.5
)
plt.title("PCA Projection of Amazon Reviews")
plt.xlabel("Maximum Variance Tendency")
plt.ylabel("Secondary Tendency")
plt.show()