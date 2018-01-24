export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=main.py
killall flask
flask run --host=0.0.0.0 --port=80
