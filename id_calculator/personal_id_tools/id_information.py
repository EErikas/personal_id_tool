from .lithuanian_personal_ID_tools import LithuanianIDTools as lpid


def text_sanitizer(text, no_exceptions=False):
    def get_unique_values(all_values):
        return list(dict.fromkeys(all_values))

    def get_digits_only(string):
        return ''.join(filter(lambda x: x.isdigit(), string))

    words = text.replace('\n', ' ').split(' ')

    valid_ak = []
    invalid_ak = []

    for word in words:
        temp = get_digits_only(word)
        if len(temp) == 11:
            if lpid.is_id_valid(temp, no_exceptions):
                valid_ak.append(temp)
            else:
                invalid_ak.append(temp)

    return {
        'valid_ak': get_unique_values(valid_ak),
        'invalid_ak': get_unique_values(invalid_ak),
    }
