#PATH := "${HOME}/.local/bin:${PATH}"
#SHELL := env PATH=$(PATH) /bin/bash
F:=$(shell date +"%Y-%m-%d-%H-%M-%S")

env:
	echo $(PATH)
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel
	poetry update --with dev -vvv
	#.venv/bin/jupyter nbextension enable --py widgetsnbextension
	poetry export -f requirements.txt --without-hashes >requirements.txt
