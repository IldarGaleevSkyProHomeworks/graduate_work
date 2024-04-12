import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from src import models
from src.database import mongodb
from src.repository import UserSecret
from tests import testing_data


@pytest.fixture(scope="module")
async def fixture_init_database(fixture_override_settings):
    async with mongodb.get_db_connection(prop=fixture_override_settings) as db_conn:
        db_conn: AsyncIOMotorClient
        db: AsyncIOMotorDatabase = db_conn.get_database(
            fixture_override_settings.database.mongo_db_name
        )

        collection = db.get_collection(UserSecret.COLLECTION_NAME)

        # create test data

        test_secret_model = models.UserSecret(
            data=testing_data.BINARY_TEST_DATA_1,
        )

        test_item_id = await collection.insert_one(
            test_secret_model.model_dump(
                exclude_none=True,
            )
        )

        yield {
            "test_item_id": str(test_item_id.inserted_id),
        }

        # cleanup

        await db_conn.drop_database(fixture_override_settings.database.mongo_db_name)


@pytest.mark.repository
@pytest.mark.dependency()
async def test_get_item_by_id(fixture_override_settings, fixture_init_database):
    async with UserSecret(prop=fixture_override_settings) as repo:

        test_item_id = fixture_init_database["test_item_id"]

        item = await repo.get_item_by_id(test_item_id)

        assert item.data == testing_data.BINARY_TEST_DATA_1


@pytest.mark.repository
@pytest.mark.dependency(depends=["test_get_item_by_id"])
async def test_write_item(fixture_override_settings, fixture_init_database):
    async with UserSecret(prop=fixture_override_settings) as repo:

        inserted_item = await repo.write_item(testing_data.USER_SECRET_TEST_DATA_1)

        check_item = await repo.get_item_by_id(inserted_item.id)

        assert str(check_item.id) == inserted_item.id
        assert check_item.data == testing_data.BINARY_TEST_DATA_1


@pytest.mark.repository
@pytest.mark.dependency(depends=["test_get_item_by_id"])
async def test_delete_item(fixture_override_settings, fixture_init_database):
    async with UserSecret(prop=fixture_override_settings) as repo:

        test_item_id = fixture_init_database["test_item_id"]

        exist_item = await repo.get_item_by_id(test_item_id)

        deleted_item = await repo.delete_item(exist_item)

        not_exist_intem = await repo.get_item_by_id(test_item_id)

        assert exist_item.id == deleted_item.id
        assert not_exist_intem is None
