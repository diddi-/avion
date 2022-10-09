create table company (
    id integer primary key,
    profile_id integer not null,
    created_at text DEFAULT CURRENT_TIMESTAMP,
    name varchar(100) not null unique,
    balance int not null default 0,
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
    balance int not null default 0,
    foreign key(user_account_id) references user_account(id)
);

create table airport (
    id integer primary key,
    name varchar(200) not null,
    type varchar(50) not null,
    latitude_deg float,
    longitude_deg float,
    continent varchar(10),
    iso_country varchar(10),
    municipality varchar(200),
    gps_code varchar(10),
    iata_code varchar(10)
);


/* Search tool for models: https://www.icao.int/publications/DOC8643/Pages/Search.aspx */
create table aircraft_model (
    id integer primary key,
    created_at text default current_timestamp,
    manufacturer text not null,
    model text not null,
    icao_code varchar(10),
    engine_count integer not null default 1,
    engine_type varchar(100) not null,
    max_fuel integer not null default 0,
    empty_weight integer not null default 0,
    max_takeoff_weight integer not null default 0,
    max_passengers integer not null default 0,
    price integer not null default 0
);

create table company_aircraft (
    id integer primary key,
    company_id integer not null,
    aircraft_model_id integer not null,
    purchased_at text default current_timestamp,

    foreign key(company_id) references company(id),
    foreign key(aircraft_model_id) references aircraft_model(id)
);
