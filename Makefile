fmt:
	black .

lint:
	pylint $(git ls-files '*.py')

run:
	python core.py

test:
	pytest tests


		
