import joblib
import pandas as pd
import numpy as np
import sys
import os

class IrisPredictor:
    def __init__(self, model_path='iris_model.joblib', metadata_path='model_metadata.joblib'):
        self.model = None
        self.feature_names = None
        self.target_names = None
        self.load_model(model_path, metadata_path)
    
    def load_model(self, model_path, metadata_path):
        """Load the trained model and metadata"""
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file '{model_path}' not found. Please train the model first.")
            
            if not os.path.exists(metadata_path):
                raise FileNotFoundError(f"Metadata file '{metadata_path}' not found.")
            
            self.model = joblib.load(model_path)
            metadata = joblib.load(metadata_path)
            
            self.feature_names = metadata['feature_names']
            self.target_names = metadata['target_names']
            
            print("✓ Model loaded successfully!")
            print(f"✓ Features: {', '.join(self.feature_names)}")
            print(f"✓ Classes: {', '.join(self.target_names)}")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            sys.exit(1)
    
    def validate_input(self, value, feature_name):
        """Validate user input"""
        try:
            val_float = float(value)
            
            # Basic range validation for Iris dataset features
            ranges = {
                'sepal length (cm)': (4.0, 8.0),
                'sepal width (cm)': (2.0, 4.5),
                'petal length (cm)': (1.0, 7.0),
                'petal width (cm)': (0.1, 2.5)
            }
            
            min_val, max_val = ranges.get(feature_name, (0, 10))
            if val_float < min_val or val_float > max_val:
                print(f"⚠️  Warning: {feature_name} is typically between {min_val} and {max_val}")
            
            return val_float
            
        except ValueError:
            raise ValueError(f"Invalid input for {feature_name}. Please enter a numeric value.")
    
    def get_user_input(self):
        """Get and validate user input"""
        print("\n" + "="*50)
        print("🌺 Iris Flower Classification")
        print("Enter the flower measurements in centimeters:")
        print("="*50)
        
        data = []
        for feature in self.feature_names:
            while True:
                try:
                    value = input(f"{feature}: ").strip()
                    if not value:
                        print("Please enter a value.")
                        continue
                    
                    validated_value = self.validate_input(value, feature)
                    data.append(validated_value)
                    break
                    
                except ValueError as e:
                    print(f"❌ {e}")
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    sys.exit(0)
        
        return pd.DataFrame([data], columns=self.feature_names)
    
    def predict_single(self):
        """Make a single prediction from user input"""
        sample_df = self.get_user_input()
        
        # Make prediction
        prediction = self.model.predict(sample_df)[0]
        probabilities = self.model.predict_proba(sample_df)[0]
        
        # Display results
        print("\n" + "="*50)
        print("📊 Prediction Results:")
        print("="*50)
        print(f"🎯 Predicted species: {self.target_names[prediction]}")
        
        print("\n📈 Prediction probabilities:")
        for i, prob in enumerate(probabilities):
            print(f"  {self.target_names[i]}: {prob:.2%}")
        
        return prediction, probabilities
    
    def predict_batch(self, data):
        """Make predictions for multiple samples"""
        if isinstance(data, list):
            data = pd.DataFrame(data, columns=self.feature_names)
        
        predictions = self.model.predict(data)
        probabilities = self.model.predict_proba(data)
        
        return predictions, probabilities

def main():
    """Main function"""
    try:
        predictor = IrisPredictor()
        
        while True:
            predictor.predict_single()
            
            # Ask if user wants to continue
            print("\n" + "-"*50)
            while True:
                continue_pred = input("Make another prediction? (y/n): ").strip().lower()
                if continue_pred in ['y', 'yes', '']:
                    break
                elif continue_pred in ['n', 'no']:
                    print("👋 Thank you for using the Iris classifier!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
                    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()