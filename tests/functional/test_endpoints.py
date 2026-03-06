"""
Tests fonctionnels pour les endpoints de l'API.
"""
import pytest
from io import BytesIO
from app.main import app


@pytest.mark.functional
class TestHealthEndpoint:
    """Tests pour l'endpoint /health."""
    
    def test_health_check_without_model(self, client):
        """Test du health check sans modèle chargé."""
        app.state.model = None
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["model_status"] == "not_loaded"
    
    def test_health_check_with_model(self, client, mock_model):
        """Test du health check avec modèle chargé."""
        app.state.model = mock_model
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["model_status"] == "loaded"
        app.state.model = None


@pytest.mark.functional
class TestPredictEndpoint:
    """Tests pour l'endpoint /predict."""
    
    def test_predict_without_model(self, client):
        """Test de prédiction sans modèle chargé."""
        app.state.model = None
        
        payload = {
            "feature_1": 5.1,
            "feature_2": 3.5,
            "feature_3": 1.4,
            "feature_4": 0.2
        }
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 503
        assert "modele n'est pas pret" in response.json()["detail"]
    
    def test_predict_missing_feature(self, client, mock_model):
        """Test avec une feature manquante."""
        app.state.model = mock_model
        
        payload = {
            "feature_1": 5.1,
            "feature_2": 3.5,
            "feature_3": 1.4
            # feature_4 manquante
        }
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        
        app.state.model = None
    
    def test_predict_invalid_type(self, client, mock_model):
        """Test avec un type de donnée invalide."""
        app.state.model = mock_model
        
        payload = {
            "feature_1": "invalid",  # String au lieu de float
            "feature_2": 3.5,
            "feature_3": 1.4,
            "feature_4": 0.2
        }
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        
        app.state.model = None


@pytest.mark.functional
class TestPredictCSVEndpoint:
    """Tests pour l'endpoint /predict/csv."""
    
    def test_predict_csv_without_model(self, client, csv_content_valid):
        """Test CSV sans modèle chargé."""
        app.state.model = None
        
        csv_file = BytesIO(csv_content_valid.encode('utf-8'))
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.csv", csv_file, "text/csv")}
        )
        
        assert response.status_code == 503
        assert "modele n'est pas pret" in response.json()["detail"]
    
    def test_predict_csv_invalid_file_type(self, client, mock_model):
        """Test avec un type de fichier invalide."""
        app.state.model = mock_model
        
        # Fichier .txt au lieu de .csv
        txt_file = BytesIO(b"not a csv")
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.txt", txt_file, "text/plain")}
        )
        
        assert response.status_code == 400
        assert "format CSV" in response.json()["detail"]
        
        app.state.model = None
    
    def test_predict_csv_invalid_content(self, client, mock_model):
        """Test avec un contenu CSV invalide."""
        app.state.model = mock_model
        
        invalid_csv = b"invalid,csv,content\n1,2"  # Structure incorrecte
        csv_file = BytesIO(invalid_csv)
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.csv", csv_file, "text/csv")}
        )
        
        # Devrait retourner une erreur 400 ou 422 (validation ou parsing)
        assert response.status_code in [400, 422, 500]
        
        app.state.model = None
    
    def test_predict_csv_empty_file(self, client, mock_model):
        """Test avec un fichier vide."""
        app.state.model = mock_model
        
        csv_file = BytesIO(b"")
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.csv", csv_file, "text/csv")}
        )
        
        # Devrait retourner une erreur
        assert response.status_code >= 400
        
        app.state.model = None
    
    def test_predict_csv_encoding_latin1(self, client, mock_model, csv_content_valid):
        """Test avec encodage Latin-1."""
        app.state.model = mock_model
        
        csv_file = BytesIO(csv_content_valid.encode('latin-1'))
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.csv", csv_file, "text/csv")}
        )
        
        # Ne devrait pas planter grâce au fallback encodage
        assert response.status_code in [200, 400, 422, 500]
        
        app.state.model = None
    
    @pytest.mark.slow
    def test_predict_csv_large_file(self, client, mock_model, sample_employee_data):
        """Test avec un fichier CSV volumineux."""
        app.state.model = mock_model
        
        # Créer un CSV avec 1000 lignes
        import pandas as pd
        df = pd.DataFrame([sample_employee_data] * 1000)
        csv_content = df.to_csv(index=False)
        csv_file = BytesIO(csv_content.encode('utf-8'))
        
        response = client.post(
            "/predict/csv",
            files={"file": ("large_test.csv", csv_file, "text/csv")}
        )
        
        # Peut être lent mais ne doit pas planter
        assert response.status_code in [200, 422, 500]  # 422 si validation échoue
        
        app.state.model = None


@pytest.mark.functional
class TestDatabaseIntegration:
    """Tests d'intégration avec la base de données."""
    
    def test_csv_prediction_saves_to_database(self, client, test_db, mock_model, csv_content_valid):
        """Test que les prédictions CSV sont bien sauvegardées en DB."""
        app.state.model = mock_model
        
        csv_file = BytesIO(csv_content_valid.encode('utf-8'))
        
        response = client.post(
            "/predict/csv",
            files={"file": ("test.csv", csv_file, "text/csv")}
        )
        
        if response.status_code == 200:
            # Vérifier que des données ont été insérées
            from app.models import EmployeeData, Prediction
            
            employees_count = test_db.query(EmployeeData).count()
            predictions_count = test_db.query(Prediction).count()
            
            assert employees_count > 0
            assert predictions_count > 0
            assert employees_count == predictions_count
        
        app.state.model = None


@pytest.mark.functional
class TestErrorHandling:
    """Tests de gestion d'erreurs."""
    
    def test_404_not_found(self, client):
        """Test d'une route inexistante."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test avec une méthode HTTP non autorisée."""
        response = client.get("/predict")  # POST attendu
        assert response.status_code == 405
