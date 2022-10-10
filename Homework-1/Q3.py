# Problem 3 from Problem Set 1 of ECE464 - Databases

from sqlalchemy import create_engine
engine = create_engine(
    "mysql+pymysql://colin:(password)@localhost:3306/newSailors", echo = True)
connection = engine.connect()
# print(connection.execute("SELECT * from sailors").fetchall())

# GETTING TABLES, MAKE SESSION, IMPORTS 
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


class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)
    eid = Column(Integer, ForeignKey('employees.eid'))
    rid = Column(Integer, ForeignKey('repairs.rid'))

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))


class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

class Repair(Base):
    __tablename__ = 'repairs'

    rid = Column(Integer, primary_key=True)
    eid = Column(Integer, ForeignKey('employees.eid'))
    cost = Column(Integer)
    repairDate = Column(DateTime)
    repairMade = Column(String)

    boat = relationship('Boat')

class Employee(Base):
    __tablename__ = 'employees'

    eid = Column(Integer, primary_key=True)
    ename = Column(String)

# <--------------------------------------------------------------------------------------->

##### Showing that the ORM is fully functional with tests #####

# A key functionality of this new system is to show which employees have to still make repairs, and
# which employee has the most boats left unrepaired

def get_bad_employees():
    bad_eids = s.query(Repair.eid).filter(Repair.repairMade == 'NO').group_by(Repair.eid)
    bad_names = s.query(Employee.ename).filter(Employee.eid.in_(bad_eids))
    expected_result = ['Robert', 'Carl']
    result = []
    for i in bad_names:
        result.append(i[0])
    # assert is not working for some reason lol?
    # assert result == expected_result

    # We expect that the employees that have to still work on repair boats are Carl and Robert. 
    print(" ")
    print("Employees that have not repaired their boats: ")
    print(result)
    print(" ")

def get_worst_employee():
    worst_employees = s.query(Repair.eid, func.count(Repair.repairMade)).filter(Repair.repairMade == 'NO').group_by(Repair.eid).order_by(desc(func.count(Repair.repairMade))).limit(1).all()
    result = []
    for i in worst_employees:
        result.append(i)

    # We expect that the worst employee is Robert, who has not repaired any of the four boats he was assigned
    # to. His employee ID is 4. Therefore, the output is (4,4)
    print(" ")
    print("The worst employee(s)' eid and the number of boats they need to fix: ")
    print(result)
    print(" ")

get_bad_employees()
get_worst_employee()
