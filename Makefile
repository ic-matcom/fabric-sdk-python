test-fast:
	python -m pytest fabric_sdk tests -v --tb=short -m "not time"

test: 
	python -m pytest fabric_sdk tests -v --tb=short --slow-last

test-full:
	python -m pytest fabric_sdk tests -v --tb=short --slow-last