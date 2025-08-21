@echo off
cd /d C:\Users\istva\Desktop\autotube\excelcrawler_codex

:: Stage all changes
git add .

:: Commit with timestamp
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
  set today=%%d-%%b-%%c
)
for /f "tokens=1 delims=:" %%a in ('time /t') do (
  set now=%%a
)
git commit -m "Auto commit on %today% %now%"

:: Push to main
git push origin main

:: Activate venv (if exists)
if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)

:: Run spiders (limit 5 pages each)
scrapy crawl support_excel -s CLOSESPIDER_PAGECOUNT=5
scrapy crawl learn_excel -s CLOSESPIDER_PAGECOUNT=5

pause
