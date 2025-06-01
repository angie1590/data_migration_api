.PHONY: backup backup-all


load-historical-data:
	python -m app.load_data

backup:
ifndef TABLE
	@echo "Use:"
	@echo "  make backup-all                       # respaldo completo"
	@echo "  make backup TABLE=departments        # respaldo solo de una tabla"
else
	python -m app.backup_data $(TABLE)

endif
backup-all:
	python -m app.backup_data all

restore:
ifndef TABLE
	@echo "Use:"
	@echo "  make restore-all              # restaurar todas las tablas"
	@echo "  make restore TABLE=departments   # restaurar solo una tabla específica"
else
	python -m app.restore_data $(TABLE)
endif

restore-all:
	python -m app.restore_data departments
	python -m app.restore_data jobs
	python -m app.restore_data hired_employees

