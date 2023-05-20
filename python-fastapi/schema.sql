---
--- SQLite3 Default Values
---

DELETE FROM users;
DELETE FROM weblist;
DELETE FROM transactions;
DELETE FROM accounts;
DELETE FROM budgets;
DELETE FROM budgetitems;

INSERT INTO users (email,username,password) VALUES (
'admin@admin.adm','admin','$2b$12$25WY1X33QIGgm8UrjH.yHeOSRPAZOnZy60UDxf8PHnaQ2y.lpBJGe'
);

INSERT INTO budgets (name,description) VALUES (
  'Default Budget','Default'
);

INSERT INTO weblist (name,value) VALUES ('Category','Default');
INSERT INTO weblist (name,value) VALUES ('Category','Income');
INSERT INTO weblist (name,value) VALUES ('Category','Expense');
INSERT INTO weblist (name,value) VALUES ('Category','Other');
INSERT INTO weblist (name,value) VALUES ('AccountType','Checking');
INSERT INTO weblist (name,value) VALUES ('AccountType','Savings');
INSERT INTO weblist (name,value) VALUES ('Currency','USD');
INSERT INTO weblist (name,value) VALUES ('Currency','EUR');
INSERT INTO weblist (name,value) VALUES ('Country','USA');
INSERT INTO weblist (name,value) VALUES ('Country','DE');

---
--- Sample Data
---

INSERT INTO transactions (datetimestamp,amount,category,name,description,accountid) VALUES (
  '20230101 00:00:00',1234.56,'Income','Paycheck','Work Income',1
);

INSERT INTO accounts (name,accounttype,currency,iban,bic,country) VALUES (
  'SampleBank','Checking','EUR','DE00000000000000','BICBICBIC','DE'
);

INSERT INTO budgetitems (name,amount,description,category,budgetid,recurrence,recurrenceday) VALUES (
  'Income',123.45,'Work income','Income',1,'Monthly',1
);
