--- SQLite3 Database Initialization

DELETE FROM budgets;
DELETE FROM budgetitems;
DELETE FROM accounts;
DELETE FROM transactions;
DELETE FROM weblists;
DELETE FROM exchangerates;
DELETE FROM users;

INSERT INTO weblists (id, name, value) VALUES 
(1, 'AccountType', 'Checking'),
(2, 'AccountType', 'Savings'),
(3, 'Country', 'USA'),
(4, 'Country', 'DE'),
(5, 'Currency', 'USD'),
(6, 'Currency', 'EUR'),
(7, 'Category', 'Income'),
(8, 'Category', 'Expense'),
(9, 'Category', 'Housing'),
(10, 'Category', 'Electric'),
(11, 'Category', 'Water'),
(12, 'Category', 'Utilities'),
(13, 'Category', 'Phone'),
(14, 'Category', 'Internet'),
(15, 'Category', 'Insurance'),
(16, 'Category', 'Debt'),
(17, 'Category', 'Credit'),
(18, 'Category', 'Food'),
(19, 'Category', 'Mobility'),
(20, 'Category', 'Entertainment'),
(21, 'Category', 'Shopping'),
(22, 'Category', 'Transfer'),
(23, 'Category', 'Bill')
;

INSERT INTO users (id, username, email, password) VALUES 
(1, 'admin', 'admin@admin.adm', '$2b$12$.G6mRohd2n058/2Om6XG4uFKvLRMp5JzQG8/XVUVwEKclKdAbpZDC');

INSERT INTO budgets (id, name, description, currency, ownerid) VALUES 
(1, 'Default', 'Default Budget', 'EUR', 1);

INSERT INTO budgetitems (id, name, description, amount, category, recurrence, duedate, budgetid) VALUES 
(1, 'Paycheck', 'Work', 4200.00, 'Income', 'Monthly', 1, 1),
(2, 'Rent', 'Apartment Rent', 870.00, 'Housing', 'Monthly', 1, 1),
(3, 'Electric', 'EnBW', 205.00, 'Electric', 'Monthly', 1, 1),
(4, 'Mobile', 'Telekom Mobile', 95.0, 'Phone', 'Monthly', 15, 1),
(5, 'Internet', 'Telekom Festnetz', 105.0, 'Internet', 'Monthly', 15, 1),
(6, 'Train Ticket', 'DeutscheBahn Aboticket', 95.0, 'Mobility', 'Monthly', 1, 1),
(7, 'Loan', 'Bank Loan', 134.0, 'Debt', 'Monthly', 15, 1),
(8, 'Insurance', 'Renters Insurance', 24.0, 'Insurance', 'Monthly', 15, 1),
(9, 'Credit Card', 'Credit Card bills', 600.0, 'Credit', 'Monthly', 1, 1),
(10, 'Storage Unit', 'Storage Unit', 47.0, 'Utilities', 'Monthly', 1, 1)
;

INSERT INTO accounts (id, name, description, accounttype, currency, ownerid) VALUES 
(1, 'KSBB', 'Kriessparkasse Boeblingen', 'Checking', 'EUR', 1);

INSERT INTO exchangerates (id, currency_from, currency_to, rate) VALUES 
(1, 'USA', 'DE', 0.93),
(2, 'DE', 'USA', 1.09)
;

INSERT INTO transactions (id, datetimestamp, amount, convertedvalue, category, currency, name, description, accountid) VALUES 
(1, '2024-01-01', 0.01, 0.01, 'Other', 'EUR', 'Test', 'Test Transaction', 1);
