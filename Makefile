# Команды для разработки Desert

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

run:
	python manage.py runserver

shell:
	python manage.py shell

test:
	python manage.py test

collectstatic:
	python manage.py collectstatic --noinput

setup: install migrate superuser
	@echo "Проект настроен! Запустите 'make run' для старта сервера"

.PHONY: install migrate superuser run shell test collectstatic setup