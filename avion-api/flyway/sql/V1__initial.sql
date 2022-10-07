create table airline (
    id integer primary key,
    profile_id integer not null,
    created_at text DEFAULT CURRENT_TIMESTAMP,
    name varchar(100) not null unique,
    foreign key(profile_id) references profile(id)
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

create table profile (
    id integer primary key,
    user_account_id integer not null,
    created_at text default current_timestamp,
    firstname varchar(100) not null,
    lastname varchar(100) not null,
    foreign key(user_account_id) references user_account(id)
)
