TABLE ?= departments
PYTHON = python
CURDIR := $(shell pwd)

run:
	$(PYTHON) -m uvicorn main:app --reload

load-historical-data:
	$(PYTHON) app/load_data.py

backup:
ifeq ($(TABLE),)
	@echo "⚠️  Usage: make backup TABLE=table_name"
else
	$(PYTHON) -m app.exporters.backup_data $(TABLE)
endif

backup-all:
	$(PYTHON) -m app.exporters.backup_data all

restore:
ifndef TABLE
	@echo "Uso:"
	@echo "  make restore-all              # restaurar todas las tablas"
	@echo "  make restore TABLE=departments   # restaurar solo una tabla específica"
else
	python -m app.restore_data $(TABLE)
endif

restore-all:
	python -m app.restore_data departments
	python -m app.restore_data jobs
	python -m app.restore_data hired_employees

clean-data:
	PYTHONPATH=. python -m utils.clean_data

dashboard-create:
	PYTHONPATH=. streamlit run app/dashboard/hiring_dashboard.py

create-bash-files:
	PYTHONPATH=. python -m utils.generate_batches_data

# ---------- DOCKER COMMANDS ----------

docker-build:
	docker build -t data-migration-api .

docker-run:
	@if docker ps -a --format '{{.Names}}' | grep -Eq '^data-api$$'; then \
		echo "Removing existing container data-api..."; \
		docker rm -f data-api; \
	fi
	docker run -p 8000:8000 --name data-api -v "$(CURDIR):/app" data-migration-api


docker-run-shell:
	docker run -it --rm --entrypoint /bin/bash -v "$(CURDIR):/app" data-migration-api

docker-load-historical:
	docker exec data-api env PYTHONPATH=/app python app/load_data.py

docker-backup:
	docker exec data-api env PYTHONPATH=/app python -m app.backup_data $(TABLE)

docker-backup-all:
	docker exec data-api env PYTHONPATH=/app python -m app.backup_data all

docker-restore:
	docker exec data-api env PYTHONPATH=/app python -m app.restore_data $(TABLE)

docker-restore-all:
	docker exec data-api env PYTHONPATH=/app python -m app.restore_data departments
	docker exec data-api env PYTHONPATH=/app python -m app.restore_data jobs
	docker exec data-api env PYTHONPATH=/app python -m app.restore_data hired_employees

docker-inspect-db:
	docker run -it --rm \
		--entrypoint /bin/bash \
		-v "$(CURDIR):/app" \
		data-migration-api \
		-c "sqlite3 /app/app.db"

docker-clean-data:
	docker exec data-api env PYTHONPATH=/app python -m utils.clean_data

docker-dashboard:
	docker run -it --rm \
		-p 8501:8501 \
		--env PYTHONPATH=/app \
		-v $(CURDIR):/app \
		data-migration-api \
		streamlit run app/dashboard/hiring_dashboard.py --server.port 8501 --server.enableCORS false

docker-create-bash-files:
	docker exec -it data-api env PYTHONPATH=/app python -m utils.generate_batches_data




