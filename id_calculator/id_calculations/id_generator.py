from random import randint
from .id_checker import get_checksum_number, check_personal_id


def split_digits(number, digits):
    return [int(foo) for foo in '{0:0{1}d}'.format(number, digits)]


def personal_id_generator(no_exceptions=False):
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
        generated_id.append(get_checksum_number(generated_id))
        # Return generated ID if it meets the requirements
        if check_personal_id(generated_id, no_exceptions):
            return ''.join([str(foo) for foo in generated_id])
