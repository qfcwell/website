python -O -m py_compile uploadservice.py
python -O -m py_compile upload.py

pyinstaller -F upload.py
