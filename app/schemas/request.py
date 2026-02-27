from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class PredictRequest(BaseModel):
    """Schéma pour une prédiction individuelle (legacy)"""
    feature_1: float = Field(..., description="Premiere caracteristique")
    feature_2: float = Field(..., description="Deuxieme caracteristique")
    feature_3: float = Field(..., description="Troisieme caracteristique")
    feature_4: float = Field(..., description="Quatrieme caracteristique")

    model_config = {
        "json_schema_extra": {
            "example": {
                "feature_1": 5.1,
                "feature_2": 3.5,
                "feature_3": 1.4,
                "feature_4": 0.2
            }
        }
    }

class EmployeeInputSchema(BaseModel):
    """Schéma de validation pour les données d'un employé depuis le CSV"""
    # Données démographiques
    age: int = Field(..., ge=18, le=70, description="Âge de l'employé")
    genre: int = Field(..., ge=0, le=1, description="Genre (0=Femme, 1=Homme)")
    ayant_enfants: int = Field(..., ge=0, le=1)
    
    # Données professionnelles
    revenu_mensuel: float = Field(..., gt=0)
    nombre_experiences_precedentes: int = Field(..., ge=0)
    annee_experience_totale: int = Field(..., ge=0)
    annees_dans_l_entreprise: int = Field(..., ge=0)
    annees_dans_le_poste_actuel: int = Field(..., ge=0)
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0)
    annes_sous_responsable_actuel: int = Field(..., ge=0)
    
    # Satisfaction et évaluation (échelles 1-5 généralement)
    satisfaction_employee_environnement: int = Field(..., ge=1, le=5)
    satisfaction_employee_nature_travail: int = Field(..., ge=1, le=5)
    satisfaction_employee_equipe: int = Field(..., ge=1, le=5)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=1, le=5)
    note_evaluation_precedente: int = Field(..., ge=1, le=5)
    note_evaluation_actuelle: int = Field(..., ge=1, le=5)
    
    # Autres informations
    heure_supplementaires: int = Field(..., ge=0, le=1)
    augementation_salaire_precedente: float = Field(..., ge=0, le=1)
    nombre_participation_pee: int = Field(..., ge=0)
    nb_formations_suivies: int = Field(..., ge=0)
    distance_domicile_travail: int = Field(..., ge=0)
    niveau_education: int = Field(..., ge=1, le=5)
    frequence_deplacement: float = Field(..., ge=0)
    
    # Colonnes one-hot encodées (toutes doivent être 0 ou 1)
    departement_Consulting: Optional[int] = Field(0, ge=0, le=1)
    departement_Ressources_Humaines: Optional[int] = Field(0, ge=0, le=1)
    
    poste_Cadre_Commercial: Optional[int] = Field(0, ge=0, le=1)
    poste_Consultant: Optional[int] = Field(0, ge=0, le=1)
    poste_Directeur_Technique: Optional[int] = Field(0, ge=0, le=1)
    poste_Manager: Optional[int] = Field(0, ge=0, le=1)
    poste_Représentant_Commercial: Optional[int] = Field(0, ge=0, le=1)
    poste_Ressources_Humaines: Optional[int] = Field(0, ge=0, le=1)
    poste_Senior_Manager: Optional[int] = Field(0, ge=0, le=1)
    poste_Tech_Lead: Optional[int] = Field(0, ge=0, le=1)
    
    domaine_etude_Entrepreunariat: Optional[int] = Field(0, ge=0, le=1)
    domaine_etude_Infra_Cloud: Optional[int] = Field(0, ge=0, le=1)
    domaine_etude_Marketing: Optional[int] = Field(0, ge=0, le=1)
    domaine_etude_Ressources_Humaines: Optional[int] = Field(0, ge=0, le=1)
    domaine_etude_Transformation_Digitale: Optional[int] = Field(0, ge=0, le=1)
    
    statut_marital_Divorcé: Optional[int] = Field(0, ge=0, le=1)
    statut_marital_Marié: Optional[int] = Field(0, ge=0, le=1)
    
    class Config:
        str_strip_whitespace = True

class EmployeePrediction(BaseModel):
    """Résultat de prédiction pour un employé"""
    employee_index: int
    prediction: int
    probability: float