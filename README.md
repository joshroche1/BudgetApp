# BudgetApp
App for monthly budgeting.
===
# Directory Tree 

### src/main/java
- /entity
- - Transaction.java (String source[bank], Date datetime, double value, String description, String category, String memo)
- - Budget.java (String name, int duedate[1...31], double value, String description, String category, String memo)
- - User.java (String email, String password, String phone)
- /session
- - AuthorizationFilter.java
- - SessionUtil.java
- - Login.java
- /datasource
- - DBUtil.java
### src/main/resources/META-INF/
- persistence.xml
- datasource.xml ?where does this go?
### src/main/webapp/
- /WEB-INF
- - web.xml
- ?faces-config.xml?
- /templates
- - template-main.xhtml
- /resources
- - /css/w3.css
- index.xhtml
- login.xhtml
- main.xhtml
pom.xml

SQLite3
===
# budgetapp.db
### CREATE TABLE Transaction (
source TEXT,
datetime TEXT,
value REAL,
description TEXT,
category TEXT,
memo TEXT
);
### CREATE TABLE Budget (
name TEXT,
duedate INTEGER,
value REAL,
description TEXT,
category TEXT,
memo TEXT
);
### CREATE TABLE Users (
email TEXT,
password TEXT,
phone TEXT
);
