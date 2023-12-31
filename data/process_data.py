import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Function to input the raw data and create a dataframe.
    inputs:messages_filepath, categories_filepath
    outputs: df - dataframe
    '''
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, on='id')
    return df

def clean_data(df):
    '''
    Function to clean the dataframe and separate categories:
    inputs: original df
    outputs: cleaned df
    '''
    categories = df['categories'].str.split(';', expand=True)
    row = categories.iloc[0]
    
    category_colnames = categories.iloc[0].apply(lambda x: x[:-2])
    category_colnames = category_colnames.tolist()
    categories.columns = category_colnames
    
    'Looping the columns:'
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = pd.to_numeric(categories[column])
        
    df = df.drop('categories', axis=1)
    df = pd.concat([df , categories], axis=1)
    df = df.drop_duplicates()
    df = df[df['related'] != 2]

    return df

def save_data(df, database_filepath):
    '''
    Saving the data
    inputs: Dataframe and its path
    outputs: none (saving)
    '''
    engine = create_engine('sqlite:///' + database_filepath)
    df.to_sql('Data_Table', engine, index=False, if_exists='replace')

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()