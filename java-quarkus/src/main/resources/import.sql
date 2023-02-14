INSERT INTO userentity(id, username, password, role, email) VALUES (nextval('hibernate_sequence'), 'admin', '$2a$10$bzT1n32kCsNlIGpJtDMgIO.C23cATmOHmjCA.III3ALGOjmEpU0yq', 'admin', 'admin@admin.adm');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'category', 'Default');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'category', 'Income');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'category', 'Expense');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'accounttype', 'Checking');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'accounttype', 'Savings');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'accounttype', 'Other');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'incometype', 'Paycheck');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'incometype', 'Dividend');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'incometype', 'Retirement');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'currency', '$');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'currency', '£');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'currency', '€');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'currency', '¥');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'USA');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'CAN');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'MEX');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'UK');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'DE');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'FR');
INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'country', 'JP');

INSERT INTO configentity(id, name, value) VALUES (nextval('hibernate_sequence'), 'systemcurrency', '€');

-- TEST DATA

INSERT INTO accountentity(id, name, number, iban, bic, type, address, city, state, country, api_credential, currency, telephone) VALUES (
  nextval('hibernate_sequence'),'Test Bank Account','1234567890','DE1234-567-890-1234567890','BIC123BIC','Checking','Strasseweg 999','Stadt','Landkries','DE','abcdABCD1234','€','+999-123-456-7890'
);

INSERT INTO billentity(id, name, amount, recurrence, date_occurence, paid, active) VALUES (
  nextval('hibernate_sequence'),'Test Rent','876.54','Monthly','1',true,true
);

INSERT INTO incomeentity(id, name, incometype, amount, recurrence, date_occurence, paid, active) VALUES (
  nextval('hibernate_sequence'),'Work','Paycheck','6543.21','Monthly','1',true,true
);

INSERT INTO transactionentity(id, datetimestamp, amount, name, description, category, reference) VALUES (
  nextval('hibernate_sequence'),'2023-01-01 00:00:00','98.76','Test Transaction','Testing transaction display','Default','1234567890'
);