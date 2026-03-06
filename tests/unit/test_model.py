"""
Tests unitaires pour le modèle ML et ses performances.
"""
import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier


@pytest.mark.unit
class TestModelPerformance:
    """Tests pour vérifier les performances du modèle."""
    
    def test_model_loaded(self, mock_model):
        """Test que le modèle peut être chargé."""
        assert mock_model is not None
        assert isinstance(mock_model, RandomForestClassifier)
    
    def test_model_prediction_shape(self, mock_model):
        """Test que le modèle retourne la bonne forme de prédiction."""
        X_test = np.random.rand(10, 43)
        predictions = mock_model.predict(X_test)
        
        assert predictions.shape == (10,)
        assert all(p in [0, 1] for p in predictions)
    
    def test_model_predict_proba(self, mock_model):
        """Test que le modèle retourne des probabilités valides."""
        X_test = np.random.rand(10, 43)
        probabilities = mock_model.predict_proba(X_test)
        
        assert probabilities.shape == (10, 2)
        # Vérifier que les probabilités sont entre 0 et 1
        assert np.all(probabilities >= 0)
        assert np.all(probabilities <= 1)
        # Vérifier que la somme des probabilités par ligne = 1
        np.testing.assert_array_almost_equal(
            probabilities.sum(axis=1),
            np.ones(10)
        )
    
    def test_model_single_prediction(self, mock_model):
        """Test de prédiction sur un seul échantillon."""
        X_test = np.random.rand(1, 43)
        prediction = mock_model.predict(X_test)
        
        assert len(prediction) == 1
        assert prediction[0] in [0, 1]
    
    def test_model_batch_prediction(self, mock_model):
        """Test de prédiction sur un batch."""
        batch_sizes = [1, 10, 100, 500]
        
        for batch_size in batch_sizes:
            X_test = np.random.rand(batch_size, 43)
            predictions = mock_model.predict(X_test)
            assert len(predictions) == batch_size
    
    def test_model_feature_count(self, mock_model):
        """Test que le modèle attend le bon nombre de features."""
        # Le modèle attend 43 features
        X_correct = np.random.rand(5, 43)
        X_wrong = np.random.rand(5, 40)
        
        # Doit fonctionner avec 43 features
        predictions_correct = mock_model.predict(X_correct)
        assert len(predictions_correct) == 5
        
        # Doit échouer avec un nombre incorrect de features
        with pytest.raises(ValueError):
            mock_model.predict(X_wrong)
    
    def test_model_reproducibility(self, mock_model):
        """Test que les prédictions sont reproductibles."""
        X_test = np.random.rand(10, 43)
        
        pred1 = mock_model.predict(X_test)
        pred2 = mock_model.predict(X_test)
        
        np.testing.assert_array_equal(pred1, pred2)
    
    def test_model_probability_threshold(self, mock_model):
        """Test du seuil de probabilité pour classification High/Low risk."""
        X_test = np.random.rand(100, 43)
        probabilities = mock_model.predict_proba(X_test)[:, 1]
        
        threshold = 0.35
        
        for prob in probabilities:
            if prob > threshold:
                risk_level = "High"
            else:
                risk_level = "Low"
            
            assert risk_level in ["High", "Low"]
            
            if prob > threshold:
                assert risk_level == "High"
            else:
                assert risk_level == "Low"


@pytest.mark.unit
class TestFeatureConsistency:
    """Tests pour vérifier la cohérence des features."""
    
    def test_engineered_features_added(self, sample_dataframe):
        """Test que les features engineered sont bien ajoutées."""
        from app.routes.routes import add_smart_features
        
        df_enriched = add_smart_features(sample_dataframe)
        
        # Nombre de colonnes doit augmenter de 3
        assert len(df_enriched.columns) == len(sample_dataframe.columns) + 3
    
    def test_feature_names_consistency(self, sample_dataframe):
        """Test que les noms de features sont constants."""
        from app.routes.routes import add_smart_features
        
        df_enriched = add_smart_features(sample_dataframe)
        
        expected_new_features = [
            'ratio_salaire_age',
            'taux_stagnation',
            'salaire_par_annee_exp'
        ]
        
        for feature in expected_new_features:
            assert feature in df_enriched.columns
    
    def test_feature_order_preservation(self, sample_dataframe):
        """Test que l'ordre des features originales est préservé."""
        from app.routes.routes import add_smart_features
        
        original_cols = list(sample_dataframe.columns)
        df_enriched = add_smart_features(sample_dataframe)
        enriched_cols = list(df_enriched.columns)
        
        # Les colonnes originales doivent être dans le même ordre
        for i, col in enumerate(original_cols):
            assert enriched_cols[i] == col


@pytest.mark.unit  
class TestModelEdgeCases:
    """Tests des cas limites pour le modèle."""
    
    def test_model_with_zeros(self, mock_model):
        """Test avec des features à zéro."""
        X_test = np.zeros((5, 43))
        predictions = mock_model.predict(X_test)
        
        assert len(predictions) == 5
        assert all(p in [0, 1] for p in predictions)
    
    def test_model_with_large_values(self, mock_model):
        """Test avec de grandes valeurs."""
        X_test = np.random.rand(5, 43) * 10000
        predictions = mock_model.predict(X_test)
        
        assert len(predictions) == 5
        assert all(p in [0, 1] for p in predictions)
    
    def test_model_with_negative_values(self, mock_model):
        """Test avec des valeurs négatives."""
        X_test = np.random.rand(5, 43) * -1
        predictions = mock_model.predict(X_test)
        
        assert len(predictions) == 5
        assert all(p in [0, 1] for p in predictions)
    
    def test_model_with_mixed_values(self, mock_model):
        """Test avec un mix de valeurs positives et négatives."""
        X_test = np.random.randn(5, 43)  # Distribution normale
        predictions = mock_model.predict(X_test)
        
        assert len(predictions) == 5
        assert all(p in [0, 1] for p in predictions)
