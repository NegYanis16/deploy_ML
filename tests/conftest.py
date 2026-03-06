"""
Fixtures globales pour les tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from app.main import app
from app.core.database import Base, get_db


# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Crée une base de données de test en mémoire pour chaque test."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()  # Fermer proprement toutes les connexions


@pytest.fixture(scope="function")
def client(test_db):
    """Client de test FastAPI avec database override."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # La session est gérée par la fixture test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def mock_model():
    """Mock d'un modèle ML pour les tests."""
    # Créer un vrai modèle simple pour les tests
    model = RandomForestClassifier(n_estimators=10, random_state=42, max_depth=3)
    
    # Entraîner sur des données fictives avec 43 features (40 base + 3 engineered)
    X_train = np.random.rand(100, 43)
    y_train = np.random.randint(0, 2, 100)
    model.fit(X_train, y_train)
    
    return model


@pytest.fixture(scope="function")
def app_with_model(mock_model):
    """App FastAPI avec un modèle chargé."""
    app.state.model = mock_model
    yield app
    app.state.model = None


@pytest.fixture
def sample_employee_data():
    """Données d'un employé valide pour les tests."""
    return {
        'age': 35,
        'genre': 1,
        'revenu_mensuel': 5000.0,
        'nombre_experiences_precedentes': 3,
        'annee_experience_totale': 10,
        'annees_dans_l_entreprise': 5,
        'annees_dans_le_poste_actuel': 2,
        'satisfaction_employee_environnement': 4,
        'note_evaluation_precedente': 3,
        'satisfaction_employee_nature_travail': 4,
        'satisfaction_employee_equipe': 5,
        'satisfaction_employee_equilibre_pro_perso': 3,
        'note_evaluation_actuelle': 4,
        'heure_supplementaires': 1,
        'augementation_salaire_precedente': 0.15,
        'nombre_participation_pee': 2,
        'nb_formations_suivies': 3,
        'distance_domicile_travail': 10,
        'niveau_education': 4,
        'ayant_enfants': 1,
        'frequence_deplacement': 2.0,
        'annees_depuis_la_derniere_promotion': 1,
        'annes_sous_responsable_actuel': 3,
        'departement_Consulting': 1,
        'departement_Ressources_Humaines': 0,
        'poste_Cadre Commercial': 0,
        'poste_Consultant': 1,
        'poste_Directeur Technique': 0,
        'poste_Manager': 0,
        'poste_Représentant Commercial': 0,
        'poste_Ressources Humaines': 0,
        'poste_Senior Manager': 0,
        'poste_Tech Lead': 0,
        'domaine_etude_Entrepreunariat': 0,
        'domaine_etude_Infra & Cloud': 1,
        'domaine_etude_Marketing': 0,
        'domaine_etude_Ressources Humaines': 0,
        'domaine_etude_Transformation Digitale': 0,
        'statut_marital_Divorcé(e)': 0,
        'statut_marital_Marié(e)': 1
    }


@pytest.fixture
def sample_dataframe(sample_employee_data):
    """DataFrame pandas avec des données de test."""
    return pd.DataFrame([sample_employee_data])


@pytest.fixture
def invalid_employee_data():
    """Données d'employé invalides pour tester la validation."""
    return {
        'age': -5,  # Invalide: âge négatif
        'genre': 2,  # Invalide: doit être 0 ou 1
        'revenu_mensuel': -1000.0,  # Invalide: négatif
        'satisfaction_employee_environnement': 10,  # Invalide: max 5
    }


@pytest.fixture
def csv_content_valid():
    """Contenu CSV valide pour les tests."""
    return """age,genre,revenu_mensuel,nombre_experiences_precedentes,annee_experience_totale,annees_dans_l_entreprise,annees_dans_le_poste_actuel,satisfaction_employee_environnement,note_evaluation_precedente,satisfaction_employee_nature_travail,satisfaction_employee_equipe,satisfaction_employee_equilibre_pro_perso,note_evaluation_actuelle,heure_supplementaires,augementation_salaire_precedente,nombre_participation_pee,nb_formations_suivies,distance_domicile_travail,niveau_education,ayant_enfants,frequence_deplacement,annees_depuis_la_derniere_promotion,annes_sous_responsable_actuel,departement_Consulting,departement_Ressources_Humaines,poste_Cadre Commercial,poste_Consultant,poste_Directeur Technique,poste_Manager,poste_Représentant Commercial,poste_Ressources Humaines,poste_Senior Manager,poste_Tech Lead,domaine_etude_Entrepreunariat,domaine_etude_Infra & Cloud,domaine_etude_Marketing,domaine_etude_Ressources Humaines,domaine_etude_Transformation Digitale,statut_marital_Divorcé(e),statut_marital_Marié(e)
35,1,5000.0,3,10,5,2,4,3,4,5,3,4,1,0.15,2,3,10,4,1,2.0,1,3,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1
28,0,3500.0,1,5,2,1,3,3,3,4,4,3,0,0.10,1,2,5,3,0,1.0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0"""


@pytest.fixture
def csv_content_invalid():
    """Contenu CSV invalide pour tester la validation."""
    return """age,genre,revenu_mensuel
-5,2,-1000.0
150,1,5000.0"""
