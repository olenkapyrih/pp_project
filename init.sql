CREATE TABLE user (
    id int,
    is_admin boolean,
    firstname varchar(45),
    lastname varchar(45),
    email varchar(45),
    password varchar(45),
    phone varchar(12),
    PRIMARY KEY (id)
);
CREATE TABLE ordering(
    id int,
    quantity int,
    ordering_date date,
    status varchar(45),
    tour_id int,
    user_id int,
    PRIMARY KEY (id)
);
CREATE TABLE tour(
    id int,
    name varchar(45),
    price int,
    photoUrl varchar(2048),
    available boolean,
    PRIMARY KEY (id)
);