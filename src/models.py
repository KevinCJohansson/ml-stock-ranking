import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42


class Winsorizer(BaseEstimator, TransformerMixin):
    """Begränsar varje kolumn till percentilgränser som lärs från träningsdata.

    Gränserna räknas i fit(), alltså bara på träningsdatan,
    och används sedan oförändrade på validering och test.
    """

    def __init__(self, lower=0.01, upper=0.99):
        self.lower = lower
        self.upper = upper

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        self.low_ = np.nanquantile(X, self.lower, axis=0)
        self.high_ = np.nanquantile(X, self.upper, axis=0)
        return self

    def transform(self, X):
        return np.clip(np.asarray(X, dtype=float), self.low_, self.high_)


def make_classifier(name):
    """Skapar själva modellen. Samma inställningar används i alla experiment."""
    if name == "Logistisk regression":
        return LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)
    if name == "Random forest":
        return RandomForestClassifier(n_estimators=300, min_samples_leaf=50,
                                      random_state=RANDOM_STATE, n_jobs=-1)
    if name == "Gradient boosting":
        return HistGradientBoostingClassifier(learning_rate=0.05, max_iter=100,
                                              max_depth=3, min_samples_leaf=20,
                                              early_stopping=False,
                                              random_state=RANDOM_STATE)
    raise ValueError(f"Okänd modell: {name}")


def make_model(name, features, winsor=False, sector=False):
    """Bygger hela pipelinen: förbehandling + modell.

    name     : "Logistisk regression", "Random forest" eller "Gradient boosting"
    features : listan med nyckeltal som ska användas
    winsor   : True = begränsa extremvärden till 1:a och 99:e percentilen
    sector   : True = ta med sektor som extra information
    """
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if winsor:
        numeric_steps.append(("winsor", Winsorizer()))
    numeric_steps.append(("scaler", StandardScaler()))

    transformers = [("num", Pipeline(numeric_steps), features)]
    if sector:
        transformers.append(("sector",
                             OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                             ["Sector"]))

    return Pipeline([
        ("prep", ColumnTransformer(transformers)),
        ("model", make_classifier(name)),
    ])