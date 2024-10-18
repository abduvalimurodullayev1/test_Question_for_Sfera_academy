from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

db_url = 'postgresql+psycopg2://postgres:root123@localhost:5432/test_question'

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, autoincrement=True, primary_key=True)
    full_name = Column(String(length=150))
    phone_number = Column(String(length=150), unique=True)
    school = Column(String(length=150))
    class_s = Column(String(length=150))
    region = Column(String(length=150))
    test_results = relationship("TestResult", back_populates="user")

    @classmethod
    def get_by_user_id(cls, user_id):
        with get_db() as session:
            return session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def add_user(cls, full_name, phone_number, region, school, class_s):
        with SessionLocal() as session:
            try:
                new_user = cls(
                    full_name=full_name,
                    phone_number=phone_number,
                    region=region,
                    school=school,
                    class_s=class_s
                )
                session.add(new_user)
                session.commit()
                return new_user
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding User: {e}")
                return None

    @classmethod
    def all_user(cls):
        with get_db() as session:
            try:
                return session.query(cls).all()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching all users: {e}")
                return []


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(length=150))
    tests = relationship("Test_Question", back_populates="category")

    @classmethod
    def all_categories(cls):
        with get_db() as session:
            try:
                return session.query(cls).all()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching all categories: {e}")
                return []

    @classmethod
    def add_category(cls, title):
        with get_db() as session:
            try:
                new_category = cls(title=title)
                session.add(new_category)
                session.commit()
                return new_category
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding Category: {e}")
                return None


class Test_Question(Base):
    __tablename__ = 'Test_Question'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    question = Column(String(length=150))
    a_variant = Column(String(length=150))
    b_variant = Column(String(length=150))
    c_variant = Column(String(length=150))
    correct_answer = Column(Integer)
    name = Column(String(length=150))

    category = relationship("Category", back_populates="tests")

    def all_Test(self):
        tests = session.query(Test_Question).all()
        return tests

    def delete_test_savol(self, test_id):
        test = session.query(Test_Question).get(test_id)
        session.delete(test)
        session.commit()
        return test

    @classmethod
    def add_test(cls, category, question, a_variant, b_variant, c_variant, correct_answer):
        with get_db() as session:
            try:
                new_test = cls(category_id=category, question=question, a_variant=a_variant,
                               b_variant=b_variant, c_variant=c_variant, correct_answer=correct_answer)
                session.add(new_test)
                session.commit()
                return new_test
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding Test_Question: {e}")
                return None

    @classmethod
    def get_tests_by_category(cls, category_id):
        with get_db() as session:
            try:
                return session.query(cls).filter_by(category_id=category_id).all()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching tests by category: {e}")
                return []

    @classmethod
    def get_correct_option(cls, poll_id):
        with get_db() as session:
            try:
                test = session.query(cls).filter_by(id=poll_id).first()
                if test:
                    return test.correct_answer
                else:
                    return None
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching correct option for poll_id {poll_id}: {e}")
                return None


class Commentary(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(150))


class TestResult(Base):
    __tablename__ = 'test_re'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    correct = Column(Integer, nullable=False)
    incorrect = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    user = relationship("User", back_populates="test_results")

    def save(self):
        session.add(self)
        session.commit()

    @classmethod
    def get_all_results(cls):
        return session.query(cls).all()


Base.metadata.create_all(engine)


class Category_2(Base):
    __tablename__ = 'category_2'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(length=150))
    tests = relationship("Image_test", back_populates="category")

    @classmethod
    def all_categories(cls):
        with get_db() as session:
            try:
                return session.query(cls).all()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching all categories: {e}")
                return []

    @classmethod
    def add_category(cls, title):
        with get_db() as session:
            try:
                new_category = cls(title=title)
                session.add(new_category)
                session.commit()
                return new_category
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error adding Category: {e}")
                return None


Base.metadata.create_all(engine)


class Image_test(Base):
    __tablename__ = 'image_test'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_id = Column(Integer, ForeignKey('category_2.id'), nullable=False)
    test_image = Column(String(length=150))
    question = Column(String(length=150))
    a_variant = Column(String(length=150))
    b_variant = Column(String(length=150))
    c_variant = Column(String(length=150))
    correct_answer = Column(Integer)

    category = relationship("Category_2", back_populates="tests")

    def add_imagetest(self, category_id, test_image, question, a_variant, b_variant, c_variant, correct_answer):
        test = Image_test(category_id=category_id, test_image=test_image, question=question, a_variant=a_variant,
                          b_variant=b_variant, c_variant=c_variant, correct_answer=correct_answer)
        session.add(test)
        session.commit()
        return test

    @classmethod
    def get_tests_by_category(cls, category_id):
        with get_db() as session:
            try:
                return session.query(cls).filter_by(category_id=category_id).all()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error fetching tests by category: {e}")
                return []

    def all_imagetest(self):
        test = session.query(Image_test).all()
        return test

    # def add_test(self category_id, test_image, question, a_variant, b_variant, c_variant, correct_answer, session
    #
    # ):
    # try:
    #     new_test = (category_id=category_id, test_image=test_image, question=question, a_variant=a_variant,
    #     b_variant=b_variant, c_variant=c_variant, correct_answer=correct_answer)
    #     session.add(new_test)
    #     session.commit()
    #     return new_test
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     print(f"Error adding Image_test: {e}")
    #     return None


def delete_test_savol(self, test_id, session):
    test = session.query(Image_test).get(test_id)
    session.delete(test)
    session.commit()
    return test


Base.metadata.create_all(engine)

Base.metadata.create_all(engine)
