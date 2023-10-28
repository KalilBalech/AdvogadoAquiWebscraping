
def create_txt_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)