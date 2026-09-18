.PHONY: install check test sirene osm match resolve crawl validate export stats run demo

PY ?= python3

install:
	$(PY) -m pip install -r requirements.txt

check:      ## le réseau est-il ouvert vers data.gouv + Overpass ?
	$(PY) -m prospect selfcheck

test:
	$(PY) -m unittest discover -s tests -v

sirene:
	$(PY) -m prospect sirene

osm:
	$(PY) -m prospect osm

match:
	$(PY) -m prospect match

resolve:
	$(PY) -m prospect resolve

crawl:
	$(PY) -m prospect crawl

validate:
	$(PY) -m prospect validate

export:
	$(PY) -m prospect export

stats:
	$(PY) -m prospect stats

run:        ## pipeline complet
	$(PY) -m prospect run

demo:       ## test rapide sur 300 établissements
	$(PY) -m prospect run --limite 300
