all:
	@echo "run scripts"

fstruct:
	@tree -f -I "Raw|__pycache__|*.ipynb|.ipynb_checkpoints" ./ >>file_structure.txt

merge:
	@bash merge.sh

clean_data:
	@bash preprocess.sh

mark_breakpoints:
	@bash breakpoint.sh

preprocess:
	$(MAKE) merge
	$(MAKE) clean_data
	$(MAKE) mark_breakpoints

compute_features:
	@bash features.sh
