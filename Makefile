HOST=127.0.0.1
TEST_PATH=./tests/
SRC_DIR=$(CURDIR)
SSH_HOST=localhost
SSH_PORT=1993
SSH_USER=vagner
SSH_TARGET_DIR=/home/vagner/projects
#SSH_TARGET_DIR=/home/vagner
#SSH_KEY=/media/sf_Vagner/AWS/aws-s01-dev-key.pem
SSH_KEY=/run/media/vagner/Dados/Vagner/Dropbox/AWS/keys/aws-s01-dev-key.pem
EXCLUDE_FILES={'.*','*.log','*conf.py'}

help:
	@echo "    clean"
	@echo "        Remove python artifacts."
	@echo "    isort"
	@echo "        Sort import statements."
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    test"
	@echo "        Run py.test"
	@echo '    run'
	@echo '        Run the `my_project` service on your local machine.'

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force  {} +
	@echo 'Arquivos removidos com sucesso'

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean
	@py.test --verbose --color=yes --pdb $(TEST_PATH)

run:
	@python run.py

deploy: clean
	@rsync -e "ssh -p $(SSH_PORT)" -P -trvz --exclude=$(EXCLUDE_FILES) \
		$(SRC_DIR) $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)


.PHONY: clean isort lint test run deploy
