all:
	@echo "run scripts"

fstruct:
	@tree -f -I "Raw|Features|__pycache__|*.ipynb|.ipynb_checkpoints" ./ >>file_structure.txt

merge:
	@bash merge.sh

preprocess:
	@bash preprocess.sh

compute_features:
	@bash features.sh
