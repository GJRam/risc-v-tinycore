FILES=$(git ls-files '*.py')

fmt:
	black .

lint:
	pylint .

	 
run:
	python core.py

test:
	pytest .
