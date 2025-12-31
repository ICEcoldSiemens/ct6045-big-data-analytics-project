import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

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
df["polarity"] = df["polarity"].astype(int)


X = df["cleaned_review"]
Y = df["polarity"]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

vectorize = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
X_train_vector = vectorize.fit_transform(X_train)
X_test_vector = vectorize.transform(X_test)

# Logistic Regression
logic_reg = LogisticRegression(max_iter=1000)
logic_reg.fit(X_train_vector, Y_train)
Y_prediction_lr = logic_reg.predict(X_test_vector)
print("Logistic Regression Acc: ", accuracy_score(Y_test, Y_prediction_lr))
print(classification_report(Y_test, Y_prediction_lr))

# Naive Bayes
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_vector,Y_train)
Y_prediction_nb = naive_bayes.predict(X_test_vector)
print("Naive Bayes Acc: ", accuracy_score(Y_test, Y_prediction_nb))
print(classification_report(Y_test, Y_prediction_nb))