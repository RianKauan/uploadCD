
cd /root/script/ || { echo "Falha ao entrar no diretório"; exit 1; }

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
pyenv activate backups || { echo "Falha ao ativar o ambiente Pyenv"; exit 1; }

#poetry install || { echo "Falha ao instalar dependências"; exit 1; }

python backups.py || { echo "Falha ao executar o script Python"; exit 1; }

echo "Script executado com sucesso!"
