---

INSERT INTO budgets (id, name, description, currency, ownerid) VALUES
(1, 'Default', 'Default budget', 'EUR', 1);

INSERT INTO budgetitems (id, name, description, amount, budgetid) VALUES
(1, 'Income', 'Paycheck', 5000.00, 1),
(2, 'Electric', 'Electric', 210.00, 1),
(3, 'Housing', 'Rent Payment', 870.00, 1);

INSERT INTO accounts (id, name, description, currency, ownerid) VALUES
(1, 'EU Bank', 'Bank in the EU', 'EUR', 1);

INSERT INTO transactions (id, datetimestamp, amount, convertedvalue, name, description, category, currency, accountid) VALUES
(1, '2020-01-01 00:00:00.00', 870.00, 870.00, 'Rent', 'Rental payment', 'Housing', 'EUR', 1),
(2, '2020-01-05 08:15:00.00', 207.00, 207.00, 'Electric', 'Electricity', 'Utilities', 'EUR', 1),
(3, '2020-01-11 17:00:00.00', 112.22, 112.22, 'Clothes', 'Store', 'Shopping', 'EUR', 1),
(4, '2020-01-12 12:00:00.00', 89.95, 89.95, 'Groceries', 'Grocery Store', 'Food', 'EUR', 1),
(5, '2020-01-20 07:04:00.00', 25.12, 25.12, 'Concert', 'Cocnert Ticket', 'Entertainment', 'EUR', 1);