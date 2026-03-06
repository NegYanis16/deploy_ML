from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.core.database import Base


class EmployeeData(Base):
    """
    Table pour stocker les données des employés (inputs).
    """
    __tablename__ = "employee_data"
    
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    genre = Column(Integer)
    revenu_mensuel = Column(Float)
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Integer)
    heure_supplementaires = Column(Integer)
    augementation_salaire_precedente = Column(Float)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    ayant_enfants = Column(Integer)
    frequence_deplacement = Column(Float)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    
    # Colonnes one-hot encoded stockées en JSON ou Text
    departement = Column(String(100))
    poste = Column(String(100))
    domaine_etude = Column(String(100))
    statut_marital = Column(String(50))
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)