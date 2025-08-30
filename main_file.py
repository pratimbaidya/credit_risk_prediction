import joblib

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from data_preprocessing_pipeline import wrangle
from model_training_pipeline import training
from model_evaluation_pipeline import classification_evaluation

train_df = pd.read_csv("GiveMeSomeCredit/cs-training.csv").drop(columns=["Unnamed: 0"])
test_df_index = pd.read_csv("GiveMeSomeCredit/cs-test.csv")

test_df = test_df_index.drop(columns=["Unnamed: 0"])

train_df, test_df = wrangle(train_df, test_df)

X = train_df.drop('SeriousDlqin2yrs', axis=1)
y = train_df['SeriousDlqin2yrs']

X_test = test_df.drop('SeriousDlqin2yrs', axis=1)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, stratify=y, random_state=42)

best_model = training(X_train, y_train)

classification_evaluation(best_model, X_train, y_train, X_val, y_val)