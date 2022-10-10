# Problem 2 from Problem Set 1 of ECE464 - Databases

# up to line  was taken from Professor Sokolov's sailors ORM
# used the code to step up a connection, a session so that changes can be made, a base to use for each
# class, and definition of classes (sailors, boats, reservations) to map to my sailor database
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+pymysql://colin:@localhost:3306/sailors", echo = True)
connection = engine.connect()

# print(connection.execute("SELECT * from sailors").fetchall())
set_trace()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime, PrimaryKeyConstraint, ForeignKey, 
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

session = sessionmaker(bind=engine)
s = session()