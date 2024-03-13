import secrets
import string

#funcion para generar un id de usuario aleatorio
def generate_user_id(length=30):
    #caracteres posibles para el id
    characters = string.ascii_letters + string.digits
    #generar el id aleatorio
    random_id = ''.join(secrets.choice(characters) for _ in range(length))

    return random_id
