# file: plotly_utils.py
import plotly.express as px

def plot_top_movies(top_movies):
    """
    Гистограмма (горизонтальная): Топ фильмов по рейтингу combined_rating.
    
    Параметры:
        top_movies (pd.DataFrame): 
            Ожидается, что содержит колонки:
            - 'movie_title'
            - 'combined_rating'
            - 'release_year'
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    fig = px.bar(
        top_movies,
        x='combined_rating',
        y='movie_title',
        orientation='h',
        color='release_year',  # Для наглядности раскрашиваем по году
        labels={
            'combined_rating': 'Средний рейтинг',
            'movie_title': 'Фильм',
            'release_year': 'Год выпуска'
        },
        hover_data=['release_year', 'combined_rating'],  # Доп. поля в подсказках
        title='Топ фильмов по рейтингу'
    )
    # Дополнительное оформление - например, убираем фон и настраиваем сетку
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig


def plot_screening_times(screening_times):
    """
    Область: Распределение количества сеансов (total_screenings) по часам дня (hour).

    Параметры:
        screening_times (pd.DataFrame): 
            Ожидается, что содержит колонки:
            - 'hour'
            - 'total_screenings'
            - 'total_tickets_sold' (необязательно)
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    # Если хотите, можно добавить 'total_tickets_sold' в hover_data, 
    # если эта колонка точно есть в DataFrame:
    hover_cols = ['total_screenings']
    if 'total_tickets_sold' in screening_times.columns:
        hover_cols.append('total_tickets_sold')

    fig = px.area(
        screening_times,
        x='hour',
        y='total_screenings',
        labels={
            'hour': 'Час дня',
            'total_screenings': 'Количество сеансов'
        },
        hover_data=hover_cols,
        title='Распределение сеансов по времени суток'
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig


def plot_monthly_sales(monthly_sales):
    """
    Линейный график: Динамика продаж (выручка) по месяцам.
    
    Параметры:
        monthly_sales (pd.DataFrame):
            Ожидается, что содержит колонки:
            - 'month'
            - 'revenue'
            - 'tickets_sold' (необязательно)
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    hover_cols = ['revenue']
    if 'tickets_sold' in monthly_sales.columns:
        hover_cols.append('tickets_sold')

    fig = px.line(
        monthly_sales,
        x='month',
        y='revenue',
        labels={
            'month': 'Месяц',
            'revenue': 'Выручка'
        },
        hover_data=hover_cols,
        title='Динамика продаж по месяцам'
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig


def plot_theaters_revenue(theaters_revenue):
    """
    Круговая диаграмма: Распределение выручки по кинотеатрам.
    
    Параметры:
        theaters_revenue (pd.DataFrame):
            Ожидается, что содержит колонки:
            - 'theater_name'
            - 'total_revenue'
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    fig = px.pie(
        theaters_revenue,
        values='total_revenue',
        names='theater_name',
        labels={
            'total_revenue': 'Выручка',
            'theater_name': 'Кинотеатр'
        },
        title='Сравнение кинотеатров по выручке'
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig


def plot_genre_ratings(genre_ratings):
    """
    Гистограмма: Сравнение средних рейтингов (IMDB, RottenTomatoes, Metacritic) по разным жанрам.
    
    Параметры:
        genre_ratings (pd.DataFrame):
            Ожидается, что содержит колонки:
            - 'genre_name'
            - 'avg_imdb_rating'
            - 'avg_rotten_tomatoes'
            - 'avg_metacritic'
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    fig = px.bar(
        genre_ratings,
        x='genre_name',
        y=['avg_imdb_rating', 'avg_rotten_tomatoes', 'avg_metacritic'],
        barmode='group',
        labels={
            'genre_name': 'Жанр',
            'value': 'Рейтинг',
            'variable': 'Метрика'
        },
        title='Средние рейтинги по жанрам'
    )
    # Если нужно, можно донастроить всплывающие подсказки:
    # fig.update_traces(hovertemplate='Жанр=%{x}<br>%{y}')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig


def plot_top_revenue_movies(top_revenue_movies):
    """
    Горизонтальная гистограмма: Топ фильмов по выручке.
    
    Параметры:
        top_revenue_movies (pd.DataFrame):
            Ожидается, что содержит колонки:
            - 'movie_title'
            - 'revenue'
            - 'release_year'
            
    Возвращает:
        fig (plotly.graph_objs._figure.Figure): Фигура Plotly.
    """
    fig = px.bar(
        top_revenue_movies,
        x='revenue',
        y='movie_title',
        orientation='h',
        color='release_year',
        labels={
            'revenue': 'Выручка',
            'movie_title': 'Фильм',
            'release_year': 'Год выпуска'
        },
        hover_data=['release_year', 'revenue'],
        title='Топ фильмов по выручке'
    )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    return fig
