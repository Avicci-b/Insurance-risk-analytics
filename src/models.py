"""
Model training and prediction utilities.
"""
from dataclasses import dataclass
from typing import Tuple, Any, Dict, List
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression
import joblib

# ========== Constants ==========
RANDOM_STATE = 42
TEST_SIZE = 0.2
CLASSIFIER_PARAMS = {
    'max_iter': 1000,
    'class_weight': 'balanced'
}
REGRESSOR_PARAMS = {
    'fit_intercept': True
}
# ================================

@dataclass
class ModelConfig:
    """Configuration for model training."""
    categorical_features: List[str]
    numerical_features: List[str]
    target_classification: str = 'HasClaim'
    target_regression: str = 'TotalClaims'
    test_size: float = TEST_SIZE
    random_state: int = RANDOM_STATE

class DataPreprocessor:
    """Handles data preprocessing pipelines."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.preprocessor = self._build_preprocessor()
    
    def _build_preprocessor(self) -> ColumnTransformer:
        """Create the preprocessing pipeline."""
        numerical_pipeline = Pipeline([
            ('scaler', StandardScaler())
        ])
        categorical_pipeline = Pipeline([
            ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ])
        return ColumnTransformer([
            ('num', numerical_pipeline, self.config.numerical_features),
            ('cat', categorical_pipeline, self.config.categorical_features)
        ])
    
    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.preprocessor.fit_transform(X)
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.preprocessor.transform(X)

class RiskModel:
    """Combined classification + regression model for risk scoring."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.preprocessor = DataPreprocessor(config)
        self.clf: LogisticRegression = None
        self.reg: LinearRegression = None
    
    def train_classifier(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train logistic regression classifier."""
        X_proc = self.preprocessor.fit_transform(X)
        self.clf = LogisticRegression(random_state=self.config.random_state, **CLASSIFIER_PARAMS)
        self.clf.fit(X_proc, y)
    
    def train_regressor(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train linear regression regressor."""
        X_proc = self.preprocessor.transform(X)  # use same preprocessing
        self.reg = LinearRegression(**REGRESSOR_PARAMS)
        self.reg.fit(X_proc, y)
    
    def predict_risk_score(self, X: pd.DataFrame) -> np.ndarray:
        """
        Compute risk score = probability_of_claim * predicted_claim_amount.
        """
        X_proc = self.preprocessor.transform(X)
        proba = self.clf.predict_proba(X_proc)[:, 1]
        amount = self.reg.predict(X_proc)
        # Normalize score to 0-100
        raw_score = proba * amount
        # You might want to store min/max from training to scale
        return raw_score  # or scale using training stats
    
    def save(self, path: str) -> None:
        joblib.dump({
            'config': self.config,
            'preprocessor': self.preprocessor,
            'clf': self.clf,
            'reg': self.reg
        }, path)
    
    @classmethod
    def load(cls, path: str) -> 'RiskModel':
        data = joblib.load(path)
        model = cls(data['config'])
        model.preprocessor = data['preprocessor']
        model.clf = data['clf']
        model.reg = data['reg']
        return model