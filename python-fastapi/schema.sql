---
--- SQLite3 Default Values
---

DELETE FROM users;
DELETE FROM weblist;
DELETE FROM exchangerate;
DELETE FROM transactions;
DELETE FROM accounts;
DELETE FROM budgets;
DELETE FROM budgetitems;

INSERT INTO users (email,username,password) VALUES (
'admin@admin.adm','admin','$2b$12$25WY1X33QIGgm8UrjH.yHeOSRPAZOnZy60UDxf8PHnaQ2y.lpBJGe'
);

INSERT INTO budgets (name,currency,description) VALUES (
  'Default Budget','EUR','Default'
);

INSERT INTO exchangerate (currency_from, currency_to, rate) VALUES ('EUR','USD',1.08);
INSERT INTO exchangerate (currency_from, currency_to, rate) VALUES ('USD','EUR',0.93);

INSERT INTO weblist (name,value) VALUES ('Category','Other');
INSERT INTO weblist (name,value) VALUES ('Category','Housing');
INSERT INTO weblist (name,value) VALUES ('Category','Electric');
INSERT INTO weblist (name,value) VALUES ('Category','Water');
INSERT INTO weblist (name,value) VALUES ('Category','Utilities');
INSERT INTO weblist (name,value) VALUES ('Category','Phone');
INSERT INTO weblist (name,value) VALUES ('Category','Internet');
INSERT INTO weblist (name,value) VALUES ('Category','Insurance');
INSERT INTO weblist (name,value) VALUES ('Category','Debt');
INSERT INTO weblist (name,value) VALUES ('Category','Credit');
INSERT INTO weblist (name,value) VALUES ('Category','Food');
INSERT INTO weblist (name,value) VALUES ('Category','Mobility');
INSERT INTO weblist (name,value) VALUES ('Category','Entertainment');
INSERT INTO weblist (name,value) VALUES ('Category','Income');
INSERT INTO weblist (name,value) VALUES ('Category','Expense');
INSERT INTO weblist (name,value) VALUES ('AccountType','Checking');
INSERT INTO weblist (name,value) VALUES ('AccountType','Savings');
INSERT INTO weblist (name,value) VALUES ('Currency','USD');
INSERT INTO weblist (name,value) VALUES ('Currency','EUR');
INSERT INTO weblist (name,value) VALUES ('Country','USA');
INSERT INTO weblist (name,value) VALUES ('Country','DE');

---
--- Sample Data
---

INSERT INTO transactions (datetimestamp,amount,convertedvalue,category,currency,name,description,accountid) VALUES (
  '2023-01-01',5000.00,5000.00,'Income','EUR','Paycheck','Work Income',1
);

INSERT INTO accounts (name,accounttype,currency,iban,bic,country) VALUES (
  'SampleBank','Checking','EUR','DE00000000000000','BICBICBIC','DE'
);

INSERT INTO budgetitems (name,amount,description,category,budgetid,recurrence,recurrenceday) VALUES (
  'Income',5000.00,'Work income','Income',1,'Monthly',1
);
