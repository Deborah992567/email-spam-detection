"""
ML evaluation script.
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ml.dataset.loader import load_and_prepare
from ml.training.trainer import train_models


def evaluate(dataset_path: str):
    print(f"Loading dataset: {dataset_path}")
    df, stats = load_and_prepare(dataset_path)
    print(f"Dataset: {stats['total']} samples ({stats['spam']} spam, {stats['ham']} ham)")

    print("\nTraining and evaluating models...")
    results = train_models(df)

    print(f"\nBest model: {results['best_model']} ({results['best_version']})")
    print(f"Train size: {results['train_size']}, Test size: {results['test_size']}")

    for name, metrics in results["results"].items():
        print(f"\n{'='*50}")
        print(f"Model: {name}")
        print(f"{'='*50}")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1 Score:  {metrics['f1_score']:.4f}")
        if "confusion_matrix" in metrics:
            cm = metrics["confusion_matrix"]
            print(f"\n  Confusion Matrix:")
            print(f"                 Predicted Ham  Predicted Spam")
            print(f"  Actual Ham:     {cm[0][0]:>12}  {cm[0][1]:>14}")
            print(f"  Actual Spam:    {cm[1][0]:>12}  {cm[1][1]:>14}")
        if "classification_report" in metrics:
            print(f"\n  Classification Report:")
            print(metrics["classification_report"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ML Model Evaluation")
    parser.add_argument("dataset", help="Path to CSV dataset")
    args = parser.parse_args()
    evaluate(args.dataset)
