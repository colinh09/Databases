create table sailors(
    sid int PRIMARY KEY,
    sname varchar(30),
    rating int,
    age int
);

create table reserves(
    sid int,
    bid int,
    day date,
	PRIMARY KEY (sid, bid, day)
);

create table boats(
    bid int PRIMARY KEY,
	bname char(20),
	color char(10),
	length int
    eid int,
    rid int
);

create table repairs(
    rid int PRIMARY KEY,
    bid int,
    eid int,
    cost int,
    repairDate date,
    repairMade char(3),
)

create table employees(
    eid int PRIMARY KEY,
    ename varchar(30),
    bid int,
    rid int
)

insert into sailors values (22,'dusting',7,45);
insert into sailors values (29,'brutus',1,33);
insert into sailors values (31,'lubber',8,55);
insert into sailors values (32,'andy',8,25);
insert into sailors values (58,'rusty',10,35);
insert into sailors values (64,'horatio',7,16);
insert into sailors values (71,'zorba',10,35);
insert into sailors values (74,'horatio',9,25);
insert into sailors values (85,'art',3,25);
insert into sailors values (95,'bob',3,63);
insert into sailors values (23,'emilio',7,45);
insert into sailors values (24,'scruntus',1,33);
insert into sailors values (35,'figaro',8,55);
insert into sailors values (59,'stum',8,25);
insert into sailors values (60,'jit',10,35);
insert into sailors values (61,'ossola',7,16);
insert into sailors values (62,'shaun',10,35);
insert into sailors values (88,'dan',9,25);
insert into sailors values (89,'dye',3,25);
insert into sailors values (90,'vin',3,63);

insert into reserves values (23,104,'1998/10/10');
insert into reserves values (24,104,'1998/10/10');
insert into reserves values (35,104,'1998/8/10');
insert into reserves values (59,105,'1998/7/10');
insert into reserves values (23,105,'1998/11/10');
insert into reserves values (35,105,'1998/11/6');
insert into reserves values (59,106,'1998/11/12');
insert into reserves values (60,106,'1998/9/5');
insert into reserves values (60,106,'1998/9/8');
insert into reserves values (88,107,'1998/9/8');
insert into reserves values (89,108,'1998/10/10');
insert into reserves values (90,109,'1998/10/10');
insert into reserves values (89,109,'1998/8/10');
insert into reserves values (60,109,'1998/7/10');
insert into reserves values (59,109,'1998/11/10');
insert into reserves values (62,110,'1998/11/6');
insert into reserves values (88,110,'1998/11/12');
insert into reserves values (88,110,'1998/9/5');
insert into reserves values (88,111,'1998/9/8');
insert into reserves values (61,112,'1998/9/8');
insert into reserves values (22,101,'1998/10/10');
insert into reserves values (22,102,'1998/10/10');
insert into reserves values (22,103,'1998/8/10');
insert into reserves values (22,104,'1998/7/10');
insert into reserves values (31,102,'1998/11/10');
insert into reserves values (31,103,'1998/11/6');
insert into reserves values (31,104,'1998/11/12');
insert into reserves values (64,101,'1998/9/5');
insert into reserves values (64,102,'1998/9/8');
insert into reserves values (74,103,'1998/9/8');

insert into boats values (101,'Interlake','blue', 45, 7, 7);
insert into boats values (102,'Interlake','red', 45, 3, 12);
insert into boats values (103,'Clipper','green', 40, 5, 10);
insert into boats values (104,'Clipper','red', 40, 6, 13);
insert into boats values (105,'Marine','red', 35, 3, 6);
insert into boats values (106,'Marine','green', 35, 1, 3);
insert into boats values (107,'Marine','blue', 35, 1, 9);
insert into boats values (108,'Driftwood','red', 35, 6, 11);
insert into boats values (109,'Driftwood','blue', 35, 4, 2);
insert into boats values (110,'Klapser','red', 30, 4, 4);
insert into boats values (111,'Sooney','green', 28, 2, 5);
insert into boats values (112,'Sooney','red', 28, 4, 1, 4, 8);

insert into repairs value(1, 112, 4, 120, '2020/1/5', 'NO');
insert into repairs value(2, 109, 4, 130, '2020/1/6', 'NO');
insert into repairs value(3, 106, 1, 100, '2020/1/8', 'YES');
insert into repairs value(4, 110, 4, 150, '2020/1/10', 'NO');
insert into repairs value(5, 111, 2, 90, '2020/1/11', 'YES');
insert into repairs value(6, 105, 3, 190, '2020/1/15', 'YES');
insert into repairs value(7, 101, 7, 110, '2020/1/15', 'NO');
insert into repairs value(8, 112, 4, 200, '2020/1/18', 'NO');
insert into repairs value(9, 107, 1, 110, '2020/1/20', 'YES');
insert into repairs value(10, 103, 5, 90, '2020/1/23', 'NO');
insert into repairs value(11, 108, 6, 130, '2020/1/24', 'YES');
insert into repairs value(12, 102, 3, 120, '2020/1/26', 'YES');
insert into repairs value(13, 104, 6, 130, '2020/1/30', 'YES');

insert into employees value(1, 'Fred', 106, 3);
insert into employees value(2, 'Carl', 111, 5);
insert into employees value(3, 'Stanley', 101, 7);
insert into employees value(4, 'Robert', 112, 1);
insert into employees value(5, 'Carl', 103, 10);
insert into employees value(4, 'Robert', 109, 2);
insert into employees value(4, 'Robert', 104, 4);
insert into employees value(4, 'Robert', 110, 8);
insert into employees value(3, 'Stanley', 105, 6);
insert into employees value(1, 'Fred', 107, 9);
insert into employees value(6, 'Eugene', 108, 11);
insert into employees value(3, 'Stanley', 102, 12);
insert into employees value(6, 'Eugene', 104, 13);