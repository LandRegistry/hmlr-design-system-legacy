# This file contains common administration commands. It is language-independent.

# Run this with 'make unittest' or 'make report="true" unittest'
unittest:
	if [ -z ${report} ]; then py.test unit_tests; else py.test --junitxml=test-output/unit-test-output.xml --cov-report=html:test-output/unit-test-cov-report unit_tests; fi

integrationtest:
	py.test --junitxml=test-output/integration-test-output.xml integration_tests

run:
	python3 manage.py runserver
