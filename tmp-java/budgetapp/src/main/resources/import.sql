--- SQL IMPORT

INSERT INTO userentity (id, email, username, password) VALUES
(1, 'admin@admin.adm', 'admin', 'admin')
ON CONFLICT DO NOTHING;

INSERT INTO budgetentity (id, name, description, currency, userid) VALUES
(1, 'Default', 'Default Budget', 'EUR', 1)
ON CONFLICT DO NOTHING;

INSERT INTO budgetitementity (id, name, description, category, amount, currency, recurrence, recurrenceday, budgetid) VALUES
(1, 'Paycheck', 'Example Income', 'Income', 1234.56, 'EUR', 'Monthly', 1, 1),
(2, 'Rent', 'Example Expense', 'Housing', 543.21, 'USD', 'Monthly', 5, 1)
ON CONFLICT DO NOTHING;

INSERT INTO accountentity (id, name, description, accounttype, currency, userid) VALUES
(1, 'Example Account', 'Example bank account', 'checking', 'EUR', 1)
ON CONFLICT DO NOTHING;

INSERT INTO transactionentity (id, datetimestamp, amount, convertedamount, name, description, category, currency, accountid) VALUES
(1, '20240101 01:23:45', 1111.11, 1111.11, 'Paycheck', 'Example Paycheck', 'Income', 'EUR', 1),
(2, '20240203 09:08:07', 543.21, 543.21, 'Rent', 'Example Rent payment', 'Housing', 'EUR', 1)
ON CONFLICT DO NOTHING;

--- END