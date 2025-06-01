.PHONY: backup backup-all

backup:
ifndef TABLE
	@echo "Uso:"
	@echo "  make backup-all                       # respaldo completo"
	@echo "  make backup TABLE=departments        # respaldo solo de una tabla"
else
	python -m app.exporters.backup_data $(TABLE)

endif
backup-all:
	python -m app.exporters.backup_data all

