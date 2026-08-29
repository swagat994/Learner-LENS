from src.database.client import get_database


def get_users_collection():
    return get_database()["users"]


def get_documents_collection():
    return get_database()["documents"]


def get_courses_collection():
    return get_database()["courses"]


def get_chats_collection():
    return get_database()["chats"]


def get_quizzes_collection():
    return get_database()["quizzes"]


def get_flashcards_collection():
    return get_database()["flashcards"]


def get_study_plans_collection():
    return get_database()["study_plans"]