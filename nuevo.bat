@echo off
title NBA IA Predictor - Project Structure
color 0A

echo.
echo ===============================================
echo      NBA IA Predictor - Structure Creator
echo ===============================================
echo.

REM =====================================================
REM Root folders
REM =====================================================

for %%d in (
backend
frontend
data
database
docker
docs
models
notebooks
scripts
tests
.github
) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [+] Created %%d
    ) else (
        echo [=] Exists %%d
    )
)

echo.
echo Creating backend structure...

for %%d in (
backend\app
backend\app\api
backend\app\api\v1
backend\app\api\dependencies
backend\app\config
backend\app\core
backend\app\database
backend\app\ingestion
backend\app\preprocessing
backend\app\feature_engineering
backend\app\ml
backend\app\ml\training
backend\app\ml\inference
backend\app\ml\evaluation
backend\app\ml\explainability
backend\app\prediction
backend\app\services
backend\app\utils
backend\app\models
backend\app\schemas
backend\app\tests
) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [+] Created %%d
    ) else (
        echo [=] Exists %%d
    )
)

echo.
echo Creating data structure...

for %%d in (
data\raw
data\processed
data\interim
data\external
) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [+] Created %%d
    ) else (
        echo [=] Exists %%d
    )
)

echo.
echo Creating docs structure...

for %%d in (
docs\architecture
docs\database
docs\decisions
docs\machine-learning
docs\api
docs\deployment
docs\roadmap
) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [+] Created %%d
    ) else (
        echo [=] Exists %%d
    )
)

echo.
echo Creating Docker structure...

for %%d in (
docker\postgres
docker\pgadmin
docker\compose
) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [+] Created %%d
    ) else (
        echo [=] Exists %%d
    )
)

echo.
echo Creating GitHub structure...

if not exist ".github\workflows" (
    mkdir ".github\workflows"
    echo [+] Created .github\workflows
) else (
    echo [=] Exists .github\workflows
)

echo.
echo ===============================================
echo      Project structure completed
echo ===============================================
echo.

pause