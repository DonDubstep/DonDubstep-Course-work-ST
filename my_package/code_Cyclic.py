import random
from copy import copy
# длина блока кодирования
CHUNK_LENGTH = 4

def chars_to_bin(chars):
    """
    Преобразование символов в бинарный формат
    #ord - преобразование в int
    #bin - преобразование в 2сс
    #zfill - заполнение нулями
    """
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

def chunk_iterator(text_bin, chunk_size=CHUNK_LENGTH):
    """
    Поблочный вывод бинарных данных
    """
    for i in range(len(text_bin)):
        if not i % chunk_size:
            yield text_bin[i:i + chunk_size]

def set_errors(encoded):
    """
    Допустить ошибку в блоках бинарных данных
    """
    result = ''
    for chunk in chunk_iterator(encoded, CHUNK_LENGTH + 3):
        num_bit = random.randint(1, len(chunk))
        chunk = '{0}{1}{2}'.format(chunk[:num_bit - 1], int(chunk[num_bit - 1]) ^ 1, chunk[num_bit:])
        result += (chunk)
    return result


def get_diff_index_list(value_bin1, value_bin2):
    """
    Получить список индексов различающихся битов
    """
    diff_index_list = []
    for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
        if char_bin_items[0] != char_bin_items[1]:
            diff_index_list.append(index)
    return diff_index_list


def fact(n):
    if n == 1 or n == 0:
        return 1
    return n * fact(n-1)

def comb(n, k):
    return fact(n) / fact(n - k) / fact(k)

def division(code, g):
    part = code[:len(g)]
    for k in range(len(code) - len(g) + 1):
        part = del_zeros(part)
        if len(part) < len(g) and (k == (len(code) - len(g))):
            break
        if len(part) < len(g):
            part.append(code[k + len(g)])
            continue
        mod = []
        for i in range(1, len(g)):
            if part[i] == g[i]:
                mod.append(0)
            else:
                mod.append(1)
        if k != (len(code) - len(g)):
            mod.append(code[k + len(g)])
        part = copy(mod)
    return part

def encode_loop(source):
    text_bin = chars_to_bin(source)#получаем из исходных данных, str типа '01011... '
    result = ''

    for chunk_bin in chunk_iterator(text_bin, 4):#перебираем чанки
        code = [0 if i=='0' else 1 for i in chunk_bin]#chunk_bin преобразуем в list int типа [0,1,0,0,1 ...]
        zeros = [0 for i in range(3)]
        code.extend(zeros)
        g = [1, 0, 1, 1]
        mod = division(code, g)
        while len(mod) < len(g) - 1:
            mod.insert(0, 0)
        del code[4:]
        code.extend(mod)
        result += ''.join(['0' if i==0 else '1' for i in code])
    return result

def del_zeros(lst):
    for i in range(len(lst)):
        if lst[i] == 1:
            return lst[i:]
    return [0]

def decode_loop(encoded):
    sub_result = ''
    result = ''
    bin_result_unfixed = ''
    bin_result_fixed = ''

    fixed_encoded_list = []
    for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + 3):  #выделяем чанки из encoded 
        code = [0 if i=='0' else 1 for i in encoded_chunk]#encoded_chunk преобразуем в list int типа [0,1,0,0,1 ...]
        code_copy = copy(code)
        g = [1, 0, 1, 1]
        code = del_zeros(code)
        syndrom = code if len(code) < len(g) else del_zeros(division(code, g))
        
        syndrom_table = {'1': 6, '10': 5, '100': 4, '11': 3, '110': 2, '111': 1, '101': 0}
        
        bin_result_unfixed += ''.join(['0' if i==0 else '1' for i in code_copy[:4]])

        if syndrom != [0]:#исправляем по синдрому
            code_copy[syndrom_table[''.join(list(map(str, syndrom)))]] = (code_copy[syndrom_table[''.join(list(map(str, syndrom)))]] + 1) % 2

        current_chunk = ''.join(['0' if i==0 else '1' for i in code_copy[:4]])
        bin_result_fixed += current_chunk

        sub_result += current_chunk
        if len(sub_result) == 8:
            fixed_encoded_list.append(sub_result)#в конечный list добавляем данные(str) без циклического кода
            sub_result = ''


    for fixed_chunk in fixed_encoded_list:
        result += chr(int(fixed_chunk, 2))
    return result, bin_result_fixed, bin_result_unfixed


if __name__ == '__main__':
    source = input('Укажите текст для кодирования/декодирования:')
    print('Длина блока кодирования: {0}'.format(CHUNK_LENGTH))
    encoded = encode_loop(source)
    print('Закодированные данные: {0}'.format(encoded))
    decoded, bin_decoded, a = decode_loop(encoded)
    print('Результат декодирования BIN: {0}'.format(bin_decoded))
    print('Результат декодирования: {0}'.format(decoded))


    encoded_with_error = set_errors(encoded)
    print('Допускаем ошибки в закодированных данных: {0}'.format(encoded_with_error))
    diff_index_list = get_diff_index_list(encoded, encoded_with_error)
    print('Допущены ошибки в битах: {0}'.format(diff_index_list))

    decoded, bin_decoded_right, bin_decoded_wrong = decode_loop(encoded_with_error)

    print('Результат декодирования ошибочных данных без исправления ошибок BIN: {0}'.format(bin_decoded_wrong))
    print('Результат декодирования ошибочных данных с исправлением ошибок BIN: {0}'.format(bin_decoded_right))
    print('Результат декодирования ошибочных данных с исправлением ошибок: {0}'.format(decoded))
