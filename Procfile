web: gunicorn "app:create_app()" -w 1
init: flask db init
migrate: flask db migrate
upgrade: flask db upgrade