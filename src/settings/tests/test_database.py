from src.settings.database import create_database, get_db, engine


def test_create_database():
    create_database()
    expected_url = "sqlite:///./test.db"
    assert str(engine.url) == expected_url


def test_get_db():
    db = next(get_db())
    assert db is not None
