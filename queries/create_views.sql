-- 1. Вьюшка с информацией о фильмах и их жанрах, включая средние рейтинги
create view movie_genre_ratings as
select 
    m.movie_id,
    m.movie_title,
    g.genre_name,
    m.release_year,
    round(m.imdb_rating, 1) as imdb_rating,
    m.rotten_tomatoes,
    round(m.metacritic_rating, 1) as metacritic_rating,
    round((m.imdb_rating * 10 + m.rotten_tomatoes + m.metacritic_rating) / 3, 1) as combined_rating,
    concat(cast(extract(year from current_date) as integer) - m.release_year, ' years ago') as years_since_release
from 
    movies m
join 
    genres g on m.genre_id = g.genre_id
order by 
    combined_rating desc;

-- 2. Вьюшка с анализом продаж по кинотеатрам (исправленная)
create view theater_sales_analysis as
select 
    t.theater_id,
    t.theater_name,
    upper(substring(split_part(t.theater_address, ',', 1), 1, 1)) || 
    lower(substring(split_part(t.theater_address, ',', 1), 2)) as city,
    count(distinct s.movie_id) as unique_movies_shown,
    sum(s.tickets_sold) as total_tickets_sold,
    sum(s.revenue) as total_revenue,
    round(sum(s.revenue) / sum(s.tickets_sold), 2) as avg_ticket_price,
    rank() over (order by sum(s.revenue) desc) as revenue_rank
from 
    screenings s
join 
    theaters t on s.theater_id = t.theater_id
group by 
    t.theater_id, t.theater_name, t.theater_address
order by 
    total_revenue desc;

-- 3. Вьюшка с ежемесячной статистикой по фильмам (исправленная)
create view monthly_movie_performance as
select 
    m.movie_id,
    m.movie_title,
    g.genre_name,
    date_trunc('month', s.screening_date) as month,
    extract(month from s.screening_date) as month_number,
    strftime(s.screening_date, '%b') as month_name,
    count(*) as screening_count,
    sum(s.tickets_sold) as tickets_sold,
    sum(s.revenue) as revenue,
    round(avg(s.tickets_sold), 1) as avg_tickets_per_screening,
    round(sum(s.tickets_sold) * 100.0 / sum(sum(s.tickets_sold)) over (partition by date_trunc('month', s.screening_date)), 1) as market_share_percentage,
    lag(sum(s.revenue), 1) over (partition by m.movie_id order by date_trunc('month', s.screening_date)) as prev_month_revenue
from 
    screenings s
join 
    movies m on s.movie_id = m.movie_id
join 
    genres g on m.genre_id = g.genre_id
group by 
    m.movie_id, m.movie_title, g.genre_name, date_trunc('month', s.screening_date), extract(month from s.screening_date), s.screening_date
order by 
    month, revenue desc;

-- 4. Вьюшка с популярными временами сеансов
create view popular_screening_times as
select 
    extract(hour from screening_time) as hour,
    count(*) as total_screenings,
    sum(tickets_sold) as total_tickets_sold,
    sum(revenue) as total_revenue,
    round(avg(tickets_sold), 1) as avg_tickets_per_screening,
    round(avg(revenue), 2) as avg_revenue_per_screening,
    rank() over (order by sum(tickets_sold) desc) as popularity_rank
from 
    screenings
group by 
    extract(hour from screening_time)
order by 
    hour;

-- 5. Вьюшка с анализом жанров
create view genre_performance_analysis as
with genre_stats as (
    select 
        g.genre_id,
        g.genre_name,
        count(distinct m.movie_id) as movie_count,
        round(avg(m.imdb_rating), 1) as avg_imdb_rating,
        round(avg(m.rotten_tomatoes), 1) as avg_rotten_tomatoes,
        round(avg(m.metacritic_rating), 1) as avg_metacritic
    from 
        genres g
    join 
        movies m on g.genre_id = m.genre_id
    group by 
        g.genre_id, g.genre_name
),
genre_sales as (
    select 
        g.genre_id,
        sum(s.tickets_sold) as total_tickets_sold,
        sum(s.revenue) as total_revenue,
        round(sum(s.revenue) / nullif(sum(s.tickets_sold), 0), 2) as avg_ticket_price
    from 
        screenings s
    join 
        movies m on s.movie_id = m.movie_id
    join 
        genres g on m.genre_id = g.genre_id
    group by 
        g.genre_id
)
select 
    gs.genre_id,
    gs.genre_name,
    gs.movie_count,
    gs.avg_imdb_rating,
    gs.avg_rotten_tomatoes,
    gs.avg_metacritic,
    gsa.total_tickets_sold,
    gsa.total_revenue,
    gsa.avg_ticket_price,
    rank() over (order by gsa.total_revenue desc) as revenue_rank,
    rank() over (order by gs.avg_imdb_rating desc) as rating_rank
from 
    genre_stats gs
join 
    genre_sales gsa on gs.genre_id = gsa.genre_id
order by 
    gsa.total_revenue desc;