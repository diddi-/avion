create table airline (
    id integer primary key,
    created_at text DEFAULT CURRENT_TIMESTAMP,
    name varchar(100) not null unique,
    icao varchar(4),
    callsign varchar(100)
);

create table user_account (
    id integer primary key,
    created_at text default current_timestamp,
    firstname varchar(100) not null,
    lastname varchar(100) not null,
    email varchar(255) not null unique,
    username varchar(255) not null unique,
    password varchar(255) not null,
    salt varchar(255) not null
);
