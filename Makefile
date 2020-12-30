PYTHON=python3
PIP=pip3

venv: venv/touchfile

venv/touchfile:: 
	test -d venv || virtualenv venv
	source venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile

venv_end: 
	deactivate 

dependencies:
	$(PIP) install --exists-action w -r requirements.txt

get_nodes:	
	@read -p "Enter search regexp:" regexp; \
	cd codeFourni/server; \
	python3 -c "import get_like_nodes; get_like_nodes.get_like_nodes('$${regexp}') " ;

get_highway_example:		
	cd codeFourni/server; \
	python3 -c "import tile; tile.get_highway_fixed() " ;	

run_WMS:
	cd codeFourni/server; \
	python3 WMSserver.py