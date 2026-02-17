import pytest
import pandas as pd
import numpy as np
from src.models import ModelConfig, DataPreprocessor, RiskModel

@pytest.fixture
def sample_data():
    """Create a small sample dataframe for testing."""
    data = {
        'SumInsured': [10000, 20000, 15000, 30000],
        'PostalCode': ['A1', 'B2', 'A1', 'C3'],
        'VehicleType': ['SUV', 'Sedan', 'SUV', 'Truck'],
        'HasClaim': [0, 1, 0, 1],
        'TotalClaims': [0, 5000, 0, 12000]
    }
    return pd.DataFrame(data)

@pytest.fixture
def model_config():
    return ModelConfig(
        categorical_features=['PostalCode', 'VehicleType'],
        numerical_features=['SumInsured']
    )

def test_preprocessor_fit_transform(model_config, sample_data):
    pre = DataPreprocessor(model_config)
    X = sample_data[model_config.categorical_features + model_config.numerical_features]
    transformed = pre.fit_transform(X)
    assert transformed.shape[0] == len(sample_data)
    assert transformed.shape[1] == len(model_config.categorical_features) + len(model_config.numerical_features)

def test_risk_model_train_classifier(model_config, sample_data):
    model = RiskModel(model_config)
    X = sample_data[model_config.categorical_features + model_config.numerical_features]
    y = sample_data['HasClaim']
    model.train_classifier(X, y)
    assert model.clf is not None
    assert hasattr(model.clf, 'coef_')

def test_risk_model_train_regressor(model_config, sample_data):
    model = RiskModel(model_config)
    X = sample_data[model_config.categorical_features + model_config.numerical_features]
    # Need to pre-fit preprocessor
    model.preprocessor.fit_transform(X)
    y = sample_data['TotalClaims']
    model.train_regressor(X, y)
    assert model.reg is not None
    assert hasattr(model.reg, 'coef_')

def test_predict_risk_score(model_config, sample_data):
    
    model = RiskModel(model_config)
    X = sample_data[model_config.categorical_features + model_config.numerical_features]
    y_clf = sample_data['HasClaim']
    y_reg = sample_data['TotalClaims']
    model.train_classifier(X, y_clf)
    model.train_regressor(X, y_reg)
    scores = model.predict_risk_score(X)
    assert isinstance(scores, np.ndarray)
    assert scores.shape[0] == len(sample_data)
    assert len(scores) == len(sample_data)
    #assert all(scores >= 0)

def test_save_load_model(tmp_path, model_config, sample_data):
    model = RiskModel(model_config)
    X = sample_data[model_config.categorical_features + model_config.numerical_features]
    y_clf = sample_data['HasClaim']
    y_reg = sample_data['TotalClaims']
    model.train_classifier(X, y_clf)
    model.train_regressor(X, y_reg)
    path = tmp_path / "model.pkl"
    model.save(path)
    loaded = RiskModel.load(path)
    assert loaded.config == model.config
    # Check that loaded model can predict
    scores_loaded = loaded.predict_risk_score(X)
    scores_original = model.predict_risk_score(X)
    np.testing.assert_array_almost_equal(scores_loaded, scores_original)