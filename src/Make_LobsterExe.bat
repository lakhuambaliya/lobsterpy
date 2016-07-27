REM Making exe of lobsterPy
python -OO lobstertoexe.py py2exe
timeout 1
REM if res folder does not exist, then create it.
if not exist ".\res" mkdir ".\res"
REM copy all the extra files needed by GUIF like MT expertsettings, style sheets etc.
REM /A Indicates an ASCII text file.
REM /Y Suppresses prompting to confirm you want to overwrite an existing destination file.
copy ..\res\*.ico .\res\*.ico /Y /A
copy *.txt .\dist\*.txt /Y /A
