rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "media/*" -delete

bash cfg.sh
python3 manage.py createsuperuser --email admin@admin.com