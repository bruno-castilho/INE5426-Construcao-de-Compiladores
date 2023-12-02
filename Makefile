SHELL := /bin/bash
PYTHON = python3.10

program_1=input/program1.lcc
program_2=input/program2.lcc
program_3=input/program3.lcc


.PHONY:
install:
	@$(PYTHON) -m pip install -r requirements.txt;

.PHONY:
run:
	@echo -e "Criando pasta output/ "
	@mkdir -p output/
	@echo -e "EXECUTANDO PROGRAMAS DE TESTE COM ANÁLISE LÉXICA E SINTÁTICA"

	@echo -e "Executando main program1.lcc"
	@$(PYTHON) main.py --src ${program_1} > output/program1.txt

	@echo -e "Executando main program2.lcc"
	@$(PYTHON) main.py --src ${program_2} > output/program2.txt

	@echo -e "Executando main program3.lcc"
	@$(PYTHON) main.py --src ${program_3} > output/program3.txt

	@echo -e "Concluido! Outputs de execucao foram salvos no diretorio 'output'"

.PHONY:
semantic:
	@echo -e "Criando pasta output/ "
	@mkdir -p output/
	@echo -e "EXECUTANDO PROGRAMAS DE TESTE COM ANÁLISE LÉXICA, SINTÁTICA E SEMÂNTICA"

	@echo -e "Executando main program1.lcc"
	@$(PYTHON) main.py --src ${program_1} --semantic True > output/program1.txt

	@echo -e "Executando main program2.lcc"
	@$(PYTHON) main.py --src ${program_2} --semantic True > output/program2.txt

	@echo -e "Executando main program3.lcc"
	@$(PYTHON) main.py --src ${program_3} --semantic True > output/program3.txt

	@echo -e "Concluido! Outputs de execucao foram salvos no diretorio 'output'"

.PHONY:
clean:
	@echo -e "Limpando diretorio output"
	@rm -r  -f output/*