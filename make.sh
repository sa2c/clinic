if [ -x "$(command -v python3)" ]
then
    PYTHON=python3
elif [ -x "$(command -v python36)" ]
then
    PYTHON=python36
else
    echo Python 3 not found
    exit 1
fi

if [ ! -f "clinic/bin/activate" ]
then
    $PYTHON -m venv clinic
    source clinic/bin/activate
    pip install -r requirements.txt
else
    source clinic/bin/activate
fi
    
$PYTHON ./generate.py clinics site/index.html --annual_template=annual_template.html
$PYTHON ./rooms.py rooms site
