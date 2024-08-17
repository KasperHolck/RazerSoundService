@echo off
cd C:\Program Files (x86)\Microsoft SDKs\ClickOnce\SignTool
echo INSERT THE SIGNING USB
pause
set /p program=Insert full program path:
echo Insert Token in pop-up window...
signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 %program%
pause