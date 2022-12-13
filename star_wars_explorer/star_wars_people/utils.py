from datetime import datetime


def create_file_name():
    file_name = datetime.now().strftime('%b.%d.%Y_%I.%M%p')
    return file_name
