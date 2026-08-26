"""Machine learning model for risk prediction."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

class RiskPredictor:
    """Machine Learning model for mine safety risk prediction."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.performance_metrics = {}
        self.feature_importance = None
    
    def prepare_data(self):
        """Prepare data for model training."""
        # Target: HIGH/CRITICAL risk = 1, LOW/MEDIUM = 0
        self.df['risk_binary'] = ((self.df['combined_risk_score'] > 50) | (self.df['incident_flag'] == 1)).astype(int)
        
        # Select features
        self.feature_columns = [
            'gas_level', 'temperature', 'humidity', 'vibration', 'pressure', 'smoke_level',
            'worker_count', 'hour', 'weekday', 'is_night_shift',
            'gas_risk_score', 'temperature_risk_score', 'vibration_risk_score',
            'abnormal_gas_flag', 'abnormal_temperature_flag', 'abnormal_vibration_flag',
            'total_anomalies', 'zone_risk_baseline'
        ]
        
        # Handle missing values
        for col in self.feature_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].mean())
        
        # One-hot encode zone
        zone_dummies = pd.get_dummies(self.df['mine_zone'], prefix='zone')
        
        X = self.df[self.feature_columns].copy()
        X = pd.concat([X, zone_dummies], axis=1)
        y = self.df['risk_binary']
        
        return X, y
    
    def train_model(self, model_type='random_forest', test_size=0.2, random_state=42):
        """Train the risk prediction model."""
        X, y = self.prepare_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        elif model_type == 'logistic_regression':
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        else:
            raise ValueError("Model type must be 'random_forest' or 'logistic_regression'")
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        self._evaluate_model(X_train_scaled, X_test_scaled, y_train, y_test)
        
        # Store feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            self.feature_importance = feature_importance_df
        
        return self.model
    
    def _evaluate_model(self, X_train_scaled, X_test_scaled, y_train, y_test):
        """Evaluate model performance."""
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)
        y_test_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        self.performance_metrics = {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'precision': precision_score(y_test, y_test_pred),
            'recall': recall_score(y_test, y_test_pred),
            'f1_score': f1_score(y_test, y_test_pred),
            'roc_auc': roc_auc_score(y_test, y_test_proba),
            'confusion_matrix': confusion_matrix(y_test, y_test_pred).tolist(),
        }
    
    def predict_risk(self, X):
        """Predict risk for new data."""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        return predictions, probabilities
    
    def get_model_summary(self):
        """Get model summary and performance metrics."""
        summary = {
            'model_type': type(self.model).__name__,
            'performance_metrics': self.performance_metrics,
            'feature_importance': self.feature_importance.to_dict() if self.feature_importance is not None else None,
        }
        return summary
    
    def predict_for_latest(self, n_records=1):
        """Predict risk for latest readings."""
        X, y = self.prepare_data()
        X_latest = X.tail(n_records)
        
        predictions, probabilities = self.predict_risk(X_latest)
        
        results = pd.DataFrame({
            'timestamp': self.df.tail(n_records)['timestamp'].values,
            'zone': self.df.tail(n_records)['mine_zone'].values,
            'predicted_risk': predictions,
            'risk_probability': np.round(probabilities, 4),
            'risk_level': ['HIGH RISK' if p > 0.6 else 'SAFE' for p in probabilities]
        })
        
        return results


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_features.csv')
    predictor = RiskPredictor(df)
    predictor.train_model(model_type='random_forest')
    summary = predictor.get_model_summary()
    print("Model trained successfully!")
    print(f"Test Accuracy: {summary['performance_metrics']['test_accuracy']:.4f}")
