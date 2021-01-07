PYTHON=python3
PIP=pip3
SHELL := /bin/bash

venv: venv/touchfile

venv/touchfile::
	python3 -m pip install --user virtualenv
	test -d venv || virtualenv venv; \
	source venv/bin/activate; pip install -Ur requirements.txt; \
	touch venv/touchfile

venv_end: 
	deactivate 

dependencies:
	$(PIP) install --exists-action w -r requirements.txt

get_nodes:venv dependencies
	@read -p "Enter search regexp:" regexp; \
	cd osm/server; \
	python3 -c "import get_like_nodes; get_like_nodes.get_like_nodes('$${regexp}') " ;

get_highway_example: venv	
	cd osm/server; \
	python3 -c "import tile; tile.get_highway_fixed() " ;	

run_WMS: venv
	cd osm/server; \
	python3 WMSserver.py