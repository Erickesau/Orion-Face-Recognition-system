color a

pyinstaller --collect-data=face_recognition_models --collect-data=cv2 --noconsole --icon=media/icon.ico "Orion FRS v1.3.4.py"

echo.
echo copying media folder using xcopy.
xcopy /I /Y /S media "dist/Orion FRS v1.3.4/media"
xcopy /I /Y /S data_base "dist/Orion FRS v1.3.4/data_base"
pause
