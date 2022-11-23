fmt:
	black .

lint:
	pylint $(git ls-files '*.py')

		
