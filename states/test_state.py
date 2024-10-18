from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    phone_number = State()
    ism_familya = State()
    region = State()
    school = State()
    class_s = State()


class TestAddStates(StatesGroup):
    category = State()
    title = State()
    a_variant = State()
    b_variant = State()
    c_variant = State()
    correct_answer = State()


class DeleteTestStates(StatesGroup):
    id = State()


class DeleteCategoryStates(StatesGroup):
    id = State()


class CategoryStates(StatesGroup):
    title = State()


class QuestionAnswerStates(StatesGroup):
    title = State()
    description = State()


class CommentState(StatesGroup):
    waiting_for_comment = State()


class TestResultForm(StatesGroup):
    user_id = State()
    test_id = State()
    score = State()
    timestamp = State()


class ImageTestStates(StatesGroup):
    category = State()
    image_test = State()
    title = State()
    a_variant = State()
    b_variant = State()
    c_variant = State()
    correct_answer = State()


class Category2States(StatesGroup):
    title = State()