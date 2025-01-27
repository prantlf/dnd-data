all::
	@echo "at first: prepare, install, upgrade"
	@echo "and then: backgrounds, classes, equipment, feats, magic-items, monsters, species, spells"

prepare::
	python3 -m venv .
	echo "Execute: . bin/activate"

install:
	pip install -r requirements.txt

upgrade::
	sed -i 's/[=~]=/>=/' requirements.txt
	pip install -U -r requirements.txt
	pip freeze | awk '/cssselect|lxml|requests|trafilatura/' | awk '!/lxml_html_clean/' > requirements.txt

backgrounds::
	python scripts/download_backgrounds.py

classes::
	python scripts/download_classes.py

equipment::
	python scripts/download_equipment.py

feats::
	python scripts/download_feats.py

monsters::
	python scripts/download_monsters.py

magic-items::
	python scripts/download_magic-items.py

species::
	python scripts/download_species.py

spells::
	python scripts/download_spells.py
