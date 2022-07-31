color a

pyinstaller --collect-data=face_recognition_models --noconsole --icon=icon.ico "Orion FRS v1.2.8.py"

echo.
echo copying media folder using xcopy.
xcopy /I /Y media "dist/Orion FRS v1.2.8/media"
xcopy /I /Y /S data_base "dist/Orion FRS v1.2.8/data_base"
pause
