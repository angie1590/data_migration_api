.PHONY: backup backup-all

backup:
ifndef TABLE
	@echo "Use:"
	@echo "  make backup-all                       # respaldo completo"
	@echo "  make backup TABLE=departments        # respaldo solo de una tabla"
else
	python -m app.exporters.backup_data $(TABLE)

endif
backup-all:
	python -m app.exporters.backup_data all

restore:
ifndef TABLE
	@echo "Use:"
	@echo "  make restore-all              # restaurar todas las tablas"
	@echo "  make restore TABLE=departments   # restaurar solo una tabla específica"
else
	python -m app.exporters.restore_data $(TABLE)
endif

restore-all:
	python -m app.exporters.restore_data departments
	python -m app.exporters.restore_data jobs
	python -m app.exporters.restore_data hired_employees
