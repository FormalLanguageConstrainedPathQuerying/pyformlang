PYTHON ?= python3
PYTEST ?= pytest

test-code:
	$(PYTEST) --showlocals -v pyformlang

test-coverage:
		rm -rf coverage .coverage
		$(PYTEST) pyformlang --showlocals -v --cov=pyformlang --cov-report=html:coverage

doc:
	$(MAKE) -C doc html

clean:
	rm -rf coverage .coverage
	$(MAKE) -C doc clean

.PHONY: doc clean