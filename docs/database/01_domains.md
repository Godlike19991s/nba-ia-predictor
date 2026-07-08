# Database Domains

> Documento: DB-001  
> Versión: 1.0.0  
> Estado: En desarrollo

---

# Objetivo

Definir los dominios funcionales que conformarán la base de datos del proyecto **NBA IA Predictor**.

Antes de diseñar tablas, relaciones o consultas SQL, es necesario comprender cómo se divide el negocio.

Cada dominio representa un área específica de responsabilidad dentro de la plataforma.

Esta separación permitirá construir una base de datos modular, escalable y fácil de mantener.

---

# ¿Qué es un dominio?

Un dominio es un conjunto de entidades que representan una misma área funcional del sistema.

En lugar de pensar únicamente en tablas, primero identificamos los diferentes problemas que la plataforma debe resolver.

Cada dominio tendrá:

- Entidades
- Relaciones
- Servicios
- Casos de uso
- Reglas de negocio

Este enfoque está inspirado en Domain Driven Design (DDD).

---

# Arquitectura General

```
                    NBA IA Predictor

                ┌──────────────────────┐
                │   Competition Domain  │
                └──────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Teams Domain      Players Domain    Statistics Domain
        │                  │                  │
        └──────────────┬───┴──────────────┐
                       ▼                  ▼
                 Context Domain     Analytics Domain
                       │                  │
                       └──────────┬───────┘
                                  ▼
                          Feature Store Domain
                                  │
                                  ▼
                       Machine Learning Domain
                                  │
                                  ▼
                         Predictions Domain
                                  │
                                  ▼
                     Administration Domain
```

---

# Dominios del sistema

La plataforma estará dividida inicialmente en diez dominios.

| Dominio | Propósito |
|----------|-----------|
| Competition | Información oficial de la competición |
| Teams | Información histórica de las franquicias |
| Players | Información de jugadores y entrenadores |
| Statistics | Estadísticas oficiales de cada partido |
| Context | Factores externos que afectan un partido |
| Analytics | Métricas avanzadas y ratings |
| Feature Store | Variables creadas para IA |
| Machine Learning | Entrenamiento y evaluación de modelos |
| Predictions | Resultados generados por la IA |
| Administration | Configuración y auditoría |

---

# 1. Competition Domain

## Objetivo

Representar la estructura oficial de la competición.

Este dominio responde preguntas como:

- ¿Qué temporada se está jugando?
- ¿Qué partido corresponde?
- ¿Qué equipos participaron?
- ¿Qué conferencia pertenece cada equipo?

## Entidades principales

- League
- Season
- Conference
- Division
- Arena
- Team
- Game
- Schedule
- GameStatus

---

# 2. Teams Domain

## Objetivo

Centralizar toda la información relacionada con las franquicias.

No solamente almacenaremos el nombre del equipo.

También su evolución histórica.

Información de la franquicia.

Cambios de ciudad.

Cambios de nombre.

Conferencia.

División.

Arena.

---

## Posibles entidades

- Team
- TeamHistory
- Arena
- CoachAssignment

---

# 3. Players Domain

## Objetivo

Administrar toda la información relacionada con jugadores.

Este dominio contendrá información permanente.

Nunca estadísticas del partido.

---

## Posibles entidades

- Player

- PlayerPosition

- PlayerContract

- Coach

- Official

---

# 4. Statistics Domain

## Objetivo

Almacenar absolutamente todas las estadísticas oficiales disponibles.

Este será uno de los dominios más grandes del sistema.

---

## Posibles entidades

- TeamBoxscore

- PlayerBoxscore

- PlayByPlay

- ShotChart

- Possession

- Timeout

- Rebound

- Foul

- Turnover

- Substitution

---

# 5. Context Domain

## Objetivo

Guardar información que normalmente no aparece en un boxscore pero influye directamente en el rendimiento.

Aquí estará gran parte del valor del proyecto.

---

## Posibles entidades

- Injury

- InjuryReport

- Lineup

- StartingFive

- Rotation

- RestDays

- BackToBack

- RoadTrip

- Travel

- Weather (cuando aplique)

---

# 6. Analytics Domain

## Objetivo

Guardar métricas avanzadas calculadas a partir de los datos oficiales.

Estas métricas no modifican la información original.

Son resultados derivados.

---

## Posibles entidades

- TeamRating

- PlayerRating

- ELO

- OffensiveRating

- DefensiveRating

- NetRating

- Pace

- FourFactors

- RAPTOR

- PER

- BPM

---

# 7. Feature Store Domain

## Objetivo

Crear las variables que utilizarán los modelos de Machine Learning.

Nunca entrenaremos directamente con las tablas originales.

Los modelos consumirán únicamente información del Feature Store.

---

## Ejemplos de variables

- Fatigue Score

- Rest Advantage

- Home Advantage

- Last 5 Wins

- Last 10 Wins

- Offensive Momentum

- Defensive Momentum

- Travel Distance

- Injury Impact Score

- Team Chemistry Score

---

# 8. Machine Learning Domain

## Objetivo

Administrar todo el ciclo de vida de los modelos.

---

## Posibles entidades

- Experiment

- Dataset

- TrainingRun

- Model

- Hyperparameters

- Metrics

- Calibration

---

# 9. Predictions Domain

## Objetivo

Guardar todas las predicciones realizadas por los modelos.

Cada predicción deberá ser completamente reproducible.

Nunca se almacenará únicamente el resultado.

También se almacenará:

- Modelo utilizado

- Variables utilizadas

- Probabilidad

- Explicación

- Fecha

---

## Posibles entidades

- Prediction

- PredictionExplanation

- ConfidenceInterval

- ProbabilityDistribution

---

# 10. Administration Domain

## Objetivo

Controlar el funcionamiento interno de la plataforma.

No contiene información deportiva.

Contiene información operacional.

---

## Posibles entidades

- DataSource

- SyncJob

- SyncLog

- ImportLog

- ErrorLog

- Configuration

- AuditLog

---

# Principios de Diseño

Durante todo el proyecto seguiremos estas reglas.

## Nunca modificar datos originales

Los datos descargados desde las APIs serán considerados la fuente oficial.

Toda transformación será almacenada en tablas independientes.

---

## Separación de responsabilidades

Cada dominio tendrá una única responsabilidad.

No mezclaremos información de negocio con información analítica.

---

## Escalabilidad

El modelo deberá permitir incorporar nuevas fuentes de datos sin modificar la estructura existente.

---

## Reutilización

Una misma entidad podrá ser utilizada por múltiples módulos del sistema.

---

# Dominios prioritarios para el Sprint 2

Durante esta fase se desarrollarán primero:

1. Competition
2. Teams
3. Players
4. Statistics

Estos cuatro dominios constituyen la base sobre la cual se construirá el resto de la plataforma.

---

# Próximos pasos

Una vez definidos los dominios se procederá a:

- Identificar todas las entidades.
- Definir sus atributos.
- Diseñar las relaciones entre ellas.
- Elaborar el modelo entidad-relación (ERD).
- Diseñar el modelo físico para PostgreSQL mediante SQLAlchemy.