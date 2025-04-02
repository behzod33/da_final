import duckdb

def fetch_data(query, database_path='my.db'):
    """
    Выполняет SQL-запрос к базе данных DuckDB и возвращает результат в виде DataFrame.
    """
    con = duckdb.connect(database=database_path)
    df = con.execute(query).fetchdf()
    con.close()
    return df

def get_genres(database_path='my.db'):
    """
    Возвращает список жанров из представления movie_genre_ratings.
    """
    query = "SELECT DISTINCT genre_name FROM movie_genre_ratings ORDER BY genre_name"
    return fetch_data(query, database_path)['genre_name'].tolist()

def get_year_range(database_path='my.db'):
    """
    Возвращает минимальный и максимальный год выпуска (release_year) из movie_genre_ratings.
    """
    query = "SELECT MIN(release_year) as min_year, MAX(release_year) as max_year FROM movie_genre_ratings"
    row = fetch_data(query, database_path).iloc[0]
    return row 

def get_top_movies_by_genre_and_year(
    genre, year_range, top_n=10, min_rating=None, database_path='my.db'
):
    conditions = [
        f"genre_name = '{genre}'",
        f"release_year BETWEEN {year_range[0]} AND {year_range[1]}"
    ]
    
    if min_rating is not None:
        conditions.append(f"combined_rating >= {min_rating}")

    where_clause = " AND ".join(conditions)

    query = f"""
    SELECT movie_title, genre_name, release_year, combined_rating
    FROM movie_genre_ratings
    WHERE {where_clause}
    ORDER BY combined_rating DESC
    LIMIT {top_n}
    """
    return fetch_data(query, database_path)


def get_screening_times(database_path='my.db', hour_range=(0, 23)):
    """
    Возвращает данные о количестве сеансов из popular_screening_times.
    Дополнительно фильтруем по диапазону часов (hour_range).
    """
    query = f"""
    SELECT hour, total_screenings, total_tickets_sold
    FROM popular_screening_times
    WHERE hour BETWEEN {hour_range[0]} AND {hour_range[1]}
    ORDER BY hour
    """
    return fetch_data(query, database_path)

def get_monthly_sales(database_path='my.db', month_range=(1, 12)):
    query = f"""
    SELECT 
        EXTRACT('month' FROM month) AS month_val,
        SUM(revenue) AS revenue, 
        SUM(tickets_sold) AS tickets_sold
    FROM monthly_movie_performance
    WHERE EXTRACT('month' FROM month) BETWEEN {month_range[0]} AND {month_range[1]}
    GROUP BY EXTRACT('month' FROM month)
    ORDER BY month_val
    """
    df = fetch_data(query, database_path)
    df.rename(columns={"month_val": "month"}, inplace=True)
    return df


def get_theaters_revenue(database_path='my.db', top_n=5):
    """
    Возвращает выручку кинотеатров (theater_sales_analysis) – топ-N по убыванию.
    """
    query = f"""
    SELECT theater_name, total_revenue
    FROM theater_sales_analysis
    ORDER BY total_revenue DESC
    LIMIT {top_n}
    """
    return fetch_data(query, database_path)

def get_genre_ratings(database_path='my.db'):
    """
    Возвращает усреднённые рейтинги по жанрам (genre_performance_analysis).
    """
    query = """
    SELECT genre_name, avg_imdb_rating, avg_rotten_tomatoes, avg_metacritic
    FROM genre_performance_analysis
    ORDER BY revenue_rank
    """
    return fetch_data(query, database_path)

def get_all_genre_names_for_ratings(database_path='my.db'):
    """
    Возвращает список жанров, которые есть в genre_performance_analysis.
    """
    query = "SELECT DISTINCT genre_name FROM genre_performance_analysis ORDER BY genre_name"
    return fetch_data(query, database_path)['genre_name'].tolist()

def get_top_revenue_movies(year_range=None, top_n=10, database_path='my.db'):
    """
    Возвращает топ-N фильмов по выручке, 
    с возможностью фильтра по диапазону годов выпуска.
    """
    # Чтобы сделать выборку по годам, можно добавить условие release_year BETWEEN ...
    where_clause = ""
    if year_range is not None:
        where_clause = f"WHERE m.release_year BETWEEN {year_range[0]} AND {year_range[1]}"

    query = f"""
    SELECT 
        m.movie_title, 
        g.genre_name, 
        m.release_year, 
        SUM(s.revenue) as revenue
    FROM screenings s
    JOIN movies m ON s.movie_id = m.movie_id
    JOIN genres g ON m.genre_id = g.genre_id
    {where_clause}
    GROUP BY m.movie_title, g.genre_name, m.release_year
    ORDER BY revenue DESC
    LIMIT {top_n}
    """
    return fetch_data(query, database_path)
