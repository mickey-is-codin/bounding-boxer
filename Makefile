PY=python3

BOX_SRC=src/boxer.py

RESULTS_ROOT=results/
BOX_RESULTS=results/box-results/

create_results:
	mkdir -p $(RESULTS_ROOT) $(BOX_RESULTS)

box: create_results
	$(PY) $(BOX_SRC)

box-clean:
	rm -rf $(BOX_RESULTS)
