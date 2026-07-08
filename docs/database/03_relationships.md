# Database Relationships

> Documento: DB-003
>
> Versión: 1.0.0
>
> Estado: En desarrollo

---

# Objetivo

Definir todas las relaciones existentes entre las entidades del sistema.

Este documento constituye la especificación oficial de las relaciones del modelo de datos del proyecto **NBA IA Predictor**.

Su propósito es garantizar que todas las entidades mantengan integridad referencial, consistencia y escalabilidad.

---

# Tipos de relaciones

Durante el proyecto se utilizarán tres tipos principales de relaciones.

## Uno a Uno (1:1)

Una entidad posee exactamente un registro relacionado.

Ejemplo:

```
Game
    │
    ▼
GameStatus
```

---

## Uno a Muchos (1:N)

Una entidad puede tener múltiples registros relacionados.

Ejemplo:

```
Team
    │
    ├────────► Games
```

---

## Muchos a Muchos (N:M)

Dos entidades pueden relacionarse múltiples veces.

Siempre será implementada mediante una tabla intermedia.

Ejemplo

```
Game

      ▲

      │

PlayerBoxscore

      │

      ▼

Player
```

---

# Competition Domain

## League → Season

Cardinalidad

```
League

1

│

└───────────────∞

Season
```

Una liga contiene múltiples temporadas.

---

## Season → Game

```
Season

1

│

└──────────────∞

Game
```

Cada temporada contiene muchos partidos.

Cada partido pertenece únicamente a una temporada.

---

## Conference → Team

```
Conference

1

│

└──────────────∞

Team
```

---

## Division → Team

```
Division

1

│

└──────────────∞

Team
```

---

## Arena → Game

```
Arena

1

│

└──────────────∞

Game
```

Un estadio puede albergar muchos partidos.

---

# Team Relationships

## Team → Home Games

```
Team

1

│

└──────────────∞

Game.home_team
```

---

## Team → Away Games

```
Team

1

│

└──────────────∞

Game.away_team
```

Un equipo puede jugar como local o visitante múltiples veces.

---

## Team → TeamBoxscore

```
Team

1

│

└──────────────∞

TeamBoxscore
```

---

## Team → CoachAssignment

```
Team

1

│

└──────────────∞

CoachAssignment
```

---

# Player Relationships

## Player → PlayerBoxscore

```
Player

1

│

└──────────────∞

PlayerBoxscore
```

Un jugador tendrá un registro por partido.

---

## Player → Injury

```
Player

1

│

└──────────────∞

Injury
```

---

## Player → Lineup

```
Player

1

│

└──────────────∞

Lineup
```

---

# Game Relationships

La entidad **Game** es el núcleo del sistema.

Todas las entidades principales dependerán de ella.

```
Game

├────────────► TeamBoxscore

├────────────► PlayerBoxscore

├────────────► PlayByPlay

├────────────► Lineup

├────────────► Injury

├────────────► OfficialAssignment

├────────────► BettingOdds

├────────────► Prediction

└────────────► FeatureSet
```

---

## Game → TeamBoxscore

```
Game

1

│

└──────────────2

TeamBoxscore
```

Cada partido tendrá exactamente dos boxscores de equipo.

---

## Game → PlayerBoxscore

```
Game

1

│

└──────────────∞

PlayerBoxscore
```

---

## Game → PlayByPlay

```
Game

1

│

└──────────────∞

PlayByPlay
```

---

## Game → Lineup

```
Game

1

│

└──────────────∞

Lineup
```

---

## Game → OfficialAssignment

```
Game

1

│

└──────────────∞

OfficialAssignment
```

---

## Game → BettingOdds

```
Game

1

│

└──────────────∞

BettingOdds
```

Un partido puede tener múltiples casas de apuestas.

---

# Statistics Relationships

## TeamBoxscore → Team

```
TeamBoxscore

∞

│

└──────────────1

Team
```

---

## PlayerBoxscore → Player

```
PlayerBoxscore

∞

│

└──────────────1

Player
```

---

## PlayerBoxscore → Team

```
PlayerBoxscore

∞

│

└──────────────1

Team
```

---

## PlayerBoxscore → Game

```
PlayerBoxscore

∞

│

└──────────────1

Game
```

---

# Context Relationships

## Injury → Player

```
Injury

∞

│

└──────────────1

Player
```

---

## Lineup → Team

```
Lineup

∞

│

└──────────────1

Team
```

---

## StartingFive → Game

```
StartingFive

∞

│

└──────────────1

Game
```

---

## Travel → Team

```
Travel

∞

│

└──────────────1

Team
```

---

## RestDays → Team

```
RestDays

∞

│

└──────────────1

Team
```

---

# Analytics Relationships

## TeamRating → Team

```
TeamRating

∞

│

└──────────────1

Team
```

---

## PlayerRating → Player

```
PlayerRating

∞

│

└──────────────1

Player
```

---

## ELO → Team

```
ELO

∞

│

└──────────────1

Team
```

---

# Feature Store Relationships

## Feature → FeatureSet

```
Feature

∞

│

└──────────────1

FeatureSet
```

---

## FeatureSet → Game

```
FeatureSet

∞

│

└──────────────1

Game
```

Cada partido generará un conjunto de variables.

---

# Machine Learning Relationships

## Dataset → TrainingRun

```
Dataset

1

│

└──────────────∞

TrainingRun
```

---

## Model → TrainingRun

```
Model

1

│

└──────────────∞

TrainingRun
```

---

## TrainingRun → Metrics

```
TrainingRun

1

│

└──────────────1

Metrics
```

---

# Predictions Relationships

## Prediction → Game

```
Prediction

∞

│

└──────────────1

Game
```

---

## Prediction → Model

```
Prediction

∞

│

└──────────────1

Model
```

---

## Prediction → PredictionExplanation

```
Prediction

1

│

└──────────────1

PredictionExplanation
```

---

# Administration Relationships

## DataSource → SyncJob

```
DataSource

1

│

└──────────────∞

SyncJob
```

---

## SyncJob → SyncLog

```
SyncJob

1

│

└──────────────∞

SyncLog
```

---

## AuditLog

AuditLog podrá relacionarse con cualquier entidad mediante referencias de auditoría.

---

# Entidades con mayor número de relaciones

| Entidad | Relaciones aproximadas |
|----------|-----------------------:|
| Game | 12+ |
| Team | 10+ |
| Player | 8+ |
| PlayerBoxscore | 6+ |
| TeamBoxscore | 5+ |
| Prediction | 4+ |

Estas entidades constituyen el núcleo del modelo de datos.

---

# Reglas generales

- Todas las tablas tendrán una clave primaria (`id`).
- Las claves foráneas deberán mantener integridad referencial.
- No se permitirán registros huérfanos.
- Las relaciones N:M siempre se implementarán mediante tablas puente.
- Los datos históricos nunca se sobrescribirán.
- Las eliminaciones físicas estarán restringidas; se preferirá el uso de estados o marcas temporales cuando sea necesario.

---

# Próximo documento

El siguiente documento será:

**DB-004 – Entity Relationship Diagram (ERD)**

A partir de las relaciones definidas en este documento se construirá el diagrama entidad-relación oficial del proyecto, que servirá como base para implementar los modelos ORM con SQLAlchemy y las migraciones mediante Alembic.