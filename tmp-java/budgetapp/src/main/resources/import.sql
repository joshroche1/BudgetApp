--- Example Data

DELETE FROM accountentity;
DELETE FROM budgetentity;
DELETE FROM budgetitementity;
DELETE FROM transactionentity;
DELETE FROM userentity;

INSERT INTO transactionentity (id, datetimestamp, name, category, amount, description, currency, accountid) VALUES
(1, '20240102 01:23:56', 'Example 1', 'Income', 1234.56, 'Example Transaction', 'EUR', 1),
(2, '20240203 09:08:07', 'Example 2', 'Expense', 543.21, 'Example 2', 'USD', 1);

INSERT INTO accountentity (id, name, description, currency, accounttype, userid) VALUES
(1, 'Default', 'Default account', 'EUR', 'checking', 1);

INSERT INTO budgetentity (id, name, description, currency, userid) VALUES
(1, 'Default', 'Default Budget', 'EUR', 1);

INSERT INTO budgetitementity (id, name, category, amount, description, recurrence, recurrenceday, budgetid) VALUES 
(1, 'Paycheck', 'Income', 1111.11, 'Income from Paycheck', 'Monthly', 1, 1),
(2, 'Bill', 'Expense', 500.00, 'Utility Bill', 'Monthly', 10, 1);

INSERT INTO userentity (id, username, password, role, email) VALUES
(1, 'admin', 'admin', 'admin', 'admin@admin.adm');

ALTER SEQUENCE accountentity_seq RESTART 2;
ALTER SEQUENCE budgetentity_seq RESTART 2;
ALTER SEQUENCE budgetitementity_seq RESTART 3;
ALTER SEQUENCE transactionentity_seq RESTART 3; 
ALTER SEQUENCE userentity_seq RESTART 2;