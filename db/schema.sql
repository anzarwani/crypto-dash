-- Coins table
create table if not exists coins (
    coin_id varchar primary key,
    name varchar not null,
    symbol varchar not null,
    market_cap_rank int
);

-- Coin prices table
create table if not exists coin_prices (
    id serial primary key,
    coin_id varchar references coins(coin_id),
    timestamp timestamptz not null,
    price numeric,
    volume numeric,
    market_cap numeric
);

-- Alerts table
create table if not exists alerts (
    id serial primary key,
    coin_id varchar references coins(coin_id),
    timestamp timestamptz not null,
    price_change_pct numeric,
    alert_type varchar
);
