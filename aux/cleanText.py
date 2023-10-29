def clean_text(text):
    # Divide o texto em linhas
    lines = text.split('\n')
    
    # Mantém apenas as linhas que têm mais de um caractere
    cleaned_lines = [line.strip() for line in lines if (len(line.strip()) > 1 and line.strip()[0] != '<' and line.strip()[0] != '&')]
    
    # Combina as linhas limpas de volta em um texto
    cleaned_text = '\n'.join(cleaned_lines)
    
    return cleaned_text
