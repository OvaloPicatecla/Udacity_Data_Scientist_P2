# Udacity_Data_Scientist_P2

In this course, you've learned and built on your data engineering skills to expand your opportunities and potential as a data scientist. In this project, you'll apply these skills to analyze disaster data from Appen (formally Figure 8) to build a model for an API that classifies disaster messages.

In the Project Workspace, you'll find a data set containing real messages that were sent during disaster events. You will be creating a machine learning pipeline to categorize these events so that you can send the messages to an appropriate disaster relief agency.

There are three main keys for this project:

1. ETL Pipeline:
    Loads Datasets, merges and cleans them into one final SQLite Database.
   
2. ML Pipeline:
    Loads data from the SQLite database. plits the dataset into training and test sets and then builds a text processing and machine learning pipeline.
    Afterwards it trains and tunes a model using GridSearchCV, outputs results on the test set and finally it exports the model as a pickle file.
   
3. Flask Web App:
    Quick web setup to have some visualizations.
   
----

How to run the project files from the IDE Workspace:


Create a processed sqlite database:

python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db

To train and save a pkl model:

python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl

Deploy the application locally:

python run.py

----

Files in the Repository:

    - app
        -templates
            -go.html
            -master.html
        -run.py
    - data
        - DisasterResponse.db
        - YourDatabaseName.db
        - disaster_categories.csv
        - disaster_messages.csv
        - process_data.py
        
    - models
        - train_classifier.py

    - Clean_dataset.db
    - ETL Pirpeline Preparation.ipynb
    - ML PipeLine Preparation.ipynb
    -README.md
