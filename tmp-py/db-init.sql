---
--- SQLite3 Default Values
---

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS weblists;
DROP TABLE IF EXISTS exchangerates;
DROP TABLE IF EXISTS budgets;
DROP TABLE IF EXISTS budgetitems;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users(
  id INT PRIMARY KEY NOT NULL,
  email TEXT,
  username TEXT,
  password TEXT
);

CREATE TABLE weblists(
  id INT PRIMARY KEY NOT NULL,
  name TEXT,
  value TEXT
);

CREATE TABLE exchangerates(
  id INT PRIMARY KEY NOT NULL,
  currency_from TEXT,
  currency_to TEXT,
  rate FLOAT
);

CREATE TABLE budgets(
  id INT PRIMARY KEY NOT NULL,
  name TEXT,
  description TEXT,
  currency TEXT,
  ownerid INT  
);

CREATE TABLE budgetitems(
  id INT PRIMARY KEY NOT NULL,
  name TEXT,
  description TEXT,
  amount FLOAT,
  category TEXT,
  recurrence TEXT,
  duedate INT,
  budgetid INT
);

CREATE TABLE accounts(
  id INT PRIMARY KEY NOT NULL,
  name TEXT,
  description TEXT,
  accounttype TEXT,
  currency TEXT,
  ownerid INT
);

CREATE TABLE transactions(
  id INT PRIMARY KEY NOT NULL,
  datetimestamp TEXT,
  amount FLOAT,
  convertedvalue FLOAT,
  category TEXT,
  currency TEXT,
  name TEXT,
  description TEXT,
  accountid INT
);

INSERT INTO users (id, email, username, password) VALUES (
  1, 'admin', 'admin', '$2b$12$PzNX7cScDmw1jh.sjWKIMe2JyFOJmYCreOFB7TTlrueAIzT0jch/q'
);

INSERT INTO weblists (id, name, value) VALUES 
  (1, 'Category', 'Other'),
  (2, 'Category', 'Housing'),
  (3, 'Category', 'Electric'),
  (4, 'Category', 'Water'),
  (5, 'Category', 'Utilities'),
  (6, 'Category', 'Phone'),
  (7, 'Category', 'Internet'),
  (8, 'Category', 'Insurance'),
  (9, 'Category', 'Debt'),
  (10, 'Category', 'Credit'),
  (11, 'Category', 'Food'),
  (12, 'Category', 'Mobility'),
  (13, 'Category', 'Shopping'),
  (14, 'Category', 'Child Support'),
  (15, 'Category', 'Transfer'),
  (16, 'Category', 'Bills'),
  (17, 'Category', 'Income'),
  (18, 'Category', 'Expense'),
  (19, 'AccountType', 'Checking'),
  (20, 'AccountType', 'Savings'),
  (21, 'Currency', 'USD'),
  (22, 'Currency', 'EUR'),
  (23, 'Country', 'USA'),
  (24, 'Country', 'DE')
;

---
--- Sample Data
---

INSERT INTO budgets (id, name, description, currency, ownerid) VALUES (
  1, 'Default', 'Default Budget', 'EUR', 1
);

INSERT INTO budgetitems (id, name, description, amount, category, recurrence, duedate, budgetid) VALUES 
(1, 'Paycheck', 'Work paycheck', 4200.00, 'Income', 'Monthly', 1, 1),
(2, 'Rent', 'Apartment rent', 870.00, 'Housing', 'Monthly', 1, 1),
(3, 'Electric', 'EnBW', 205.00, 'Electric', 'Monthly', 1, 1),
(4, 'Mobile', 'Telekom Mobile', 95.00, 'Phone', 'Monthly', 15, 1),
(5, 'Internet', 'Telekom Festnetz', 105.00, 'Internet', 'Monthly', 15, 1),
(6, 'DBahn', 'DeutcheBahn ABOTicket', 95.00, 'Mobility', 'Monthly', 1, 1),
(7, 'USAA Insurance', 'Renters Insurance', 24.00, 'Insurance', 'Monthly', 15, 1),
(8, 'USAA Credit', 'Credit card', 250.00, 'Credit', 'Monthly', 1, 1),
(9, 'CHASE Credit', 'Credit card', 100.00, 'Credit', 'Monthly', 1, 1),
(10, 'MILSTAR', 'Credit card', 250.00, 'Credit', 'Monthly', 1, 1),
(11, 'Child Support', 'Child support', 2034.00, 'Child Support', 'Monthly', 1, 1),
(12, 'Storage Unit', 'Non-temp storage in GA', 47.00, 'Utilities', 'Monthly', 1, 1)
;

INSERT INTO exchangerates (id, currency_from, currency_to, rate) VALUES
(1, 'USA', 'DE', 0.93),
(2, 'DE', 'USA', 1.09);

INSERT INTO accounts (id, name, description, accounttype, currency, ownerid) VALUES 
(1, 'Default Account', 'Default Bank', 'Checking', 'EUR', 1);

INSERT INTO transactions (id, datetimestamp, amount, convertedvalue, category, currency, name, description, accountid) VALUES 
(1, '2020-01-01', 0.01, 0.01, 'Other', 'EUR', 'Test Transaction', 'Test transaction', 1);
