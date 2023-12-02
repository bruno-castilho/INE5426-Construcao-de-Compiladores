
# INE5426-Construcao-de-Compiladores

#### Integrantes: 
- Bruno da Silva Castilho;
- Leonardo Seishi Yamazaki; 
- Rafael Francisco Réus; 
- Rafael Begnini de Castilhos.

### Makefile:
Foi definido a versão do Python em 3.10, pode ser que seja necessário alterar conforme a versão instalada em sua máquina.

Para executar programas de teste na análise léxica e sintática:

```
make run
```

Para executar programas de teste na análise léxica, sintática e semântica (com problemas nas regras semânticas) para visualizar o loop no terminal:

```
make semantic
```

Para limpar os arquivos de saída:

```
make clean
```

Caso desejar executar um programa de teste apenas:

```
python3 main.py --src data/program.lcc --semantic True/False
```