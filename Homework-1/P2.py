# Problem 2 from Problem Set 1 of ECE464 - Databases

from sqlalchemy import create_engine
engine = create_engine(
    "mysql+pymysql://colin:watermelon@localhost:3306/sailors", echo = True)
connection = engine.connect()
# print(connection.execute("SELECT * from sailors").fetchall())

# GETTING TABLES, MAKE SESSION, IMPORTS 
# The majority of setting up the ORM was with the help of Professor Sokolov's sailors example ORM
# https://github.com/eugsokolov/ece464-databases/blob/master/sailors/sailors.py
# <--------------------------------------------------------------------------------------->
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, desc, select, distinct
from sqlalchemy.orm import backref, relationship, sessionmaker

session = sessionmaker(bind=engine)
s = session()
Base = declarative_base()

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
# <--------------------------------------------------------------------------------------->

##### Showing that the ORM is fully functional with tests #####


# Show that ORM queries match expected SQL queries through random tests
class Testclass:
    # Skipped testing a few of the question for time sake and my sanity

    # Question 1: List, for every boat, the number of times it has been reserved, excluding
    # those boats that have never been reserved
    def test_one_Q1(self):
        sql = "SELECT B.bid, B.bname, COUNT(*) as numReserve FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY B.bid HAVING numReserve > 0;"
        sqlResult = connection.execute(sql)
        sqlOutput = []
        for i in sqlResult:
            sqlOutput.append(i)

        orm = s.query(Reservation.bid, Boat.bname, func.count(Reservation.bid)).filter(Reservation.bid == Boat.bid).group_by(Reservation.bid, Boat.bname)
        # orm = s.query(Reservation.bid, func.count("*")).group_by(Reservation.bid).having(func.count("*") > 0)
        ormOutput = []
        for i in orm:
            ormOutput.append(i)

        assert sqlOutput == ormOutput

    # Question 2: List those sailors who have reserved every red boat (list their id and the name)
    def test_two_Q2(self):
        sql = "SELECT S.sname, S.sid FROM sailors S WHERE NOT EXISTS ( SELECT B.bid FROM boats B WHERE B.color='red' AND NOT EXISTS (SELECT * FROM reserves R WHERE R.bid = B.bid AND R.sid = S.sid))"
        sqlResult = connection.execute(sql)
        sqlOutput = []
        for i in sqlResult:
            sqlOutput.append(i)

        redBoats = s.query(Boat.bid).filter(Boat.color == "red")
        numRedBoats = redBoats.count()
        orm = s.query(Sailor.sid, Sailor.sname).filter(Reservation.bid.in_(redBoats)).filter(Reservation.sid == Sailor.sid).group_by(Reservation.sid).having(func.count(distinct(Reservation.bid)) == numRedBoats)
        ormOutput = []
        for i in orm:
            ormOutput.append(i)

    # Question 4: For which boat has the most reservations?
    def test_three_Q4(self):
        sql = "SELECT B.bname, B.bid, COUNT(*) as numReserve FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY B.bid ORDER BY numReserve DESC LIMIT 1;"
        sqlResult = connection.execute(sql)
        sqlOutput = []
        for i in sqlResult:
            sqlOutput.append(i)
        orm = s.query(Boat.bname, Reservation.bid, func.count(Reservation.bid)).filter(Boat.bid == Reservation.bid).group_by(Reservation.bid).limit(1)
        ormOutput = []
        for i in orm:
            ormOutput.append(i)

    # Question 5: Select all sailors who have never reserved a red boat
    def test_four_Q5(self):
        sql = "SELECT S.sid, S.sname FROM sailors as S WHERE S.sid NOT IN (SELECT R.sid FROM reserves as R INNER JOIN boats as B ON R.bid = B.bid WHERE B.color = 'red');"
        sqlResult = connection.execute(sql)
        sqlOutput = []
        for i in sqlResult:
            sqlOutput.append(i)
        redBoats = s.query(Boat.bid).filter(Boat.color == "red")
        orm = s.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(s.query(Reservation.sid).filter(Reservation.bid.in_(redBoats))))
        ormOutput = []
        for i in orm:
            ormOutput.append(i)

    # Question 6: Find the average age of sailors with a rating of 10
    def test_five_Q6(self):
        sql = "SELECT AVG(S.age) FROM sailors S WHERE S.rating = 10;"
        sqlResult = connection.execute(sql)
        sqlOutput = []
        for i in sqlResult:
            sqlOutput.append(i)
        orm = s.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).all()
        ormOutput = []
        for i in orm:
            ormOutput.append(i)
    



# Show that results from sql queries match orm queries

#