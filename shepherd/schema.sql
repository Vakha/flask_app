DROP TABLE IF EXISTS labyak;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_status;

CREATE TABLE labyak
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL,
    age  INTEGER NOT NULL,
    sex  INTEGER NOT NULL CHECK (sex = 0 OR sex = 1) -- 0 - female, 1 - male
);

CREATE TABLE orders
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_id     INTEGER   NOT NULL,
    day             INTEGER   NOT NULL CHECK (day >= 0),
    milk_requested  REAL      NOT NULL CHECK (milk_requested >= 0),
    skins_requested INTEGER   NOT NULL CHECK (skins_requested >= 0),
    milk_allocated  REAL      NOT NULL CHECK (milk_allocated >= 0),
    skins_allocated INTEGER   NOT NULL CHECK (skins_allocated >= 0),
    status          INTEGER   NOT NULL REFERENCES order_status (id)
);

CREATE TABLE order_status
(
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO order_status (id, name)
VALUES (1, 'succeeded'),
       (2, 'partially_succeeded'),
       (3, 'fail');