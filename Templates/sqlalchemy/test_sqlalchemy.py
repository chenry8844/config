#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------
# DESCRIPTION
# ===========
# test sqlalchemy
# ----------------------------------------

# build-in, 3rd party and my modules
import time
import os.path
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Boolean, and_, Table, desc, Date
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime


cur_file_path = os.path.realpath(__file__)
cur_dir_path = os.path.dirname(cur_file_path)
sqlite_db_path = os.path.join(cur_dir_path, "test.sqlite")
engine = create_engine("sqlite:///%s" % sqlite_db_path, echo=True)
Model = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()     # create a Session


class Person(Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True,
            autoincrement=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    is_man = Column(Boolean, nullable=False)
    score = Column(Integer)
    join_date = Column(Date, default=datetime.datetime.now().date())
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    #books = relationship("book")
    def __repr__(self):
        return "<Person('%s', '%s', '%s', '%s', '%s', '%s')>" % (
                self.name, self.is_man, self.score, self.join_date,
                self.created_at, self.updated_at)


class Book(Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    #owner = Column(Integer(unsigned=True), ForeignKey("person.id"),
    #        nullable=False)
    content = Column(String(255))


# ----------------------------------------
# test many to many
# ----------------------------------------
sentence_tag = Table("sentence_tag", Model.metadata,
    Column("sentence_id", Integer, ForeignKey("sentence.id")),
    Column("tag_id", Integer, ForeignKey("tag.id"))
)


class Sentence(Model):
    __tablename__ = "sentence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=False)
    tags = relationship("Tag", secondary=sentence_tag, backref="sentences")

    def _find_or_create_tag(self, tag_name):
        query = session.query(Tag).filter_by(name=tag_name)
        tag = query.first()
        if not tag:
            tag = Tag(name=tag_name)
        return tag

    def _get_tags(self):
        return [tag.name for tag in self.tags]

    def _set_tags(self, tag_names):
        # clear the list first
        while self.tags:
            del self.tags[0]
        # add new tag
        for tag_name in tag_names:
            self.tags.append(self._find_or_create_tag(tag_name))

    str_tags = property(_get_tags, _set_tags)

    def __repr__(self):
        return "id: %s, content: %s, tags: %s" % (self.id, self.content,
                self.str_tags)


class Tag(Model):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


def create_tables():
    Model.metadata.create_all(engine)


def insert_data():
    person = Person(name="zhongwei", is_man=True, score=100)
    session.add(person)
    session.commit()

    person = Person(name="zhongwei2", is_man=True, score=200)
    session.add(person)
    session.commit()

    person = Person(name="qq", is_man=True, score=200)
    session.add(person)
    session.commit()


def query_data():
    person = session.query(Person).filter_by(name="zhongwei").order_by(
            Person.created_at).first()
    print person
    print type(person.join_date)
    time.sleep(2)
    person.is_man = False
    session.commit()

    persons = session.query(Person).filter_by(name="zhongwei").order_by(
            desc(Person.created_at)).all()
    for person in persons:
        print person


def query_first():
    '''测试，当查询不到数据时，first() 的返回值

    结果：
    None
    '''
    person = session.query(Person).filter_by(name="zhongwei2").order_by(
            Person.created_at).first()
    print person


def query_all():
    '''测试，当查询不到数据时，all() 的返回值

    结果：
    []
    '''
    persons = session.query(Person).filter_by(name="zhongwei2").order_by(
            Person.created_at).all()
    print "query all with no data"
    print persons


def query_in():
    query = session.query(Person).filter(Person.name.in_(("zhongwei", "qq")))
    persons = query.all()
    print "query in"
    print persons


def short_query():
    '''测试，从长语句中提取公共的部分，以复用

    结果：
    完全可以，果然只在最后执行的时候才生成 SQL 语句
    '''
    print "define query"
    query = session.query(Person).filter_by(name="zhongwei")

    print "get one"
    zhongwei = query.filter_by(is_man=True).first()
    print zhongwei

    print "get some"
    persons = query.order_by(desc(Person.created_at)).limit(3).all()
    for person in persons:
        print person


def query_average():
    print "test query_average"
    avg = session.query(func.avg(Person.score))\
            .filter_by(name="zhongwei").first()[0]
    if avg is None:
        print "No result found!"
    else:
        print "avg is: %s" % (avg)


def query_average_by_group():
    print "test query_average_by_group"
    avg_by_name = session.query(Person.name, func.avg(Person.score))\
            .group_by(Person.name).all()
    print avg_by_name

    avg_by_name = session.query(Person.name, func.avg(Person.score))\
            .filter_by(is_man=False).group_by(Person.name).all()
    print avg_by_name

    avg_by_name = session.query(Person.name, func.sum(Person.score), func.count(Person.score))\
            .group_by(Person.name).all()
    print avg_by_name


def query_with_filter():
    print "test query_with_filter"
    persons = session.query(Person).filter(and_(Person.name=="zhongwei",
        Person.is_man==True)).all()
    for person in persons:
        print person

    persons = session.query(Person).filter(and_(Person.name=="zhongwei",
        Person.is_man==False)).all()
    for person in persons:
        print person


def test_many_to_many():
    sentence = Sentence(content="Hello world!")
    session.add(sentence)
    session.commit()

    sentence.str_tags = ["test", "test2"]
    session.commit()
    print sentence


def test_count():
    '''http://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query
    第一种方式有性能问题，推荐使用第二种
    '''
    print "test count"
    total = session.query(Person).count()
    print total

    total = session.query(func.count(Person.id)).first()[0]
    print total


def test_empty_field():
    new_book = Book(name="heart")
    session.add(new_book)
    session.commit()
    book = session.query(Book).first()
    print book.name, book.content


# ----------------------------------------
# test cases
# ----------------------------------------
def run_doctest():
    '''python -B <__file__> -v
    '''
    import doctest
    doctest.testmod()


if '__main__' == __name__:
    create_tables()
    #insert_data()
    #query_data()
    #query_average_by_group()
    #query_with_filter()
    #test_many_to_many()
    test_empty_field()


