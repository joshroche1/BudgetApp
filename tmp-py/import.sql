---

DELETE FROM budgets;
DELETE FROM budgetitems;
DELETE FROM accounts;
DELETE FROM transactions;
DELETE FROM weblists;
DELETE FROM exchangerates;

INSERT INTO weblists (id, name, value) VALUES
(1, 'Category', 'Income'),
(2, 'Category', 'Expense'),
(3, 'Category', 'Other'),
(4, 'Category', 'Housing'),
(5, 'Category', 'Utility'),
(6, 'Category', 'Electric'),
(7, 'Category', 'Phone'),
(8, 'Category', 'Internet'),
(9, 'Category', 'Insurance'),
(10, 'Category', 'Credit'),
(11, 'Category', 'Debt'),
(12, 'Category', 'Food'),
(13, 'Category', 'Shopping'),
(14, 'Category', 'Entertainment'),
(15, 'Category', 'Mobility'),
(16, 'AccountType', 'Checking'),
(17, 'AccountType', 'Savings'),
(18, 'Country', 'USA'),
(19, 'Country', 'DE'),
(20, 'Currency', 'USD'),
(21, 'Currency', 'EUR');

INSERT INTO exchangerates (id, currency_from, currency_to, rate) VALUES
(1, 'EUR', 'USD', 1.08),
(2, 'USD', 'EUR', 0.93);

INSERT INTO budgets (id, name, description, currency, ownerid) VALUES
(1, 'Default', 'Default budget', 'EUR', 1);

INSERT INTO budgetitems (id, name, description, amount, category, budgetid) VALUES
(1, 'Income', 'Paycheck', 5000.00, 'Income', 1),
(2, 'Electric', 'EnBW', 210.00, 'Electric', 1),
(3, 'Housing', 'Rent Payment', 870.00, 'Housing', 1);

INSERT INTO accounts (id, name, description, currency, accounttype, ownerid) VALUES
(1, 'EU Bank', 'Bank in the EU', 'EUR', 'Checking', 1);

INSERT INTO transactions (id, datetimestamp, amount, convertedvalue, name, description, category, currency, accountid) VALUES
(1, '2020-01-01 00:00:00.00', 870.00, 870.00, 'Rent', 'Rental payment', 'Housing', 'EUR', 1),
(2, '2020-01-05 08:15:00.00', 207.00, 207.00, 'Electric', 'Electricity', 'Utility', 'EUR', 1),
(3, '2020-01-11 17:00:00.00', 112.22, 112.22, 'Clothes', 'Store', 'Shopping', 'EUR', 1),
(4, '2020-01-12 12:00:00.00', 89.95, 89.95, 'Groceries', 'Grocery Store', 'Food', 'EUR', 1),
(5, '2020-01-20 07:04:00.00', 25.12, 25.12, 'Concert', 'Cocnert Ticket', 'Entertainment', 'EUR', 1);
