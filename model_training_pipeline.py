import joblib

import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.model_selection import StratifiedKFold



def training(X_train, y_train):

    cost_for_positive_class = 13.96

    best_rfc = joblib.load("best_rfc.pkl")
    best_xgbc = joblib.load("best_xgbc.pkl")
    best_lgbmc = joblib.load("best_lgbmc.pkl")

    estimators = [
    ("rfc", best_rfc),
    ("xgb", best_xgbc),
    ("lgbm", best_lgbmc)
    ]

    final_estimator = LogisticRegression(solver='liblinear', max_iter=2000, class_weight={0:1, 1:cost_for_positive_class})

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    stacking_model = StackingClassifier(
        estimators=estimators,
        final_estimator=final_estimator,
        cv=cv,
        passthrough=False,
        n_jobs=1
    )

    stacking_model.fit(X_train, y_train)

    joblib.dump(stacking_model, "stacking_model.pkl")

    return stacking_model

    

