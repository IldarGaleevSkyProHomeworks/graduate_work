from src.models import UserSecret


GENERATED_SECRET_ID = "test_id_{0}"
GENERATED_SECRET_KEY = "FakeSecret"
STRING_TEST_DATA_1 = "TestBinaryData1"

BINARY_TEST_DATA_1 = f"{STRING_TEST_DATA_1}__{GENERATED_SECRET_KEY}".encode("utf-8")

USER_SECRET_TEST_DATA_1 = UserSecret(
    data=BINARY_TEST_DATA_1,
)
