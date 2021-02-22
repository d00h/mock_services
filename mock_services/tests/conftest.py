import pytest
from faker import Faker

from redis import Redis
from mock_services.config import MockServicesConfig as confi
from mock_services.models import MockService, MockProfile

# from mock_services.api.app import create_app
# from mock_services.models.profile import ProfileStepRepository

# @pytest.fixture(scope="session")
# def app():
#     yield create_app()


@pytest.fixture(scope="class" )
def fake():
    yield Faker()


@pytest.fixture(scope="session")
def redis():
    yield Redis.from_url(confi.REDIS_URL)


@pytest.fixture()
def mock_service(redis) -> MockService:
    yield MockService(redis, expire=10)

# def profile_steps() -> profilesteprepository:
#     return none


# @pytest.fixture(scope='session')
# def config(app):
#     yield app.confi


# @pytest.fixture(scope="session")
# def db_engine(app):
#     """
#     Setup the database for a test session and drop all tables after the
#     session ends. It is not intended to be used on tests functions,
#     use `db_session` instead.
#     """
#     db = app.extensions["sqlalchemy"].db
#     with app.app_context():
#         yield db.engine
#         db.drop_all()


# @pytest.fixture()
# def db_session(app, db_engine, request):
#     """
#     Creates a new database transaction for the test and roll it back
#     when the test is completed
#     """
#     db = app.extensions["sqlalchemy"].db
#     connection = db_engine.connect()
#     transaction = connection.begin()
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#     db.session = session

#     def finalize():
#         db.session.close()
#         transaction.rollback()
#         connection.close()

#     request.addfinalizer(finalize)
#     return session


# @pytest.fixture
# def fake():
#     f = Faker()
#     return f
