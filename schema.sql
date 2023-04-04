---
--- SQLite3 Default Values
---

DELETE FROM users;
DELETE FROM weblist;
DELETE FROM budget;
DELETE FROM budgetitem;
DELETE FROM transactionitem;


INSERT INTO users (email,username,password) VALUES (
'admin@admin.adm','admin','$2b$12$25WY1X33QIGgm8UrjH.yHeOSRPAZOnZy60UDxf8PHnaQ2y.lpBJGe'
);

INSERT INTO weblist (name,value) VALUES ('Type','Income');
INSERT INTO weblist (name,value) VALUES ('Type','Expense');
INSERT INTO weblist (name,value) VALUES ('Category','Paycheck');
INSERT INTO weblist (name,value) VALUES ('Category','Rent');
INSERT INTO weblist (name,value) VALUES ('Category','Utilities');
INSERT INTO weblist (name,value) VALUES ('Category','Other');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Daily');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Weekly');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Bi-weekly');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Monthly');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Quarterly');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Bi-annually');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Yearly');
INSERT INTO weblist (name,value) VALUES ('Recurrence','Other');
INSERT INTO weblist (name,value) VALUES ('Currency','USD');
INSERT INTO weblist (name,value) VALUES ('Currency','EUR');
INSERT INTO weblist (name,value) VALUES ('Currency','JPY');

---
--- Sample Data
---

INSERT INTO budget (name,owner,currency,notes,incometotal,expensetotal,remainder) VALUES (
  'Default','user@user.usr','USD','Default Budget',0.0,0.0,0.0
);

INSERT INTO budgetitem (name,description,amount,budget,itemtype,category,recurrence,recurrence_day) VALUES (
  'Paycheck','TEST INCOME',4567.89,1,'Income','Paycheck','Monthly',1
);
INSERT INTO budgetitem (name,description,amount,budget,itemtype,category,recurrence,recurrence_day) VALUES (
  'Rent','TEST BILL',876.54,1,'Expense','Rent','Monthly',5
);