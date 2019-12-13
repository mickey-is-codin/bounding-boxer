# Python Program
PY=python3

# Source Files
BOX_SRC=src/boxer.py

# Result Directories
RESULTS_ROOT=results/
BOX_RESULTS=results/box-results/

create_results:
	mkdir -p $(RESULTS_ROOT) $(BOX_RESULTS)

box: create_results
	$(PY) $(BOX_SRC)

box-clean:
	rm -rf $(BOX_RESULTS)
