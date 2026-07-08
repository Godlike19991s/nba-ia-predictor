# Database Entities

> Documento: DB-002
>
> Versión: 1.0.0
>
> Estado: En desarrollo

---

# Objetivo

Definir todas las entidades que compondrán la plataforma de datos del proyecto **NBA IA Predictor**.

Una entidad representa un objeto del mundo real o un concepto del negocio que necesita ser almacenado, relacionado o procesado.

Este documento constituye el catálogo oficial de entidades del sistema.

---

# Arquitectura de Datos

Todas las entidades pertenecerán a una de las siguientes capas.

```
RAW
│
├── Datos originales descargados
│
▼
CORE
│
├── Datos normalizados
│
▼
ANALYTICS
│
└── Variables para IA
```

---

# Convención

Cada entidad tendrá definida la siguiente información.

- Nombre
- Dominio
- Capa
- Descripción
- Relaciones
- Consumidores

---

# Competition Domain

## League

### Capa

CORE

### Descripción

Representa la liga deportiva.

Inicialmente solamente existirá NBA.

Se deja preparada la arquitectura para soportar futuras ligas.

### Consumido por

- Season

---

## Season

### Capa

CORE

### Descripción

Representa una temporada oficial.

Ejemplo

2024-2025

### Consumido por

- Games
- Standings
- Team Ratings

---

## Conference

### Capa

CORE

Representa una conferencia.

Actualmente:

- East
- West

---

## Division

### Capa

CORE

Representa una división oficial.

---

## Arena

### Capa

CORE

Representa el estadio donde se disputa un partido.

---

## Game

### Capa

CORE

Entidad central del sistema.

Todo gira alrededor del partido.

Será la entidad más relacionada de toda la plataforma.

Relacionada con:

- Teams

- Officials

- Injuries

- Boxscores

- Predictions

- Play By Play

- Lineups

- Odds

---

## Schedule

### Capa

CORE

Calendario oficial de la competición.

---

## GameStatus

### Capa

CORE

Estado del partido.

Ejemplos

- Scheduled

- Live

- Finished

- Postponed

---

# Teams Domain

## Team

### Capa

CORE

Representa una franquicia NBA.

No representa una temporada.

Representa la organización.

---

## TeamHistory

### Capa

CORE

Permite registrar cambios históricos.

Ejemplo

Seattle SuperSonics

↓

Oklahoma City Thunder

---

## CoachAssignment

### Capa

CORE

Historial de entrenadores.

---

# Players Domain

## Player

### Capa

CORE

Representa un jugador.

Nunca contendrá estadísticas.

Solo información permanente.

---

## Coach

### Capa

CORE

Representa entrenadores.

---

## Official

### Capa

CORE

Representa árbitros oficiales.

---

# Statistics Domain

## TeamBoxscore

### Capa

CORE

Estadísticas de un equipo en un partido.

Una fila por equipo.

---

## PlayerBoxscore

### Capa

CORE

Estadísticas de un jugador en un partido.

Una fila por jugador.

---

## PlayByPlay

### Capa

RAW

Registro cronológico de cada evento.

---

## ShotChart

### Capa

RAW

Todos los lanzamientos realizados.

---

## Possession

### Capa

ANALYTICS

Posesiones calculadas.

---

## Rebound

### Capa

ANALYTICS

Eventos de rebote.

---

## Turnover

### Capa

ANALYTICS

Eventos de pérdida.

---

## Timeout

### Capa

RAW

Tiempos muertos.

---

## Substitution

### Capa

RAW

Cambios de jugadores.

---

## Foul

### Capa

RAW

Registro de faltas.

---

# Context Domain

## Injury

### Capa

CORE

Lesiones registradas.

---

## InjuryReport

### Capa

RAW

Reporte original descargado.

---

## Lineup

### Capa

CORE

Alineación disponible.

---

## StartingFive

### Capa

CORE

Quinteto inicial.

---

## Rotation

### Capa

ANALYTICS

Rotación estimada.

---

## Travel

### Capa

ANALYTICS

Kilómetros recorridos.

---

## RestDays

### Capa

ANALYTICS

Días de descanso.

---

## BackToBack

### Capa

ANALYTICS

Indica si el equipo jugó la noche anterior.

---

## RoadTrip

### Capa

ANALYTICS

Información de giras.

---

# Analytics Domain

## TeamRating

### Capa

ANALYTICS

Rating avanzado del equipo.

---

## PlayerRating

### Capa

ANALYTICS

Rating avanzado del jugador.

---

## ELO

### Capa

ANALYTICS

Ranking ELO.

---

## OffensiveRating

### Capa

ANALYTICS

---

## DefensiveRating

### Capa

ANALYTICS

---

## NetRating

### Capa

ANALYTICS

---

## Pace

### Capa

ANALYTICS

---

## FourFactors

### Capa

ANALYTICS

---

## PER

### Capa

ANALYTICS

Player Efficiency Rating.

---

## BPM

### Capa

ANALYTICS

Box Plus Minus.

---

# Feature Store Domain

## Feature

### Capa

ANALYTICS

Representa una variable calculada.

---

## FeatureSet

### Capa

ANALYTICS

Agrupa conjuntos de variables.

---

## Dataset

### Capa

ANALYTICS

Conjunto de entrenamiento.

---

# Machine Learning Domain

## Experiment

### Capa

ANALYTICS

Representa un experimento.

---

## TrainingRun

### Capa

ANALYTICS

Cada entrenamiento realizado.

---

## Model

### Capa

ANALYTICS

Modelo entrenado.

---

## Hyperparameters

### Capa

ANALYTICS

Configuración utilizada.

---

## Metrics

### Capa

ANALYTICS

Métricas obtenidas.

---

## Calibration

### Capa

ANALYTICS

Información de calibración.

---

# Predictions Domain

## Prediction

### Capa

ANALYTICS

Predicción generada.

---

## PredictionExplanation

### Capa

ANALYTICS

Explicación SHAP.

---

## ProbabilityDistribution

### Capa

ANALYTICS

Distribución completa de probabilidades.

---

## ConfidenceInterval

### Capa

ANALYTICS

Intervalos de confianza.

---

# Administration Domain

## DataSource

### Capa

CORE

Fuente de datos.

---

## SyncJob

### Capa

CORE

Proceso automático.

---

## SyncLog

### Capa

CORE

Historial de sincronizaciones.

---

## ImportLog

### Capa

CORE

Importaciones realizadas.

---

## ErrorLog

### Capa

CORE

Errores detectados.

---

## Configuration

### Capa

CORE

Configuración del sistema.

---

## AuditLog

### Capa

CORE

Auditoría de operaciones.

---

# Resumen

## Total aproximado de entidades

| Dominio | Entidades |
|----------|----------:|
| Competition | 8 |
| Teams | 3 |
| Players | 3 |
| Statistics | 10 |
| Context | 8 |
| Analytics | 9 |
| Feature Store | 3 |
| Machine Learning | 6 |
| Predictions | 4 |
| Administration | 6 |

**Total estimado: 60 entidades**

---

# Próximo documento

El siguiente documento será:

**DB-003 – Relationships**

En él se definirán todas las relaciones entre entidades, sus cardinalidades (1:1, 1:N, N:M) y las reglas de integridad que servirán como base para construir el diagrama entidad-relación (ERD) y, posteriormente, los modelos de SQLAlchemy.