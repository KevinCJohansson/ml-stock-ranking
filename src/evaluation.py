import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score


def evaluate(df, proba, name="Modell"):
    """Utvärderar en modell.

    df    : datan modellen testas på (måste ha above_median och next_year_return)
    proba : modellens sannolikhet för att aktien hamnar över medianen
    """
    y_true = df["above_median"]
    y_pred = (proba >= 0.5).astype(int)

    # Rangordna aktierna efter sannolikhet och ta ut topp- och botten-10 %
    ranked = df.assign(proba=proba).sort_values("proba", ascending=False)
    n = len(ranked) // 10
    top = ranked.head(n)["next_year_return"]
    bottom = ranked.tail(n)["next_year_return"]

    # Median i stället för medel
    return pd.Series({
        "Accuracy": accuracy_score(y_true, y_pred),
        "ROC-AUC": roc_auc_score(y_true, proba),
        "Topp 10 % (median avk.)": top.median(),
        "Botten 10 % (median avk.)": bottom.median(),
        "Alla (median avk.)": df["next_year_return"].median(),
    }, name=name).round(3)

def bootstrap_auc(df, proba, n_boot=1000, seed=42):
    """95 %-intervall för ROC-AUC med bootstrap.

    Drar nya urval av aktierna (med återläggning) många gånger och räknar
    ROC-AUC varje gång. Spridningen visar hur osäkert resultatet är.
    """
    rng = np.random.default_rng(seed)
    y = df["above_median"].to_numpy()
    proba = np.asarray(proba)
    scores = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        scores.append(roc_auc_score(y[idx], proba[idx]))
    low, high = np.percentile(scores, [2.5, 97.5])
    return round(low, 3), round(high, 3)