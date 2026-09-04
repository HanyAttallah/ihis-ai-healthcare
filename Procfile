web: flask --app run.py db upgrade && python -m scripts.seed_roles && python -m scripts.seed_public_demo && gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 120 run:app
