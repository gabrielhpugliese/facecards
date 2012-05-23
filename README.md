facecards
=========

ATOL -- no settings - trocar a ulr do face pela do heroku e trocar no aplicativo (tirando o sandbox mode)

Após dar um um git clone no projeto, faça o seguinte (necessario ter um virtualenv instalado)

virtualenv venv --distribute --no-site-packages
source venv/bin/activate
pip install -r requirements.txt 

python manage.py syncdb
python manage.py runserver
