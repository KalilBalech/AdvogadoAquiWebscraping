
def remove_digits(number_str):
    if len(number_str) != 20:
        raise ValueError("A entrada deve ter exatamente 20 dígitos.")

    # Remover o décimo quarto, décimo quinto e décimo sexto dígitos
    return number_str[:13] + number_str[16:]
