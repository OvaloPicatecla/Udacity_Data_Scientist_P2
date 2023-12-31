import sys, pickle, re
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sqlalchemy import create_engine

def load_data(database_filepath):
    '''
    Function made to load the data from the database and separate in categories
    Input: Path of the database
    Output: Variables X,y and the names of the categories
    '''
    table_name = 'Data_Table'
    engine = create_engine(f"sqlite:///{database_filepath}")
    df = pd.read_sql_table(table_name,engine)
    X = df["message"]
    y = df.drop(["message","id","genre","original"], axis=1)
    category_names = y.columns
    return X, y, category_names

def tokenize(text):
    '''
    Function to tokenize the twitter messages in the database 
    input: message text
    output: list of clean messages tokenized
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    # Return the list of tokens
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    return clean_tokens

def build_model():
    '''
    Function to build the model and optimize it 
    Input: none
    Output: Model
    '''
    # Create the pipeline
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    # Define the parameters grid
    parameters = {
        #'vect__ngram_range': [(1, 1), (1, 2)],
        'clf__estimator__n_estimators': [10, 50]  # Update parameter name to 'clf__estimator__n_estimators'
    }
    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Function to evaluate the model created and display its accuracy
    Input: Model, X and Y test variables and the categories 
    Output: Printing the classification report and the accuracy
    '''
    y_pred = model.predict(X_test)
    print(classification_report(y_pred, Y_test.values, target_names=category_names))
    print('Accuracy score: ' + str((y_pred == Y_test).mean().mean()))

def save_model(model, model_filepath):
    '''
    Quick Function to save the model 
    Input: Model and its path
    Output: Model in a pickle file
    '''
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()