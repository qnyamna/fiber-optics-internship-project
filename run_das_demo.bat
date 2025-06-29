@echo off
echo === Starting DAS Demo ===
cd /d %~dp0
cd C:\Users\ebrah\Downloads\fiber-optics-project-main\fiberoptics-das-simulator-main

:: Step 1: Start Docker services
echo.
echo [1/6] Starting Docker Services...
docker-compose --env-file ./dependson-services/.env -f ./dependson-services/compose-kafka.yml up -d

:: Step 2: Wait for services to initialize
echo.
echo [2/6] Waiting 30 seconds for initialization...
timeout /t 30

:: Step 3: Run DAS Simulator
echo.
echo [3/6] Running DAS Simulator...
for /f "delims=" %%i in (das-producer\defaults.cmd) do set %%i
java -jar ./das-producer/target/das-producer-2.0.12-SNAPSHOT.jar

:: Step 4: Run analysis
echo.
echo [4/6] Running demo analysis...
python run_demo_analysis.py

:: Step 5: View results
echo.
echo [5/6] Viewing results...
python view_results.py

:: Step 6: Optionally stop Docker services
echo.
set /p stopDocker="Do you want to stop Docker services now? (y/n): "
if /i "%stopDocker%"=="y" (
    echo [6/6] Stopping Docker Services...
    docker-compose --env-file ./dependson-services/.env -f ./dependson-services/compose-kafka.yml down
) else (
    echo Skipped stopping Docker.
)

echo.
echo === DAS Demo Complete ===
pause
