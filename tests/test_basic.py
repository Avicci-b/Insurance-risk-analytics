# tests/test_basic.py
"""Basic tests for the insurance analytics project."""

def test_imports():
    """Test that required packages can be imported."""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    
    assert True  # If we get here, imports worked

def test_data_structure():
    """Test that data directory structure exists."""
    import os
    
    # Check required directories exist
    required_dirs = ['data/raw', 'data/processed', 'src', 'tests']
    
    for directory in required_dirs:
        assert os.path.exists(directory) or os.path.exists(f"../{directory}"), \
            f"Directory {directory} does not exist"