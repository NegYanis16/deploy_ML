"""
Tests unitaires pour la validation des schémas Pydantic.
"""
import pytest
from pydantic import ValidationError
from app.schemas.request import PredictRequest, EmployeeInputSchema
from app.schemas.response import PredictResponse, BatchPredictResponse


@pytest.mark.unit
class TestPredictRequestValidation:
    """Tests pour le schéma PredictRequest."""
    
    def test_valid_predict_request(self):
        """Test avec des données valides."""
        data = {
            'feature_1': 5.1,
            'feature_2': 3.5,
            'feature_3': 1.4,
            'feature_4': 0.2
        }
        request = PredictRequest(**data)
        assert request.feature_1 == 5.1
        assert request.feature_2 == 3.5
        assert request.feature_3 == 1.4
        assert request.feature_4 == 0.2
    
    def test_missing_field(self):
        """Test avec un champ manquant."""
        data = {
            'feature_1': 5.1,
            'feature_2': 3.5,
            'feature_3': 1.4
            # feature_4 manquant
        }
        with pytest.raises(ValidationError) as exc_info:
            PredictRequest(**data)
        assert 'feature_4' in str(exc_info.value)


@pytest.mark.unit
class TestEmployeeInputSchemaValidation:
    """Tests pour le schéma EmployeeInputSchema."""
    
    def test_valid_employee_data(self, sample_employee_data):
        """Test avec des données employé valides."""
        # Normaliser les noms de colonnes
        normalized = {
            k.replace(' ', '_').replace('&', '').replace('é', 'e').replace('(', '').replace(')', ''): v 
            for k, v in sample_employee_data.items()
        }
        employee = EmployeeInputSchema(**normalized)
        assert employee.age == 35
        assert employee.genre == 1
        assert employee.revenu_mensuel == 5000.0
    
    def test_age_too_young(self):
        """Test avec un âge trop jeune."""
        data = {
            'age': 17,  # < 18
            'genre': 1,
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'age' for e in errors)
    
    def test_age_too_old(self):
        """Test avec un âge trop élevé."""
        data = {
            'age': 71,  # > 70
            'genre': 1,
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'age' for e in errors)
    
    def test_negative_revenue(self):
        """Test avec un revenu négatif."""
        data = {
            'age': 30,
            'genre': 1,
            'revenu_mensuel': -1000.0,  # Invalide
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'revenu_mensuel' for e in errors)
    
    def test_invalid_genre(self):
        """Test avec un genre invalide."""
        data = {
            'age': 30,
            'genre': 5,  # Doit être 0 ou 1
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'genre' for e in errors)
    
    def test_satisfaction_out_of_range_high(self):
        """Test avec une satisfaction trop élevée."""
        data = {
            'age': 30,
            'genre': 1,
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 10,  # Max 5
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any('satisfaction_employee_environnement' in str(e['loc']) for e in errors)
    
    def test_satisfaction_out_of_range_low(self):
        """Test avec une satisfaction trop basse."""
        data = {
            'age': 30,
            'genre': 1,
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': 0,
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 0,  # Min 1
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any('satisfaction_employee_nature_travail' in str(e['loc']) for e in errors)
    
    def test_negative_experience(self):
        """Test avec une expérience négative."""
        data = {
            'age': 30,
            'genre': 1,
            'revenu_mensuel': 3000.0,
            'nombre_experiences_precedentes': -1,  # Invalide
            'annee_experience_totale': 0,
            'annees_dans_l_entreprise': 0,
            'annees_dans_le_poste_actuel': 0,
            'annees_depuis_la_derniere_promotion': 0,
            'annes_sous_responsable_actuel': 0,
            'satisfaction_employee_environnement': 3,
            'satisfaction_employee_nature_travail': 3,
            'satisfaction_employee_equipe': 3,
            'satisfaction_employee_equilibre_pro_perso': 3,
            'note_evaluation_precedente': 3,
            'note_evaluation_actuelle': 3,
            'heure_supplementaires': 0,
            'augementation_salaire_precedente': 0.0,
            'nombre_participation_pee': 0,
            'nb_formations_suivies': 0,
            'distance_domicile_travail': 0,
            'niveau_education': 3,
            'ayant_enfants': 0,
            'frequence_deplacement': 0.0
        }
        with pytest.raises(ValidationError) as exc_info:
            EmployeeInputSchema(**data)
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'nombre_experiences_precedentes' for e in errors)


@pytest.mark.unit
class TestResponseSchemas:
    """Tests pour les schémas de réponse."""
    
    def test_predict_response(self):
        """Test du schéma PredictResponse."""
        response = PredictResponse(prediction=1)
        assert response.prediction == 1
    
    def test_batch_predict_response(self):
        """Test du schéma BatchPredictResponse."""
        predictions = [
            {"employee_index": 0, "employee_id": 1, "prediction": 1, "probability": 0.75, "risk_level": "High"},
            {"employee_index": 1, "employee_id": 2, "prediction": 0, "probability": 0.25, "risk_level": "Low"}
        ]
        response = BatchPredictResponse(total_employees=2, predictions=predictions)
        assert response.total_employees == 2
        assert len(response.predictions) == 2
