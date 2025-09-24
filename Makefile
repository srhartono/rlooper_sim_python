# Makefile for rlooper_sim_python workflow
# Note: This is actually run by Python, not make

.PHONY: help setup clean run dry-run summary dag

help:
	@echo "Available commands:"
	@echo "  make setup    - Set up virtual environment and dependencies"
	@echo "  make run      - Run all simulations"
	@echo "  make dry-run  - Show what would be executed"
	@echo "  make summary  - Generate summary report"
	@echo "  make dag      - Generate workflow DAG visualization"
	@echo "  make clean    - Clean all outputs"

setup:
	python setup_venv.py

run:
	python run_workflow.py all

dry-run:
	python run_workflow.py dry-run

summary:
	python run_workflow.py summary

dag:
	python run_workflow.py dag

clean:
	python run_workflow.py clean