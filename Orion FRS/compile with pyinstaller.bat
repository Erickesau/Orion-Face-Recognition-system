color a

pyinstaller --collect-data=face_recognition_models --noconsole --icon=icon.ico "Orion FRS v1.3.0.py"

echo.
echo copying media folder using xcopy.
xcopy /I /Y media "dist/Orion FRS v1.3.0/media"
xcopy /I /Y /S data_base "dist/Orion FRS v1.3.0/data_base"
pause
