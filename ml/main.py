"""
CLI entry point for the ML module.
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def cmd_train(args):
    from ml.dataset.loader import load_and_prepare
    from ml.training.trainer import train_models

    print(f"Loading dataset from: {args.dataset}")
    df, stats = load_and_prepare(args.dataset)
    print(f"Dataset loaded: {stats['total']} samples ({stats['spam']} spam, {stats['ham']} ham)")

    print("Training models...")
    results = train_models(df)

    print(f"\nBest model: {results['best_model']} ({results['best_version']})")
    print(f"Total samples: {results['total_samples']}")
    print(f"Train/Test split: {results['train_size']}/{results['test_size']}")

    for name, metrics in results["results"].items():
        print(f"\n--- {name} ---")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1 Score:  {metrics['f1_score']:.4f}")
        if "confusion_matrix" in metrics:
            print(f"  Confusion Matrix: {metrics['confusion_matrix']}")


def cmd_predict(args):
    from ml.prediction.predictor import predict_email

    result = predict_email(
        sender=args.sender or "unknown",
        subject=args.subject or "",
        body=args.body or "",
    )

    print(f"\nPrediction:  {result['prediction'].upper()}")
    print(f"Confidence:  {result['confidence']}%")
    print(f"Risk Level:  {result['risk_level']}")
    print(f"Model:       {result['algorithm']} ({result['model_version']})")

    if result["indicators"]:
        print("\nIndicators:")
        for ind in result["indicators"]:
            print(f"  [{ind['severity'].upper()}] {ind['description']}")


def cmd_info(args):
    from ml.models.model_manager import get_registry

    registry = get_registry()
    if not registry:
        print("No trained models found.")
        return

    print(f"Model Registry ({len(registry)} version(s)):\n")
    for entry in registry:
        print(f"  {entry['version']} - {entry['algorithm']}")
        print(f"    Accuracy:  {entry['accuracy']:.4f}")
        print(f"    Precision: {entry['precision']:.4f}")
        print(f"    Recall:    {entry['recall']:.4f}")
        print(f"    F1 Score:  {entry['f1_score']:.4f}")
        print(f"    Trained:   {entry['trained_at']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Email Spam Detection ML Module")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    train_parser = subparsers.add_parser("train", help="Train models")
    train_parser.add_argument("dataset", help="Path to CSV dataset")

    predict_parser = subparsers.add_parser("predict", help="Predict an email")
    predict_parser.add_argument("--sender", help="Sender email")
    predict_parser.add_argument("--subject", help="Email subject")
    predict_parser.add_argument("--body", help="Email body")

    subparsers.add_parser("info", help="Show model registry info")

    args = parser.parse_args()

    if args.command == "train":
        cmd_train(args)
    elif args.command == "predict":
        cmd_predict(args)
    elif args.command == "info":
        cmd_info(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
