requirementsRemove:
	pip freeze > requirements.txt
	pip uninstall -y -r requirements.txt

requirementsAdd:
	pip freeze > requirements.txt

requirementsInstall:
	pip install -r requirements.txt

test:
	python -m pytest
