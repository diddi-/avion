create table airline (
    id integer primary key,
    created_at text DEFAULT CURRENT_TIMESTAMP,
    name varchar(100) not null unique,
    icao varchar(4),
    callsign varchar(100)
);
