create table theaters(
    theater_id integer primary key,
    theater_name varchar,
    theater_address varchar
);

create table genres(
    genre_id integer primary key,
    genre_name varchar
);


create table movies(
    movie_id integer primary key,
    movie_title varchar,
    release_year integer,
    genre_id integer,
    imdb_rating float,
    rotten_tomatoes integer,
    metacritic_rating float,
    foreign key (genre_id) references genres(genre_id)
);

create table screenings(
    screening_date date,
    theater_id integer,
    movie_id integer,
    screening_time time,
    tickets_sold integer,
    revenue integer,
    primary key (screening_date, theater_id, movie_id),
    foreign key (theater_id) references theaters(theater_id),
    foreign key (movie_id) references movies(movie_id)
);

