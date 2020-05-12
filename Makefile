lint:
	@autopep8 -i medusa/*.py
	@pyflakes medusa/*.py

utests:
	@pytest utests
utests-verbose:
	@pytest utests -vv
utests-cov:
	@if test -z "$$SHOW"; then pytest utests --cov medusa --cov-report html; \
	else pytest utests --cov medusa --cov-report term; fi;

clean:
	rm -rf htmlcov
	rm .coverage

.PHONY: utests docs
