from app.utils import text_to_binary

def improved_sign_file(file_data, private_key, modulus, multiplier):
    """ Улучшенная функция подписи файла """
    binary_data = text_to_binary(file_data)
    chunks = [binary_data[i:i+len(private_key)] for i in range(0, len(binary_data), len(private_key))]

    signature = []
    for chunk in chunks:
        chunk_value = sum(private_key[i] for i, bit in enumerate(chunk) if bit == '1')
        signature.append(chunk_value)

    # Применяем множитель и модуль к каждому элементу подписи
    encrypted_signature = [x * multiplier % modulus for x in signature]
    return encrypted_signature

def improved_verify_signature(file_data, signature, public_key, modulus):
    """ Улучшенная функция проверки подписи """
    binary_data = text_to_binary(file_data)
    chunks = [binary_data[i:i+len(public_key)] for i in range(0, len(binary_data), len(public_key))]

    calculated_signature = []
    for chunk in chunks:
        chunk_value = sum(public_key[i] for i, bit in enumerate(chunk) if bit == '1')
        calculated_signature.append(chunk_value)

    # Сравниваем каждый элемент расшифрованной подписи с соответствующим элементом исходной подписи
    return all((chunk_value % modulus) == signature[i] for i, chunk_value in enumerate(calculated_signature))
