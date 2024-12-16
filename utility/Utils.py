
import random
import string


class Utils:

    @staticmethod
    def generate_id(prefix):
        N = 22
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))