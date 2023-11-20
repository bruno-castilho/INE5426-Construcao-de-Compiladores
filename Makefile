SHELL := /bin/bash


program_1=data/program1.lcc
program_2=data/program2.lcc
program_3=data/program3.lcc

.PHONY:
run:
	@echo -e "Criando pasta output/ "
	@mkdir -p output/
	@echo -e "EXECUTANDO PROGRAMAS DE TESTE"

	@echo -e "Executando main program1.lcc"
	@python3 main.py --src ${program_1} > output/program1.txt

	@echo -e "Executando main program2.lcc"
	@python3 main.py --src ${program_2} > output/program2.txt

	@echo -e "Executando main program3.lcc"
	@python3 main.py --src ${program_3} > output/program3.txt

	@echo -e "Concluido! Outputs de execucao foram salvos no diretorio 'output'"
.PHONY:
clean:
	@echo -e "Limpando diretorio output"
	@rm -r  -f output/*