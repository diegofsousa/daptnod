clean:
	find . -name "*.pyc" -exec rm -rf {} \;

run:
	python manage.py runserver 0.0.0.0:8000 	
runAll:
	celery -A geocovid  worker --loglevel=info &
	python manage.py runserver 0.0.0.0:8000 
migrate:
	python manage.py migrate
migrations:
	python manage.py makemigrations
user:
	python manage.py createsuperuser

shell:
	python manage.py shell

ishell:
	python manage.py shell -i ipython

jupyter:
	python manage.py shell_plus --notebook
test:
	python manage.py test

cleanmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

dockerup:
	docker-compose up -d
dockerdown:
	docker-compose down --volumes

update-deploy:
	sudo systemctl restart gunicorn
	sudo systemctl restart gunicorn.socket gunicorn.service
	sudo systemctl daemon-reload
	sudo nginx -t && sudo systemctl restart nginx
