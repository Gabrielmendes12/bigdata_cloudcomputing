#!/bin/bash

echo "--- [PLANO FINAL] Iniciando startup.sh customizado ---"

# ETAPA DE DIAGNÓSTICO:
# Vamos listar todos os arquivos no diretório raiz. A saída disso nos dirá
# exatamente como o Azure vê sua estrutura de pastas.
echo "--- Estrutura de arquivos em /home/site/wwwroot: ---"
ls -lA /home/site/wwwroot
echo "----------------------------------------------------"

# ETAPA DE EXECUÇÃO:
# Agora, vamos iniciar o Gunicorn.
# Usaremos o --chdir para forçar o diretório de trabalho correto.
echo "--- Iniciando Gunicorn... ---"
gunicorn --chdir /home/site/wwwroot controle.wsgi:application --bind=0.0.0.0:8000