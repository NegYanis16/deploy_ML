"""
Tests unitaires pour les fonctions helper (extraction de données).
"""
import pytest
from app.routes.routes import (
    _get_poste_from_row,
    _get_domaine_from_row,
    _get_statut_marital_from_row
)


@pytest.mark.unit
class TestPosteExtraction:
    """Tests pour l'extraction du poste depuis les colonnes one-hot."""
    
    def test_get_poste_consultant(self):
        """Test extraction du poste Consultant."""
        row = {'poste_Consultant': 1, 'poste_Manager': 0}
        assert _get_poste_from_row(row) == 'Consultant'
    
    def test_get_poste_manager(self):
        """Test extraction du poste Manager."""
        row = {'poste_Manager': 1, 'poste_Consultant': 0}
        assert _get_poste_from_row(row) == 'Manager'
    
    def test_get_poste_cadre_commercial(self):
        """Test extraction du poste Cadre Commercial."""
        row = {'poste_Cadre Commercial': 1}
        assert _get_poste_from_row(row) == 'Cadre Commercial'
    
    def test_get_poste_directeur_technique(self):
        """Test extraction du poste Directeur Technique."""
        row = {'poste_Directeur Technique': 1}
        assert _get_poste_from_row(row) == 'Directeur Technique'
    
    def test_get_poste_representant_commercial(self):
        """Test extraction du poste Représentant Commercial."""
        row = {'poste_Représentant Commercial': 1}
        assert _get_poste_from_row(row) == 'Représentant Commercial'
    
    def test_get_poste_ressources_humaines(self):
        """Test extraction du poste Ressources Humaines."""
        row = {'poste_Ressources Humaines': 1}
        assert _get_poste_from_row(row) == 'Ressources Humaines'
    
    def test_get_poste_senior_manager(self):
        """Test extraction du poste Senior Manager."""
        row = {'poste_Senior Manager': 1}
        assert _get_poste_from_row(row) == 'Senior Manager'
    
    def test_get_poste_tech_lead(self):
        """Test extraction du poste Tech Lead."""
        row = {'poste_Tech Lead': 1}
        assert _get_poste_from_row(row) == 'Tech Lead'
    
    def test_get_poste_not_specified(self):
        """Test quand aucun poste n'est spécifié."""
        row = {'poste_Manager': 0, 'poste_Consultant': 0}
        assert _get_poste_from_row(row) == 'Non spécifié'
    
    def test_get_poste_empty_row(self):
        """Test avec une row vide."""
        row = {}
        assert _get_poste_from_row(row) == 'Non spécifié'
    
    def test_get_poste_first_match_priority(self):
        """Test que le premier match est retourné (cas anormal)."""
        # Dans un cas normal, un seul poste devrait être à 1
        row = {
            'poste_Cadre Commercial': 1,
            'poste_Consultant': 1  # Anormal mais on teste le comportement
        }
        # Devrait retourner le premier trouvé dans l'ordre du dict
        result = _get_poste_from_row(row)
        assert result in ['Cadre Commercial', 'Consultant']


@pytest.mark.unit
class TestDomaineExtraction:
    """Tests pour l'extraction du domaine d'étude."""
    
    def test_get_domaine_entrepreunariat(self):
        """Test extraction Entrepreunariat."""
        row = {'domaine_etude_Entrepreunariat': 1}
        assert _get_domaine_from_row(row) == 'Entrepreunariat'
    
    def test_get_domaine_infra_cloud(self):
        """Test extraction Infra & Cloud."""
        row = {'domaine_etude_Infra & Cloud': 1}
        assert _get_domaine_from_row(row) == 'Infra & Cloud'
    
    def test_get_domaine_marketing(self):
        """Test extraction Marketing."""
        row = {'domaine_etude_Marketing': 1}
        assert _get_domaine_from_row(row) == 'Marketing'
    
    def test_get_domaine_ressources_humaines(self):
        """Test extraction Ressources Humaines."""
        row = {'domaine_etude_Ressources Humaines': 1}
        assert _get_domaine_from_row(row) == 'Ressources Humaines'
    
    def test_get_domaine_transformation_digitale(self):
        """Test extraction Transformation Digitale."""
        row = {'domaine_etude_Transformation Digitale': 1}
        assert _get_domaine_from_row(row) == 'Transformation Digitale'
    
    def test_get_domaine_not_specified(self):
        """Test quand aucun domaine n'est spécifié."""
        row = {'domaine_etude_Marketing': 0}
        assert _get_domaine_from_row(row) == 'Non spécifié'
    
    def test_get_domaine_empty_row(self):
        """Test avec une row vide."""
        row = {}
        assert _get_domaine_from_row(row) == 'Non spécifié'


@pytest.mark.unit
class TestStatutMaritalExtraction:
    """Tests pour l'extraction du statut marital."""
    
    def test_get_statut_divorce(self):
        """Test extraction Divorcé(e)."""
        row = {'statut_marital_Divorcé(e)': 1, 'statut_marital_Marié(e)': 0}
        assert _get_statut_marital_from_row(row) == 'Divorcé(e)'
    
    def test_get_statut_marie(self):
        """Test extraction Marié(e)."""
        row = {'statut_marital_Divorcé(e)': 0, 'statut_marital_Marié(e)': 1}
        assert _get_statut_marital_from_row(row) == 'Marié(e)'
    
    def test_get_statut_celibataire_default(self):
        """Test extraction Célibataire (par défaut)."""
        row = {'statut_marital_Divorcé(e)': 0, 'statut_marital_Marié(e)': 0}
        assert _get_statut_marital_from_row(row) == 'Célibataire'
    
    def test_get_statut_celibataire_empty_row(self):
        """Test avec une row vide (défaut Célibataire)."""
        row = {}
        assert _get_statut_marital_from_row(row) == 'Célibataire'
    
    def test_get_statut_divorce_priority(self):
        """Test que Divorcé a priorité sur Marié si les deux sont à 1 (cas anormal)."""
        row = {'statut_marital_Divorcé(e)': 1, 'statut_marital_Marié(e)': 1}
        assert _get_statut_marital_from_row(row) == 'Divorcé(e)'
    
    def test_get_statut_with_none_values(self):
        """Test avec des valeurs None."""
        row = {'statut_marital_Divorcé(e)': None, 'statut_marital_Marié(e)': None}
        assert _get_statut_marital_from_row(row) == 'Célibataire'
    
    def test_get_statut_with_zero_values(self):
        """Test avec des valeurs 0 explicites."""
        row = {'statut_marital_Divorcé(e)': 0, 'statut_marital_Marié(e)': 0}
        assert _get_statut_marital_from_row(row) == 'Célibataire'


@pytest.mark.unit
class TestHelpersFunctionsIntegration:
    """Tests d'intégration des fonctions helper."""
    
    def test_all_helpers_with_complete_row(self, sample_employee_data):
        """Test toutes les fonctions helper avec des données complètes."""
        poste = _get_poste_from_row(sample_employee_data)
        domaine = _get_domaine_from_row(sample_employee_data)
        statut = _get_statut_marital_from_row(sample_employee_data)
        
        # Vérifier que les valeurs sont valides
        assert poste in ['Consultant', 'Manager', 'Cadre Commercial', 
                        'Directeur Technique', 'Représentant Commercial',
                        'Ressources Humaines', 'Senior Manager', 'Tech Lead', 
                        'Non spécifié']
        assert domaine in ['Entrepreunariat', 'Infra & Cloud', 'Marketing',
                          'Ressources Humaines', 'Transformation Digitale',
                          'Non spécifié']
        assert statut in ['Divorcé(e)', 'Marié(e)', 'Célibataire']
    
    def test_helpers_with_minimal_data(self):
        """Test les helpers avec un minimum de données."""
        row = {
            'age': 30,
            'revenu_mensuel': 3000
        }
        
        # Ne doit pas planter
        poste = _get_poste_from_row(row)
        domaine = _get_domaine_from_row(row)
        statut = _get_statut_marital_from_row(row)
        
        assert poste == 'Non spécifié'
        assert domaine == 'Non spécifié'
        assert statut == 'Célibataire'
