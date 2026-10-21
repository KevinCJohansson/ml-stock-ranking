import pandas as pd
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