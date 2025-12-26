import sys
import os

# Isso adiciona o diretório raiz do projeto ao caminho de busca do Python.
# Assim, o teste consegue encontrar a pasta "src".
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))