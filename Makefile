F:=$(shell date +"%Y-%m-%d-%H-%M-%S")

env:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel
	poetry update -vvv
	#.venv/bin/jupyter nbextension enable --py widgetsnbextension
	poetry export -f requirements.txt --without-hashes >requirements.txt

