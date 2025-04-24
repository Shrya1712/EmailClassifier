import os
import pandas as pd
import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

class EmailClassifier:
    def __init__(self, model_path=None):
        """
        Initialize the email classifier
        
        Args:
            model_path: Path to the saved model file. If None, a new model will be trained.
        """
        self.model_path = model_path or "email_classifier.pkl"
        
        # Load the model if it exists, otherwise train a new one
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train_model()
    
    def preprocess_text(self, text):
        """
        Preprocess text for classification
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if isinstance(text, str):
            # Convert to lowercase
            text = text.lower()
            # Remove special characters and numbers
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            # Remove extra whitespaces
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        return ''
    
    def load_data(self, data_path="combined_emails_with_natural_pii.csv"):
        """
        Load and prepare the dataset
        
        Args:
            data_path: Path to the dataset
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        # Load data
        df = pd.read_csv(data_path)
        
        # Extract email body and category
        # Assuming the last column is the category and the rest is the email body
        if len(df.columns) < 2:
            raise ValueError("Dataset must have at least 2 columns: email body and category")
        
        # Extract email body and category
        email_body_col = df.columns[0]
        category_col = df.columns[-1]
        
        # Preprocess email bodies
        df['processed_email'] = df[email_body_col].apply(self.preprocess_text)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            df['processed_email'], 
            df[category_col], 
            test_size=0.2, 
            random_state=42
        )
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, data_path="combined_emails_with_natural_pii.csv"):
        """
        Train the email classification model
        
        Args:
            data_path: Path to the dataset
        """
        # Load and prepare data
        X_train, X_test, y_train, y_test = self.load_data(data_path)
        
        # Create a pipeline with TF-IDF vectorizer and Multinomial Naive Bayes classifier
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        
        # Save the model
        self.save_model()
    
    def save_model(self):
        """
        Save the trained model to a file
        """
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """
        Load the trained model from a file
        """
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {self.model_path}")
    
    def predict(self, text):
        """
        Predict the category of an email
        
        Args:
            text: Email text to classify
            
        Returns:
            Predicted category
        """
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        # Make prediction
        return self.model.predict([processed_text])[0]
