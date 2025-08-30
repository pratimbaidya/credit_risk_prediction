import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (accuracy_score,
                             balanced_accuracy_score,
                             precision_score,
                             recall_score,
                             f1_score,
                             roc_auc_score,
                             roc_curve,
                             auc,
                             classification_report,
                             confusion_matrix,
                             ConfusionMatrixDisplay,)


def classification_evaluation(model, X_train, y_train, X_test, y_test, threshold=0.5):
    # ===== Train Predictions =====
    prob_train = model.predict_proba(X_train)[:, 1]
    y_pred_train = (prob_train >= threshold).astype(int)

    # ===== Test Predictions =====
    prob_test = model.predict_proba(X_test)[:, 1]
    y_pred_test = (prob_test >= threshold).astype(int)

    # ===== TRAIN METRICS =====
    print(f"\n------ Training Evaluation at threshold={threshold} ------")
    print(f"Accuracy:  {accuracy_score(y_train, y_pred_train):.4f}")
    print(f"Balanced Accuracy: {balanced_accuracy_score(y_train, y_pred_train):.4f}")
    print(f"Precision: {precision_score(y_train, y_pred_train):.4f}")
    print(f"Recall:    {recall_score(y_train, y_pred_train):.4f}")
    print(f"F1-Score:  {f1_score(y_train, y_pred_train):.4f}")
    print(f"AUC-ROC:   {roc_auc_score(y_train, prob_train):.4f}")

    print("\nClassification Report (Train):")
    print(classification_report(y_train, y_pred_train, digits=4))

    cm_train = confusion_matrix(y_train, y_pred_train)
    print("Confusion Matrix (Train):\n", cm_train)

    disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train)
    disp_train.plot(cmap="Blues", colorbar=False)
    plt.title("Confusion Matrix - Train")
    plt.show()

    # ===== TEST METRICS =====
    print(f"\n------ Testing Evaluation at threshold={threshold} ------")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred_test):.4f}")
    print(f"Balanced Accuracy: {balanced_accuracy_score(y_test, y_pred_test):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred_test):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred_test):.4f}")
    print(f"F1-Score:  {f1_score(y_test, y_pred_test):.4f}")
    print(f"AUC-ROC:   {roc_auc_score(y_test, prob_test):.4f}")

    # ===== Plot all the four Metrices ina single graph =====
    thresholds = np.arange(0, 1.01, 0.01)

    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []

    for t in thresholds:
        y_pred = (prob_test >= t).astype(int)
        accuracy_scores.append(accuracy_score(y_test, y_pred))
        precision_scores.append(precision_score(y_test, y_pred, zero_division=0))
        recall_scores.append(recall_score(y_test, y_pred, zero_division=0))
        f1_scores.append(f1_score(y_test, y_pred, zero_division=0))

    plt.figure(figsize=(10, 7))
    plt.plot(thresholds, accuracy_scores, label='Accuracy', color='purple', linestyle='-')
    plt.plot(thresholds, precision_scores, label='Precision', color='blue', linestyle='--')
    plt.plot(thresholds, recall_scores, label='Recall', color='green', linestyle='-.')
    plt.plot(thresholds, f1_scores, label='F1-Score', color='red', linestyle=':')

    plt.title('Performance Metrics vs. Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Score (0 to 1)')
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.legend()
    plt.show()

    print("\nClassification Report (Test):")
    print(classification_report(y_test, y_pred_test, digits=4))

    cm_test = confusion_matrix(y_test, y_pred_test)
    print("Confusion Matrix (Test):\n", cm_test)

    disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test)
    disp_test.plot(cmap="Oranges", colorbar=False)
    plt.title("Confusion Matrix - Test")
    plt.show()

    # ===== Test ROC Curve =====
    fpr, tpr, thresholds = roc_curve(y_test, prob_test)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()

