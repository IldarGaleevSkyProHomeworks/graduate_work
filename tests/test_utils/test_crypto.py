from src.utils import crypto
from tests import testing_data


def test_decrypt_equal_encrypt():

    encrypted_data = crypto.encrypt(
        testing_data.STRING_TEST_DATA_1, testing_data.GENERATED_SECRET_KEY
    )

    decrypted_data = crypto.decrypt(encrypted_data, testing_data.GENERATED_SECRET_KEY)

    assert decrypted_data == testing_data.STRING_TEST_DATA_1
