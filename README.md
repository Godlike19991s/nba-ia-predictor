# NBA IA Predictor

> Plataforma profesional de Inteligencia Artificial para predicción de partidos de la NBA utilizando Machine Learning, Estadística Avanzada y Automatización.

---

## Descripción

NBA IA Predictor es un proyecto desarrollado desde cero con el objetivo de construir un sistema profesional capaz de:

- Descargar automáticamente más de 10 años de datos históricos de la NBA.
- Almacenar la información en PostgreSQL.
- Generar variables estadísticas avanzadas.
- Entrenar múltiples modelos de Machine Learning.
- Explicar cada predicción mediante técnicas de IA explicable.
- Exponer una API con FastAPI.
- Mostrar predicciones y análisis mediante un dashboard web.

El objetivo principal es desarrollar un sistema completamente reproducible, escalable y documentado.

---

#  Objetivos

- Automatizar la descarga de datos históricos.
- Construir una base de datos profesional.
- Crear un Feature Store.
- Comparar diferentes algoritmos de Machine Learning.
- Generar probabilidades calibradas.
- Explicar las predicciones mediante SHAP.
- Automatizar el entrenamiento del modelo.
- Publicar predicciones mediante una API.

---

# Arquitectura

```
Fuentes de Datos
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
Prediction Engine
        │
        ▼
Explainability
        │
        ▼
FastAPI
        │
        ▼
React Dashboard
```

---

# 🛠 Tecnologías

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

## Base de datos

- PostgreSQL
- pgAdmin

## Machine Learning

- Scikit-Learn
- XGBoost
- LightGBM
- CatBoost

## IA Explicable

- SHAP

## Frontend

- React
- TypeScript
- Tailwind CSS

## DevOps

- Docker
- GitHub Actions

---

#  Estructura

```text
backend/
frontend/
data/
database/
docker/
docs/
models/
notebooks/
scripts/
tests/
```

---

#  Roadmap

- [x] Configuración del entorno
- [ ] Arquitectura del proyecto
- [ ] Base de datos PostgreSQL
- [ ] Descarga histórica NBA
- [ ] Ingeniería de características
- [ ] Machine Learning
- [ ] Explicabilidad
- [ ] API
- [ ] Frontend
- [ ] Automatización
- [ ] Producción

---

# Licencia

MIT

---

#  Autor

José Manuel Nazarit Hidalgo

Proyecto desarrollado con fines educativos y profesionales.