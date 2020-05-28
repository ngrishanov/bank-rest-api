CREATE TABLE accounts (
    num INTEGER PRIMARY KEY CONSTRAINT num_constraint CHECK (num > 0),
    amount INTEGER CONSTRAINT sum_constraint CHECK (amount >= 0) DEFAULT 0
);
