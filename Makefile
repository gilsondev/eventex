.PHONY: init
init:
	@poetry init

.PHONY: install
install:
	@poetry install

.PHONY: setup
setup: init setup

.PHONY: requirementstxt
requirementstxt:
	@poetry export -f requirements.txt --output requirements.txt

.PHONY: heroku-deploy
heroku-deploy: BRANCH_NAME := "main"
heroku-deploy: requirementstxt
	@git push heroku $(BRANCH_NAME) --force
