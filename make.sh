source clinic/bin/activate
python3 ./generate.py clinics site/index.html --annual_template=annual_template.html
python3 ./rooms.py rooms site
