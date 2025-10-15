@echo off
REM FloatChat - Add Screenshots Script
REM This script helps you add screenshots to the repository

echo.
echo ========================================
echo   FloatChat Screenshot Setup
echo ========================================
echo.

echo STEP 1: Save Your Screenshots
echo -----------------------------
echo Please save your screenshots with these exact names:
echo.
echo   1. demo-temperature-trends.png
echo   2. demo-fishing-zones.png
echo.
echo Save them to: assets\screenshots\
echo.

pause

echo.
echo STEP 2: Verify Screenshots
echo --------------------------

if exist "assets\screenshots\demo-temperature-trends.png" (
    echo [OK] demo-temperature-trends.png found!
) else (
    echo [MISSING] demo-temperature-trends.png NOT found
    echo Please add it to assets\screenshots\
)

if exist "assets\screenshots\demo-fishing-zones.png" (
    echo [OK] demo-fishing-zones.png found!
) else (
    echo [MISSING] demo-fishing-zones.png NOT found
    echo Please add it to assets\screenshots\
)

echo.
echo STEP 3: Ready to Commit?
echo ------------------------
echo.
set /p commit="Do you want to commit the screenshots now? (y/n): "

if /i "%commit%"=="y" (
    echo.
    echo Adding files to git...
    git add assets/screenshots/*.png
    git add assets/screenshots/README.md
    git add README.md
    
    echo.
    echo Committing changes...
    git commit -m "Add application screenshots and update README with demo images"
    
    echo.
    echo Pushing to GitHub...
    git push origin enhanced-version
    
    echo.
    echo [SUCCESS] Screenshots pushed to GitHub!
    echo Check your repository at: https://github.com/Swapnil565/FloatChat
) else (
    echo.
    echo Skipped commit. Run this script again when ready.
)

echo.
pause
