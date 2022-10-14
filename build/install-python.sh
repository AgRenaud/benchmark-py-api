#!/bin/sh

install_pyenv() {
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
}

install_poetry() {
    POETRY_HOME="/etc/poetry"
    
    curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_HOME python3 -
}

install_pyenv
install_poetry