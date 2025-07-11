# -*- coding: utf-8 -*-
"""P3_Sentiment_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1g6PMofzrlopw5NUhVtQV9PMY0dmSLgXo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import string
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

df = pd.read_excel("/content/dataset.xlsx")
df["review"] = df["title"].astype(str) + " " + df["body"].astype(str)


def label_sentiment(rating):
    if rating <= 2:
        return "Negative"
    elif rating == 3:
        return "Neutral"
    else:
        return "Positive"
df["sentiment"] = df["rating"].apply(label_sentiment)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@w+|\#','', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

df["clean_review"] = df["review"].apply(clean_text)


plt.figure(figsize=(6,4))
sns.countplot(x='rating', data=df, palette="viridis")
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x='sentiment', data=df, palette='pastel', order=['Negative', 'Neutral', 'Positive'])
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()

def plot_rating_wordcloud(star):
    text = " ".join(df[df["rating"] == star]["clean_review"])
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Word Cloud - {star} Star Reviews")
    plt.show()

plot_rating_wordcloud(1)
plot_rating_wordcloud(5)


def plot_wordcloud(sentiment):
    text = " ".join(df[df["sentiment"] == sentiment]["clean_review"])
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Word Cloud - {sentiment}")
    plt.show()

plot_wordcloud("Positive")
plot_wordcloud("Negative")


vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["clean_review"])
y = df["sentiment"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
log_preds = log_model.predict(X_test)

nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
nb_preds = nb_model.predict(X_test)

print("Logistic Regression Report:\n")
print(classification_report(y_test, log_preds))

print("Naive Bayes Report:\n")
print(classification_report(y_test, nb_preds))

def plot_conf_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred, labels=["Negative", "Neutral", "Positive"])
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=["Negative", "Neutral", "Positive"],
                yticklabels=["Negative", "Neutral", "Positive"], cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title)
    plt.show()

plot_conf_matrix(y_test, log_preds, "Logistic Regression Confusion Matrix")
plot_conf_matrix(y_test, nb_preds, "Naive Bayes Confusion Matrix")