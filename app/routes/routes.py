from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Depends
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime
from sqlalchemy.orm import Session
import uuid
from pydantic import ValidationError

from app.schemas.request import PredictRequest, EmployeeInputSchema
from app.schemas.response import PredictResponse, BatchPredictResponse
from app.config import logger
from app.core.database import get_db
from app.models import EmployeeData, Prediction

router = APIRouter()

def add_smart_features(df):
    """
    Ajoute les features calculées au DataFrame.
    """
    df_new = df.copy()
    
    # Ratio Salaire / Age
    df_new['ratio_salaire_age'] = df_new['revenu_mensuel'] / df_new['age']
    
    # Taux de stagnation
    df_new['taux_stagnation'] = df_new['annees_dans_le_poste_actuel'] / (df_new['annees_dans_l_entreprise'] + 1)
    
    # Salaire par année d'expérience
    df_new['salaire_par_annee_exp'] = df_new['revenu_mensuel'] / (df_new['annee_experience_totale'] + 1)
    
    return df_new

@router.get("/health", tags=["System"])
async def health_check(request: Request):
    model_status = "loaded" if request.app.state.model else "not_loaded"
    return {"status": "ok", "model_status": model_status}

@router.post("/predict", response_model=PredictResponse, tags=["ML"])
async def predict(data: PredictRequest, request: Request):
    """Endpoint legacy pour prédiction individuelle."""
    model = request.app.state.model
    if not model:
        raise HTTPException(status_code=503, detail="Le modele n'est pas pret.")

    try:
        input_array = [[
            data.feature_1,
            data.feature_2,
            data.feature_3,
            data.feature_4
        ]]
        prediction = model.predict(input_array)[0]
        return PredictResponse(prediction=int(prediction))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/csv", response_model=BatchPredictResponse, tags=["ML"])
async def predict_csv(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Prédiction batch à partir d'un fichier CSV.
    Sauvegarde les inputs et les prédictions dans la base de données.
    """
    model = request.app.state.model
    if not model:
        raise HTTPException(status_code=503, detail="Le modele n'est pas pret.")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV")
    
    try:
        # Lecture du fichier CSV avec l'encodage approprié
        contents = await file.read()
        
        # Essayer plusieurs encodages
        try:
            csv_data = StringIO(contents.decode('utf-8'))
        except UnicodeDecodeError:
            csv_data = StringIO(contents.decode('latin-1'))
        
        df = pd.read_csv(csv_data)
        
        logger.info(f"CSV reçu avec {len(df)} lignes et {len(df.columns)} colonnes")
        
        # Correction des noms de colonnes (problèmes d'encodage)
        column_mapping = {
            'poste_ReprÃ©sentant Commercial': 'poste_Représentant Commercial',
            'statut_marital_DivorcÃ©(e)': 'statut_marital_Divorcé(e)',
            'statut_marital_MariÃ©(e)': 'statut_marital_Marié(e)'
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Appliquer le feature engineering
        df_enriched = add_smart_features(df)
        
        # Prédictions
        predictions = model.predict(df_enriched)
        probabilities = model.predict_proba(df_enriched)[:, 1]
        
        # Générer un batch_id unique pour ce groupe de prédictions
        batch_id = f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Sauvegarder dans la base de données
        results = []
        validation_errors = []
        
        for idx, (row, pred, proba) in enumerate(zip(df.to_dict('records'), predictions, probabilities)):
            try:
                # Validation Pydantic de la ligne
                # Normaliser les noms de colonnes pour Pydantic (remplacer espaces par _)
                normalized_row = {
                    k.replace(' ', '_').replace('&', '').replace('é', 'e').replace('(', '').replace(')', ''): v 
                    for k, v in row.items()
                }
                
                # Valider avec Pydantic
                validated_data = EmployeeInputSchema(**normalized_row)
                
                # 1. Sauvegarder les données de l'employé (input)
                employee = EmployeeData(
                    age=validated_data.age,
                    genre=validated_data.genre,
                    revenu_mensuel=validated_data.revenu_mensuel,
                    nombre_experiences_precedentes=validated_data.nombre_experiences_precedentes,
                    annee_experience_totale=validated_data.annee_experience_totale,
                    annees_dans_l_entreprise=validated_data.annees_dans_l_entreprise,
                    annees_dans_le_poste_actuel=validated_data.annees_dans_le_poste_actuel,
                    satisfaction_employee_environnement=validated_data.satisfaction_employee_environnement,
                    note_evaluation_precedente=validated_data.note_evaluation_precedente,
                    satisfaction_employee_nature_travail=validated_data.satisfaction_employee_nature_travail,
                    satisfaction_employee_equipe=validated_data.satisfaction_employee_equipe,
                    satisfaction_employee_equilibre_pro_perso=validated_data.satisfaction_employee_equilibre_pro_perso,
                    note_evaluation_actuelle=validated_data.note_evaluation_actuelle,
                    heure_supplementaires=validated_data.heure_supplementaires,
                    augementation_salaire_precedente=validated_data.augementation_salaire_precedente,
                    nombre_participation_pee=validated_data.nombre_participation_pee,
                    nb_formations_suivies=validated_data.nb_formations_suivies,
                    distance_domicile_travail=validated_data.distance_domicile_travail,
                    niveau_education=validated_data.niveau_education,
                    ayant_enfants=validated_data.ayant_enfants,
                    frequence_deplacement=validated_data.frequence_deplacement,
                    annees_depuis_la_derniere_promotion=validated_data.annees_depuis_la_derniere_promotion,
                    annes_sous_responsable_actuel=validated_data.annes_sous_responsable_actuel,
                    departement="Consulting" if row.get('departement_Consulting') == 1 else "Ressources Humaines",
                    poste=_get_poste_from_row(row),
                    domaine_etude=_get_domaine_from_row(row),
                    statut_marital=_get_statut_marital_from_row(row)
                )
                db.add(employee)
                db.flush()
                
                # 2. Sauvegarder la prédiction (output)
                risk_level = "High" if proba > 0.35 else "Low"
                prediction_record = Prediction(
                    employee_id=employee.id,
                    prediction=int(pred),
                    probability=float(proba),
                    risk_level=risk_level,
                    batch_id=batch_id
                )
                db.add(prediction_record)
                
                results.append({
                    "employee_index": idx,
                    "employee_id": employee.id,
                    "prediction": int(pred),
                    "probability": float(proba),
                    "risk_level": risk_level
                })
                
            except ValidationError as ve:
                validation_errors.append({
                    "employee_index": idx,
                    "errors": ve.errors()
                })
                logger.warning(f"Validation échouée pour l'employé {idx}: {ve.errors()}")
        
        # Si des erreurs de validation, on annule tout
        if validation_errors:
            db.rollback()
            logger.error(f"{len(validation_errors)} erreurs de validation détectées")
            raise HTTPException(
                status_code=422, 
                detail={
                    "message": f"{len(validation_errors)} lignes invalides détectées",
                    "errors": validation_errors
                }
            )
        
        # Commit toutes les données
        db.commit()
        
        logger.info(f"Prédictions effectuées et sauvegardées pour {len(results)} employés (batch_id: {batch_id})")
        
        return BatchPredictResponse(
            total_employees=len(results),
            predictions=results
        )
        
    except pd.errors.ParserError as e:
        logger.error(f"Erreur de parsing CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Fichier CSV invalide: {str(e)}")
    except KeyError as e:
        logger.error(f"Colonne manquante dans le CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Colonne manquante dans le CSV: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_poste_from_row(row):
    """Extrait le poste depuis les colonnes one-hot encodées."""
    postes = {
        'poste_Cadre Commercial': 'Cadre Commercial',
        'poste_Consultant': 'Consultant',
        'poste_Directeur Technique': 'Directeur Technique',
        'poste_Manager': 'Manager',
        'poste_Représentant Commercial': 'Représentant Commercial',
        'poste_Ressources Humaines': 'Ressources Humaines',
        'poste_Senior Manager': 'Senior Manager',
        'poste_Tech Lead': 'Tech Lead'
    }
    for col, poste in postes.items():
        if row.get(col) == 1:
            return poste
    return "Non spécifié"


def _get_domaine_from_row(row):
    """Extrait le domaine d'étude depuis les colonnes one-hot encodées."""
    domaines = {
        'domaine_etude_Entrepreunariat': 'Entrepreunariat',
        'domaine_etude_Infra & Cloud': 'Infra & Cloud',
        'domaine_etude_Marketing': 'Marketing',
        'domaine_etude_Ressources Humaines': 'Ressources Humaines',
        'domaine_etude_Transformation Digitale': 'Transformation Digitale'
    }
    for col, domaine in domaines.items():
        if row.get(col) == 1:
            return domaine
    return "Non spécifié"


def _get_statut_marital_from_row(row):
    """Extrait le statut marital depuis les colonnes one-hot encodées."""
    if row.get('statut_marital_Divorcé(e)') == 1:
        return 'Divorcé(e)'
    elif row.get('statut_marital_Marié(e)') == 1:
        return 'Marié(e)'
    return 'Célibataire'