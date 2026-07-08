# System Architecture

## Proyecto

NBA IA Predictor

---

# Objetivo

Construir una plataforma profesional capaz de descargar, almacenar, transformar y analizar datos históricos y en tiempo real de la NBA para generar predicciones utilizando Inteligencia Artificial y Machine Learning.

La plataforma estará diseñada con principios de Clean Architecture, modularidad y escalabilidad.

---

# Arquitectura General

```
                    External Data Sources
    ┌─────────────────────────────────────────────┐
    │                                             │
    │ NBA API                                     │
    │ Basketball Reference                        │
    │ pbpstats                                    │
    │ ESPN                                        │
    │ Injury Reports                              │
    │ Betting Odds APIs                           │
    └─────────────────────────────────────────────┘
                          │
                          ▼
                 Data Ingestion Layer
                          │
                          ▼
                    PostgreSQL Database
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Feature Engineering   Data Validation   Analytics
        │
        ▼
      Feature Store
        │
        ▼
 Machine Learning Pipeline
        │
 ┌──────┼────────────┐
 ▼      ▼            ▼
 LR   RandomForest  XGBoost ...
        │
        ▼
 Prediction Engine
        │
        ▼
 Explainability (SHAP)
        │
        ▼
      FastAPI
        │
        ▼
 React Dashboard
```

---

# Capas del sistema

## 1. Data Sources

Responsabilidad:

Obtener información desde distintas fuentes externas.

Entradas:

- NBA API
- Basketball Reference
- pbpstats
- ESPN
- APIs de lesiones
- APIs de cuotas

Salida:

Datos sin procesar.

---

## 2. Data Ingestion

Responsabilidad:

Descargar información automáticamente.

Funciones:

- Descarga
- Validación
- Reintentos
- Eliminación de duplicados

Salida:

Datos almacenados en PostgreSQL.

---

## 3. Database

Responsabilidad:

Persistir toda la información del sistema.

Motor:

PostgreSQL

---

## 4. Feature Engineering

Responsabilidad:

Crear variables que alimentarán los modelos.

Ejemplos:

- Fatigue Score
- Rest Days
- Back-to-back
- ELO
- Forma reciente
- Offensive Momentum
- Defensive Momentum

---

## 5. Machine Learning

Responsabilidad:

Entrenar múltiples modelos.

Modelos iniciales:

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM
- CatBoost

---

## 6. Prediction Engine

Responsabilidad:

Generar probabilidades.

Salidas:

- Ganador
- Handicap
- Total puntos
- Marcador esperado
- Intervalos de confianza

---

## 7. Explainability

Responsabilidad:

Explicar cada predicción.

Tecnologías:

- SHAP
- Feature Importance
- Permutation Importance

---

## 8. Backend

Framework:

FastAPI

Responsabilidad:

Exponer la información mediante API REST.

---

## 9. Frontend

Tecnologías:

- React
- TypeScript
- Tailwind CSS

Responsabilidad:

Visualizar estadísticas y predicciones.

---

# Principios de Arquitectura

- Clean Architecture
- SOLID
- DRY
- KISS
- Modularidad
- Escalabilidad
- Separación de responsabilidades
- Reproducibilidad

---

# Flujo de datos

```
Data Sources
        │
        ▼
Data Ingestion
        │
        ▼
PostgreSQL
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning
        │
        ▼
Predictions
        │
        ▼
FastAPI
        │
        ▼
Frontend
```