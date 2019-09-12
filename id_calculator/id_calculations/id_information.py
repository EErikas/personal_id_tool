from .id_checker import get_int_list, get_birthday, check_personal_id


def get_personal_description(id_code):
    id_code_as_int_list = get_int_list(id_code)
    if check_personal_id(id_code_as_int_list):
        gender = 'Male' if int(id_code[0]) % 2 == 1 else 'Female'
        return '{0} born on {1}'.format(gender, get_birthday(id_code_as_int_list))
    else:
        return 'Invalid code!'


def get_unique_values(all_values):
    return list(dict.fromkeys(all_values))


def get_digits_only(string):
    return ''.join(filter(lambda x: x.isdigit(), string))


def text_sanitizer(text, no_exceptions=False):
    words = text.replace('\n', ' ').split(' ')

    valid_ak = []
    invalid_ak = []

    for word in words:
        temp = get_digits_only(word)
        if len(temp) == 11:
            id_code = get_int_list(temp)
            if check_personal_id(id_code, no_exceptions):
                valid_ak.append(temp)
            else:
                invalid_ak.append(temp)

    return {
        'valid_ak': get_unique_values(valid_ak),
        'invalid_ak': get_unique_values(invalid_ak),
    }
