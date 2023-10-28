import os

def get_last_downloaded_file(download_path):
    # Lista todos os arquivos no diretório
    list_of_files = [os.path.join(download_path, file) for file in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, file))]
    
    # Ordena os arquivos por data de modificação
    sorted_files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    
    # Retorna o arquivo mais recentemente modificado (ou seja, o último baixado)
    return sorted_files[0] if sorted_files else None