import os

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Arquivo {filepath} excluído com sucesso!")
    else:
        print(f"Arquivo {filepath} não encontrado!")