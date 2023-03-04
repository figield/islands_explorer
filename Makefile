test:
	python3 -m unittest tests/test_*.py
stream:
	bash run.sh tests/test_data/map_milion.txt stream --debug
matrix:
	bash run.sh tests/test_data/map_milion.txt matrix --debug
