from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from sklearn.metrics import classification_report, confusion_matrix
import shap


def create_rfc_model(params: dict):
    model = RandomForestClassifier(**params)

    return model


def shap_explainer(model, X_test):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test)


def report(X_train, y_train, X_test, y_test, model):
    rfc_predict = model.predict(X_test)
    rfc_cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, rfc_predict))
    print("\n")
    print("=== Classification Report ===")
    print(classification_report(y_test, rfc_predict))
    print("\n")
    print("=== All AUC Scores ===")
    print(rfc_cv_score)
    print("\n")
    print("=== Mean AUC Score ===")
    print("Mean AUC Score - Random Forest: ", rfc_cv_score.mean())
