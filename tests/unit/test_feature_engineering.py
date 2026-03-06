"""
Tests unitaires pour les fonctions de feature engineering.
"""
import pytest
import pandas as pd
import numpy as np
from app.routes.routes import add_smart_features


@pytest.mark.unit
class TestFeatureEngineering:
    """Tests pour la fonction add_smart_features"""
    
    def test_add_smart_features_basic(self, sample_dataframe):
        """Test que les features calculées sont bien ajoutées."""
        df_enriched = add_smart_features(sample_dataframe)
        
        # Vérifier que les colonnes sont ajoutées
        assert 'ratio_salaire_age' in df_enriched.columns
        assert 'taux_stagnation' in df_enriched.columns
        assert 'salaire_par_annee_exp' in df_enriched.columns
        
        # Vérifier que l'original n'est pas modifié
        assert 'ratio_salaire_age' not in sample_dataframe.columns
    
    def test_ratio_salaire_age_calculation(self):
        """Test le calcul du ratio salaire/âge."""
        df = pd.DataFrame({
            'age': [30, 40, 50],
            'revenu_mensuel': [3000, 4000, 5000],
            'annees_dans_le_poste_actuel': [1, 2, 3],
            'annees_dans_l_entreprise': [2, 3, 4],
            'annee_experience_totale': [5, 10, 15]
        })
        
        df_enriched = add_smart_features(df)
        
        expected_ratio = [3000/30, 4000/40, 5000/50]
        np.testing.assert_array_almost_equal(
            df_enriched['ratio_salaire_age'].values,
            expected_ratio
        )
    
    def test_taux_stagnation_calculation(self):
        """Test le calcul du taux de stagnation."""
        df = pd.DataFrame({
            'age': [30],
            'revenu_mensuel': [3000],
            'annees_dans_le_poste_actuel': [2],
            'annees_dans_l_entreprise': [5],
            'annee_experience_totale': [10]
        })
        
        df_enriched = add_smart_features(df)
        
        # Taux = annees_poste / (annees_entreprise + 1) = 2 / 6
        expected = 2 / (5 + 1)
        assert df_enriched['taux_stagnation'].iloc[0] == pytest.approx(expected)
    
    def test_salaire_par_annee_exp_calculation(self):
        """Test le calcul du salaire par année d'expérience."""
        df = pd.DataFrame({
            'age': [30],
            'revenu_mensuel': [6000],
            'annees_dans_le_poste_actuel': [2],
            'annees_dans_l_entreprise': [5],
            'annee_experience_totale': [11]
        })
        
        df_enriched = add_smart_features(df)
        
        # Salaire/exp = 6000 / (11 + 1) = 500
        expected = 6000 / (11 + 1)
        assert df_enriched['salaire_par_annee_exp'].iloc[0] == pytest.approx(expected)
    
    def test_division_by_zero_protection_stagnation(self):
        """Test la protection contre la division par zéro pour taux_stagnation."""
        df = pd.DataFrame({
            'age': [25],
            'revenu_mensuel': [3000],
            'annees_dans_le_poste_actuel': [0],
            'annees_dans_l_entreprise': [0],  # Devrait donner 0 / (0 + 1) = 0
            'annee_experience_totale': [0]
        })
        
        df_enriched = add_smart_features(df)
        
        # Ne doit pas planter et donner 0
        assert df_enriched['taux_stagnation'].iloc[0] == 0.0
    
    def test_division_by_zero_protection_salaire_exp(self):
        """Test la protection contre la division par zéro pour salaire_par_annee_exp."""
        df = pd.DataFrame({
            'age': [22],
            'revenu_mensuel': [2500],
            'annees_dans_le_poste_actuel': [0],
            'annees_dans_l_entreprise': [0],
            'annee_experience_totale': [0]  # Devrait donner 2500 / (0 + 1) = 2500
        })
        
        df_enriched = add_smart_features(df)
        
        # Ne doit pas planter
        assert df_enriched['salaire_par_annee_exp'].iloc[0] == 2500.0
    
    def test_multiple_rows(self):
        """Test avec plusieurs lignes."""
        df = pd.DataFrame({
            'age': [25, 30, 35, 40],
            'revenu_mensuel': [2500, 3500, 4500, 5500],
            'annees_dans_le_poste_actuel': [1, 2, 3, 4],
            'annees_dans_l_entreprise': [2, 4, 6, 8],
            'annee_experience_totale': [3, 6, 9, 12]
        })
        
        df_enriched = add_smart_features(df)
        
        # Vérifier que toutes les lignes ont les nouvelles features
        assert len(df_enriched) == 4
        assert not df_enriched['ratio_salaire_age'].isna().any()
        assert not df_enriched['taux_stagnation'].isna().any()
        assert not df_enriched['salaire_par_annee_exp'].isna().any()
    
    def test_original_columns_preserved(self, sample_dataframe):
        """Test que les colonnes originales sont préservées."""
        original_cols = set(sample_dataframe.columns)
        df_enriched = add_smart_features(sample_dataframe)
        
        # Toutes les colonnes originales doivent être présentes
        for col in original_cols:
            assert col in df_enriched.columns
    
    def test_feature_engineering_with_edge_values(self):
        """Test avec des valeurs extrêmes."""
        df = pd.DataFrame({
            'age': [18, 70],  # Min et max age
            'revenu_mensuel': [1500, 20000],
            'annees_dans_le_poste_actuel': [0, 30],
            'annees_dans_l_entreprise': [0, 40],
            'annee_experience_totale': [0, 50]
        })
        
        df_enriched = add_smart_features(df)
        
        # Vérifier qu'il n'y a pas de NaN ou Inf
        assert not df_enriched['ratio_salaire_age'].isna().any()
        assert not df_enriched['taux_stagnation'].isna().any()
        assert not df_enriched['salaire_par_annee_exp'].isna().any()
        assert np.isfinite(df_enriched['ratio_salaire_age']).all()
        assert np.isfinite(df_enriched['taux_stagnation']).all()
        assert np.isfinite(df_enriched['salaire_par_annee_exp']).all()
