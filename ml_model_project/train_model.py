import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_and_save_model():
    try:
        # Load data
        print("Loading Iris dataset...")
        iris = load_iris(as_frame=True)
        X = iris.data
        y = iris.target
        feature_names = iris.feature_names
        target_names = iris.target_names
        
        print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"Features: {', '.join(feature_names)}")
        print(f"Target classes: {', '.join(target_names)}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Train model
        print("Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=3
        )
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel trained successfully!")
        print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Save model
        model_filename = 'iris_model.joblib'
        joblib.dump(model, model_filename)
        
        # Also save feature names and target names for prediction
        model_metadata = {
            'feature_names': feature_names.tolist(),
            'target_names': target_names.tolist(),
            'accuracy': accuracy
        }
        joblib.dump(model_metadata, 'model_metadata.joblib')
        
        print(f"\nModel saved as '{model_filename}'")
        print("Model metadata saved as 'model_metadata.joblib'")
        
        return model, accuracy
        
    except Exception as e:
        print(f"Error during model training: {str(e)}")
        raise

if __name__ == "__main__":
    train_and_save_model()