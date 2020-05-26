/U
@echo off
CLS
TITLE OpenDB_Scraper
CLS
call "adjust_cmd.exe" "100" "70" "1385" "200"
CLS


call "D:\Code\Python Versions\3.7.3\python.exe" "OpenDB_Scrape.py"
PAUSE