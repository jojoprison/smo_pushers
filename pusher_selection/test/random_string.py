import random
import string


def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for _ in range(str_size))


chars = string.ascii_letters + string.punctuation
size = 4

print(chars)
print('Random String of length 12 =', random_string_generator(size, chars))