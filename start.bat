@echo off
cd /d %~dp0
echo AndroBoss saytini ishga tushirish...
echo.
echo Admin panel: http://127.0.0.1:8000/admin/
echo   Login: admin
echo   Parol: admin123
echo.
echo Statistika: http://127.0.0.1:8000/statistics/
echo Sayt: http://127.0.0.1:8000/
echo.
venv\Scripts\python manage.py runserver 0.0.0.0:8000
pause
