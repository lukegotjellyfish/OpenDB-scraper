#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.

winx = %1%
winy = %2%
winw = %3%
winh = %4%

WinWait, OpenDB_Scraper
WinMove, OpenDB_Scraper,, winx, winy, winw, winh