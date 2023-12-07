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

INSERT INTO users (id,email,username,password) VALUES (
  1,'admin@admin.adm','admin','$2b$12$25WY1X33QIGgm8UrjH.yHeOSRPAZOnZy60UDxf8PHnaQ2y.lpBJGe'
);

INSERT INTO budgets (id,name,currency,description) VALUES (
  1,'Default','EUR','Default'
);

INSERT INTO exchangerate (id,currency_from, currency_to, rate) VALUES (1,'EUR','USD',1.08);
INSERT INTO exchangerate (id,currency_from, currency_to, rate) VALUES (2,'USD','EUR',0.93);

INSERT INTO weblist (id,name,value) VALUES (1,'Category','Other');
INSERT INTO weblist (id,name,value) VALUES (2,'Category','Housing');
INSERT INTO weblist (id,name,value) VALUES (3,'Category','Electric');
INSERT INTO weblist (id,name,value) VALUES (4,'Category','Water');
INSERT INTO weblist (id,name,value) VALUES (5,'Category','Utilities');
INSERT INTO weblist (id,name,value) VALUES (6,'Category','Phone');
INSERT INTO weblist (id,name,value) VALUES (7,'Category','Internet');
INSERT INTO weblist (id,name,value) VALUES (8,'Category','Insurance');
INSERT INTO weblist (id,name,value) VALUES (9,'Category','Debt');
INSERT INTO weblist (id,name,value) VALUES (10,'Category','Credit');
INSERT INTO weblist (id,name,value) VALUES (11,'Category','Food');
INSERT INTO weblist (id,name,value) VALUES (12,'Category','Mobility');
INSERT INTO weblist (id,name,value) VALUES (13,'Category','Entertainment');
INSERT INTO weblist (id,name,value) VALUES (14,'Category','Income');
INSERT INTO weblist (id,name,value) VALUES (15,'Category','Expense');
INSERT INTO weblist (id,name,value) VALUES (16,'AccountType','Checking');
INSERT INTO weblist (id,name,value) VALUES (17,'AccountType','Savings');
INSERT INTO weblist (id,name,value) VALUES (18,'Currency','USD');
INSERT INTO weblist (id,name,value) VALUES (19,'Currency','EUR');
INSERT INTO weblist (id,name,value) VALUES (20,'Country','USA');
INSERT INTO weblist (id,name,value) VALUES (21,'Country','DE');

---
--- Sample Data
---

INSERT INTO accounts (id,name,accounttype,currency,country) VALUES (
  1,'SampleBank','Checking','EUR','DE'
);

INSERT INTO budgetitems (id,name,amount,description,category,budgetid,recurrence,recurrenceday) VALUES 
  (1,'Paycheck',4200.00,'Work income','Income',1,'Monthly',1),
  (2,'Rent',870.00,'Rent for apartment','Housing',1,'Monthly',1),
  (3,'Electric',205.00,'EnBW','Electric',1,'Monthly',1),
  (4,'Bahn Ticket',36.80,'Deutschland Ticket','Mobility',1,'Monthly',1),
  (5,'DSL',115.55,'Telekom','Internet',1,'Monthly',1),
  (6,'Mobile',90.19,'Telekom','Phone',1,'Monthly',1),
  (7,'Adam Reise',7.64,'Personal/Legal Insurance','Insurance',1,'Monthly',1),
  (8,'USAA Loan',125.00,'USAA Loan','Debt',1,'Monthly',15),
  (9,'USAA Insurance',22.00,'Renters Insurance','Insurance',1,'Monthly',15),
  (10,'USAA Credit',280.00,'USAA Credit Card','Credit',1,'Monthly',15),
  (11,'CHASE Credit',93.00,'CHASE Credit Card','Credit',1,'Monthly',15),
  (12,'MILSTAR Credit',186.00,'AAFES Star Card','Credit',1,'Monthly',1),
  (13,'GA Storage',48.00,'GA Non-Temp Storage','Utilities',1,'Monthly',1);

INSERT INTO transactions (id,datetimestamp,amount,convertedvalue,category,currency,name,description,accountid) VALUES 
  (1,'2023-01-01',4288.00,4288.00,'Income','EUR','Paycheck','Work Income',1),
  (2,'2023-01-01',870.00,870.00,'Housing','EUR','Rent','Transfer',1),
  (3,'2023-01-02',15.45,15.45,'Food','EUR','Fast Food','Fast Food',1),
  (4,'2023-01-03',49.99,46.49,'Shopping','USD','Online store','Online shopping',1),
  (5,'2023-01-04',25.15,25.15,'Shopping','EUR','Convenience','store',1);

