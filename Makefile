test:
	python3 -m unittest tests/test_*.py
stream:
	bash run.sh tests/test_data/map_milion.txt stream --debug
matrix:
	bash run.sh tests/test_data/map_milion.txt matrix --debug
graph:
	python3 main_arbitrary_solution.py tests/test_data/map_milion.txt --debug
