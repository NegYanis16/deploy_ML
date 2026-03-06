# Tests - Documentation

## Structure des tests

```
tests/
├── __init__.py
├── conftest.py              # Fixtures globales
├── unit/                    # Tests unitaires
│   ├── __init__.py
│   ├── test_feature_engineering.py
│   ├── test_helpers.py
│   ├── test_validation.py
│   └── test_model.py
└── functional/              # Tests fonctionnels/intégration
    ├── __init__.py
    └── test_endpoints.py
```

## Installation des dépendances de test

```powershell
pip install -r requirements.txt
```

## Exécution des tests

### Tous les tests
```powershell
pytest
```

### Tests unitaires uniquement
```powershell
pytest -m unit
```

### Tests fonctionnels uniquement
```powershell
pytest -m functional
```

### Tests avec rapport de couverture
```powershell
pytest --cov=app --cov-report=html
```

Le rapport HTML sera généré dans `htmlcov/index.html`

### Tests avec rapport détaillé
```powershell
pytest -v
```

### Tests spécifiques
```powershell
# Un fichier de test
pytest tests/unit/test_feature_engineering.py

# Une classe de test
pytest tests/unit/test_feature_engineering.py::TestFeatureEngineering

# Un test spécifique
pytest tests/unit/test_feature_engineering.py::TestFeatureEngineering::test_add_smart_features_basic
```

### Exclure les tests lents
```powershell
pytest -m "not slow"
```

### Mode verbeux avec détails des échecs
```powershell
pytest -vv --tb=short
```

## Couverture de test attendue

L'objectif de couverture est fixé à **70%** minimum (voir `pytest.ini`).

### Zones couvertes

#### Tests Unitaires (`tests/unit/`)

1. **Feature Engineering** (`test_feature_engineering.py`)
   - ✅ Calcul du `ratio_salaire_age`
   - ✅ Calcul du `taux_stagnation`
   - ✅ Calcul du `salaire_par_annee_exp`
   - ✅ Protection division par zéro
   - ✅ Préservation des colonnes originales
   - ✅ Cas limites (valeurs extrêmes)

2. **Helper Functions** (`test_helpers.py`)
   - ✅ Extraction poste (8 postes + défaut)
   - ✅ Extraction domaine étude (5 domaines + défaut)
   - ✅ Extraction statut marital (3 statuts)
   - ✅ Cas limites (données manquantes, rows vides)

3. **Validation Pydantic** (`test_validation.py`)
   - ✅ Validation `PredictRequest`
   - ✅ Validation `EmployeeInputSchema`
   - ✅ Contraintes d'âge (18-70)
   - ✅ Contraintes de satisfaction (1-5)
   - ✅ Contraintes de revenus (> 0)
   - ✅ Valeurs binaires (0 ou 1)

4. **Modèle ML** (`test_model.py`)
   - ✅ Chargement du modèle
   - ✅ Forme des prédictions
   - ✅ Probabilités valides (0-1)
   - ✅ Nombre de features (43)
   - ✅ Reproductibilité
   - ✅ Seuil de classification (0.35)
   - ✅ Cas limites (zeros, grandes valeurs, valeurs négatives)

#### Tests Fonctionnels (`tests/functional/`)

1. **Endpoint /health** (`test_endpoints.py`)
   - ✅ Sans modèle chargé
   - ✅ Avec modèle chargé

2. **Endpoint /predict** (`test_endpoints.py`)
   - ✅ Prédiction réussie
   - ✅ Sans modèle (503)
   - ✅ Feature manquante (422)
   - ✅ Type invalide (422)

3. **Endpoint /predict/csv** (`test_endpoints.py`)
   - ✅ Upload CSV réussi
   - ✅ Sans modèle (503)
   - ✅ Type de fichier invalide (400)
   - ✅ Contenu CSV invalide
   - ✅ Fichier vide
   - ✅ Encodages (UTF-8, Latin-1)
   - ✅ Fichiers volumineux (1000 lignes)

4. **Intégration Base de Données** (`test_endpoints.py`)
   - ✅ Sauvegarde en DB des prédictions
   - ✅ Rollback sur validation échouée
   - ✅ Cohérence employee_data + predictions

5. **Gestion d'Erreurs** (`test_endpoints.py`)
   - ✅ Route 404
   - ✅ Méthode HTTP non autorisée (405)

## Fixtures disponibles (conftest.py)

- `test_db` : Base de données SQLite en mémoire
- `client` : TestClient FastAPI
- `mock_model` : Modèle RandomForest entraîné pour tests
- `app_with_model` : App avec modèle chargé
- `sample_employee_data` : Données employé valides
- `sample_dataframe` : DataFrame pandas de test
- `invalid_employee_data` : Données invalides pour tests
- `csv_content_valid` : Contenu CSV valide
- `csv_content_invalid` : Contenu CSV invalide

## Markers pytest

- `@pytest.mark.unit` - Tests unitaires
- `@pytest.mark.functional` - Tests fonctionnels/intégration
- `@pytest.mark.slow` - Tests lents (fichiers volumineux, etc.)

## Rapport de couverture

Après exécution de `pytest --cov=app --cov-report=html`, consultez :

```
htmlcov/index.html
```

### Fichiers de rapport générés

- `htmlcov/` - Rapport HTML interactif
- `coverage.xml` - Rapport XML pour CI/CD
- Terminal - Résumé avec lignes manquantes

## Bonnes pratiques

1. **Isolement** : Chaque test est indépendant (DB en mémoire par test)
2. **Nomenclature** : `test_<fonction>_<scenario>` (ex: `test_age_too_young`)
3. **AAA Pattern** : Arrange, Act, Assert
4. **Fixtures** : Réutiliser les fixtures globales
5. **Markers** : Taguer les tests longs avec `@pytest.mark.slow`

## CI/CD

Pour intégrer dans un pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Run tests
  run: |
    pytest --cov=app --cov-report=xml --cov-fail-under=70
```

## Debugging

### Afficher les print statements
```powershell
pytest -s
```

### Arrêter au premier échec
```powershell
pytest -x
```

### Mode debug interactif
```powershell
pytest --pdb
```

### Voir les logs
```powershell
pytest --log-cli-level=DEBUG
```

## Maintenance

- Ajouter des tests pour chaque nouvelle fonctionnalité
- Maintenir la couverture > 70%
- Exécuter les tests avant chaque commit
- Mettre à jour les fixtures si le schéma change
