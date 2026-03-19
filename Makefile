FILE=VERSION
VERSION=v`cat $(FILE)`

ndef = $(if $(value $(1)),,$(error $(1) not set, provide $(1), e.g. make $(1)=<value> <target>))

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type d -name .hypothesis -prune -exec rm -rf {} \;
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} \;
	find . -type d -name .pytest_cache -prune -exec rm -rf {} \;
	find . -type d -name .mypy_cache -prune -exec rm -rf {} \;
	find . -type f -name .DS_Store -delete

tree:
	tree skills agents shared hooks scripts

commitizen:
	pipx ensurepath
	pipx install commitizen
	pipx upgrade commitizen

requirements-dev.txt: requirements-dev.in
	uv pip compile --upgrade requirements-dev.in -o $@

install-dev: requirements-dev.txt
	uv pip install -r requirements-dev.txt

setup-dev-env: install-dev commitizen
	pre-commit install

fetch-tags:
	git fetch --tags

changelog: setup-dev-env
	cz changelog --unreleased-version $(VERSION)

# this will update the version, changelog, tag and commit
bump: fetch-tags setup-dev-env
	cz bump

bump-version-minor: fetch-tags setup-dev-env
	cz bump --increment MINOR

bump-version-major: fetch-tags setup-dev-env
	cz bump --increment MAJOR

bump-version-patch: fetch-tags setup-dev-env
	cz bump --increment PATCH

# after the bump, we need to push the tag and the commit in order to actually create the tag
push-tag: fetch-tags
	git push --follow-tags origin main
