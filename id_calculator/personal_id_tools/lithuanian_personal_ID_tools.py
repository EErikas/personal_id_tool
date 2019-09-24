from datetime import datetime
from random import randint


class LithuanianIDTools:
    # Public methods:
    @classmethod
    def is_id_valid(cls, id_sting, no_exceptions=False):
        return cls.__check_personal_id(cls.__get_int_list(id_sting), no_exceptions)

    @classmethod
    def personal_id_generator(cls, no_exceptions=False):
        def split_digits(number, digits):
            return [int(foo) for foo in '{0:0{1}d}'.format(number, digits)]

        # Run while correct code is generated:
        while True:
            # Generate first 10 numbers of personal ID:
            generated_id = [
                randint(1, 6),  # Gender and century number
                *split_digits(randint(0, 99), 2),  # Year
                *split_digits(randint(0, 12), 2),  # Month
                *split_digits(randint(0, 31), 2),  # Day
                *split_digits(randint(0, 999), 3),  # People born before
            ]
            # Calculate check number:
            generated_id.append(cls.__get_checksum_number(generated_id))
            # Return generated ID if it meets the requirements
            if cls.__check_personal_id(generated_id, no_exceptions):
                return ''.join([str(foo) for foo in generated_id])

    @classmethod
    def get_personal_description(cls, id_code):
        id_code_as_int_list = cls.__get_int_list(id_code)
        if cls.__check_personal_id(id_code_as_int_list):
            gender = 'Male' if int(id_code[0]) % 2 == 1 else 'Female'
            return '{0} born on {1}'.format(gender, cls.__get_birthday(id_code_as_int_list))
        else:
            return 'Invalid code!'

    # Private methods:
    @staticmethod
    def __get_int_list(personal_id_string):
        return [int(foo) for foo in personal_id_string]

    @staticmethod
    def __get_int_from_int_list(numbers):
        return numbers[0] * 10 + numbers[1]

    @staticmethod
    def __get_checksum_number(id_code):
        def get_sum_mod(id_code, values):
            return sum([foo * bar for foo, bar in zip(id_code[:10], values)]) % 11

        value_set_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
        value_set_2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]

        check_number = get_sum_mod(id_code, value_set_1)
        if check_number != 10:
            return check_number
        else:
            check_number = get_sum_mod(id_code, value_set_2)
            if check_number != 10:
                return check_number
            else:
                return 0

    @classmethod
    def __get_birthday(cls, id_date_data):
        century_code = id_date_data[0]
        year_code = cls.__get_int_from_int_list(id_date_data[1:3])
        month_code = cls.__get_int_from_int_list(id_date_data[3:5])
        day_code = cls.__get_int_from_int_list(id_date_data[5:7])

        century = 1800 if century_code <= 2 else 1900 if century_code <= 4 else 2000
        year = century + year_code
        if month_code == 0 or day_code == 0:
            return '{0}-{1}-{2}'.format(year,
                                        'N/A' if month_code == 0 else month_code,
                                        'N/A' if day_code == 0 else day_code)
        else:
            # Convert values to a date in order to check if date exists
            # this is especially helpful when working with leap years
            try:
                return datetime(year, month_code, day_code).strftime('%Y-%m-%d')
            except ValueError:
                return None

    @classmethod
    def __check_personal_id(cls, id_number, no_exceptions=False):
        month_code = cls.__get_int_from_int_list(id_number[3:5])
        day_code = cls.__get_int_from_int_list(id_number[5:7])
        # First digit can be from 1 to 6:
        is_first_digit_correct = int(id_number[0]) in range(1, 7)
        # Date digits must be in a right range
        # Note: there is an exception when a person cannot remember their month or day of birth
        # in such cases the corresponding digits are replaced by 0s
        # By default these exceptions are allowed, but can be disabled, therefore variable no_exceptions is used
        # Since it is a bool value it can be interpreted as 0 or 1 so it is used in range accordingly:
        # False means range starts from 0, True means it starts from 1
        is_date_format_correct = month_code in range(no_exceptions, 13) and day_code in range(no_exceptions, 32)

        is_date_correct = cls.__get_birthday(id_number[:7]) is not None
        is_check_number_correct = id_number[-1] == cls.__get_checksum_number(id_number)

        # Method returns True if all requirements are met:
        return is_first_digit_correct and is_date_format_correct and is_date_correct and is_check_number_correct
