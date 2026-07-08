# Database Design

> Documento: DB-004
>
> Versión: 1.0.0
>
> Estado: Aprobado
>
> Proyecto: NBA IA Predictor

---

# Objetivo

Definir los principios, convenciones y decisiones de diseño que regirán la base de datos del proyecto.

Este documento establece la arquitectura física y lógica que deberá seguir toda implementación en PostgreSQL y SQLAlchemy.

Todas las tablas, modelos ORM, migraciones y consultas deberán respetar las reglas aquí descritas.

---

# Filosofía de Diseño

La base de datos del proyecto no será únicamente un lugar para almacenar información.

Será la plataforma central sobre la cual funcionarán:

- Descarga automática de datos
- Ingeniería de datos
- Ingeniería de características
- Machine Learning
- API REST
- Dashboard
- Automatización

Por esta razón, el diseño prioriza:

- Escalabilidad
- Integridad
- Rendimiento
- Reproducibilidad
- Mantenibilidad

---

# Arquitectura General

La plataforma estará dividida en tres capas de datos.

```
                 PostgreSQL

        ┌─────────────────────────┐
        │          RAW            │
        └─────────────────────────┘
                   │
          Limpieza y Validación
                   │
                   ▼
        ┌─────────────────────────┐
        │         CORE            │
        └─────────────────────────┘
                   │
      Feature Engineering / IA
                   │
                   ▼
        ┌─────────────────────────┐
        │      ANALYTICS          │
        └─────────────────────────┘
```

Cada capa tiene responsabilidades claramente definidas.

---

# Capa RAW

## Objetivo

Almacenar exactamente la información descargada desde las fuentes externas.

No se realizarán modificaciones sobre estos datos.

Representan la fuente oficial de información.

Ejemplos:

- raw_games
- raw_players
- raw_boxscores
- raw_play_by_play
- raw_injuries

---

# Capa CORE

## Objetivo

Contener datos normalizados y relacionados.

Aquí vivirán las entidades principales del negocio.

Ejemplos:

- teams
- players
- seasons
- games
- player_boxscores
- team_boxscores

Toda la lógica de negocio utilizará esta capa.

---

# Capa ANALYTICS

## Objetivo

Contener información calculada.

Nunca almacenará datos originales.

Ejemplos:

- fatigue_score
- elo
- team_rating
- player_rating
- feature_sets
- predictions

Esta capa será utilizada por los modelos de Machine Learning.

---

# Convenciones de Nombres

## Tablas

Todas las tablas utilizarán:

- minúsculas
- snake_case
- nombres en plural

Ejemplos

Correcto

```
players

team_boxscores

games
```

Incorrecto

```
Players

Game

PlayerBoxScore
```

---

## Columnas

Todas las columnas utilizarán:

snake_case

Ejemplo

```
game_date

home_team_id

minutes_played
```

---

## Claves Primarias

Todas las tablas tendrán una clave primaria.

Nombre

```
id
```

Tipo

```
BIGINT
```

Inicialmente utilizaremos BIGINT autoincremental por simplicidad y rendimiento.

En el futuro podrá evaluarse el uso de UUID si aparecen necesidades de distribución.

---

## Claves Foráneas

Todas las claves foráneas seguirán la convención

```
nombre_entidad_id
```

Ejemplos

```
team_id

player_id

game_id

season_id
```

---

# Convenciones de Fechas

Todos los registros importantes deberán incluir:

```
created_at

updated_at
```

Tipo

```
TIMESTAMP WITH TIME ZONE
```

Siempre se almacenarán en UTC.

---

# Eliminación de Datos

No se eliminarán registros históricos.

La prioridad será preservar la trazabilidad.

Cuando sea necesario se utilizarán estados o marcas temporales antes que eliminaciones físicas.

---

# Integridad Referencial

Todas las relaciones utilizarán claves foráneas.

No se permitirán registros huérfanos.

Toda referencia deberá existir previamente.

---

# Normalización

La capa CORE seguirá principalmente la Tercera Forma Normal (3NF).

Objetivos:

- Reducir duplicidad.
- Facilitar mantenimiento.
- Garantizar consistencia.

Las desnormalizaciones solo se permitirán en la capa ANALYTICS cuando aporten mejoras significativas de rendimiento.

---

# Índices

Solo se crearán índices cuando exista una necesidad clara.

Los índices iniciales estarán orientados a:

- búsquedas por fecha
- búsquedas por jugador
- búsquedas por equipo
- búsquedas por temporada
- consultas de predicción

---

# Auditoría

Las operaciones importantes deberán poder rastrearse.

Se registrarán:

- sincronizaciones
- importaciones
- errores
- entrenamientos
- predicciones

---

# Escalabilidad

La base de datos deberá soportar:

- múltiples temporadas
- múltiples ligas
- nuevas fuentes de datos
- nuevos modelos de IA

Sin necesidad de rediseñar la estructura principal.

---

# Rendimiento

La prioridad será:

1. Integridad
2. Legibilidad
3. Rendimiento

No se sacrificarán principios de diseño por optimizaciones prematuras.

---

# Compatibilidad

Aunque PostgreSQL será el motor oficial, el diseño buscará minimizar dependencias específicas cuando sea razonable.

Esto facilitará futuras migraciones o pruebas con otros motores si fueran necesarias.

---

# Tecnologías Asociadas

La implementación utilizará:

- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Docker
- Python 3.13+

---

# Reglas de Desarrollo

Durante el proyecto se seguirán las siguientes reglas:

- Nunca modificar datos RAW.
- Toda transformación deberá generar nuevos registros.
- Las entidades CORE representan la verdad del negocio.
- La capa ANALYTICS nunca reemplazará la capa CORE.
- Todo modelo ORM deberá estar documentado.
- Toda migración deberá ser versionada con Alembic.
- Ningún cambio en la estructura podrá realizarse directamente sobre la base de datos.

---

# Flujo de Datos

```
Fuentes Externas

        │

        ▼

RAW

        │

Validación

        │

        ▼

CORE

        │

Feature Engineering

        │

        ▼

ANALYTICS

        │

Machine Learning

        │

        ▼

Predicciones

        │

FastAPI

        │

Frontend
```

---

# Resultado Esperado

Al finalizar el proyecto la base de datos deberá ser capaz de:

- almacenar más de diez años de historia de la NBA
- soportar millones de registros
- alimentar múltiples modelos de IA
- permitir consultas complejas de manera eficiente
- servir como base para análisis estadístico avanzado
- facilitar la incorporación de nuevas fuentes de datos sin rediseñar la arquitectura

---

# Próximos Pasos

Con este documento finaliza la fase inicial de diseño de la base de datos.

El siguiente paso del proyecto será la implementación utilizando:

- SQLAlchemy 2.x
- Alembic
- PostgreSQL

A partir de este punto comenzará el desarrollo de los modelos ORM y las migraciones que materializarán esta arquitectura.