import streamlit as st
import os

from functions.ddl import create_tables, load_data, create_views
from functions.db import (
    get_genres, get_year_range, get_top_movies_by_genre_and_year,
    get_screening_times, get_monthly_sales, get_theaters_revenue,
    get_genre_ratings, get_all_genre_names_for_ratings,
    get_top_revenue_movies
)
from functions.plotly_utils import (
    plot_top_movies, plot_screening_times, plot_monthly_sales,
    plot_theaters_revenue, plot_genre_ratings, plot_top_revenue_movies
)

DATABASE_PATH = 'my.db'


def initialize_database():
    """
    Инициализация базы данных.
    Если файла БД нет, создаём и загружаем данные.
    Иначе предполагаем, что всё уже загружено.
    """
    if not os.path.exists(DATABASE_PATH):
        st.info("Создаём базу данных, так как файл не найден...")
        create_tables(DATABASE_PATH)
        load_data(DATABASE_PATH)
        create_views(DATABASE_PATH)
    else:
        st.info("Файл базы данных уже существует. Пропускаем создание/загрузку.")


def main():
    st.set_page_config(page_title="Аналитика фильмов и кинотеатров", layout="wide")
    st.title("🎬 Аналитика данных о фильмах и кинотеатрах")

    # Инициализируем базу данных (при первом запуске)
    initialize_database()

    # --- Боковая панель с фильтрами для разных графиков ---
    st.sidebar.header("Фильтры для графиков")

    # === 1. Фильтры для Топ фильмов по рейтингу ===
    st.sidebar.subheader("Топ фильмов по рейтингу")
    genres_list = get_genres(DATABASE_PATH)
    selected_genre = st.sidebar.selectbox("Жанр", genres_list)
    
    years = get_year_range(DATABASE_PATH)
    min_year, max_year = int(years["min_year"]), int(years["max_year"])
    selected_year_range = st.sidebar.slider(
        "Годы выпуска (Топ фильмов)",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    top_n_movies = st.sidebar.slider("Топ-N фильмов", 5, 20, 10)

    # === 2. Фильтры для Распределения сеансов по времени суток ===
    st.sidebar.subheader("Распределение сеансов по времени")
    hour_range = st.sidebar.slider("Диапазон часов", 0, 23, (0, 23))

    # === 3. Фильтры для Динамики продаж по месяцам ===
    st.sidebar.subheader("Динамика продаж по месяцам")
    month_range = st.sidebar.slider("Диапазон месяцев", 1, 12, (1, 12))

    # === 4. Фильтры для Сравнения кинотеатров по выручке ===
    st.sidebar.subheader("Сравнение кинотеатров")
    top_n_theaters = st.sidebar.slider("Топ-N кинотеатров", 1, 20, 5)

    # === 5. Фильтры для Сравнения жанров по рейтингам ===
    st.sidebar.subheader("Сравнение жанров по рейтингам")
    all_genre_names = get_all_genre_names_for_ratings(DATABASE_PATH)
    selected_genre_names = st.sidebar.multiselect(
        "Выберите жанры (оставьте пустым, чтобы взять все)",
        all_genre_names
    )

    # === 6. Фильтры для Топ фильмов по выручке ===
    st.sidebar.subheader("Топ фильмов по выручке")
    # Перепользуем диапазон лет (min_year, max_year) — но сделаем отдельный слайдер,
    # потому что, возможно, хотим другой диапазон для этого графика.
    selected_year_range_revenue = st.sidebar.slider(
        "Годы выпуска (Топ по выручке)",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    top_n_revenue_movies = st.sidebar.slider("Топ-N по выручке", 5, 20, 10)

    # --- ОСНОВНОЕ ОКНО: отрисовываем все графики с учётом фильтров ---

    # 1. Топ фильмов по рейтингу
    st.subheader(f"Топ-{top_n_movies} фильмов по рейтингу в жанре «{selected_genre}» ({selected_year_range[0]}–{selected_year_range[1]})")
    df_top_movies = get_top_movies_by_genre_and_year(
        genre=selected_genre,
        year_range=selected_year_range,
        top_n=top_n_movies,
        database_path=DATABASE_PATH
    )
    fig1 = plot_top_movies(df_top_movies)
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Распределение сеансов по времени суток
    st.subheader("Распределение сеансов по времени суток")
    df_screening = get_screening_times(DATABASE_PATH, hour_range=hour_range)
    fig2 = plot_screening_times(df_screening)
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Динамика продаж по месяцам
    st.subheader("Динамика продаж по месяцам")
    df_monthly = get_monthly_sales(DATABASE_PATH, month_range=month_range)
    fig3 = plot_monthly_sales(df_monthly)
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Сравнение кинотеатров по выручке
    st.subheader("Сравнение кинотеатров по выручке")
    df_theaters = get_theaters_revenue(DATABASE_PATH, top_n=top_n_theaters)
    fig4 = plot_theaters_revenue(df_theaters)
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Сравнение жанров по рейтингам
    st.subheader("Сравнение жанров по рейтингам")
    df_genres = get_genre_ratings(DATABASE_PATH)

    # Если пользователь выбрал конкретные жанры, фильтруем
    if selected_genre_names:
        df_genres = df_genres[df_genres['genre_name'].isin(selected_genre_names)]

    fig5 = plot_genre_ratings(df_genres)
    st.plotly_chart(fig5, use_container_width=True)

    # 6. Топ фильмов по выручке
    st.subheader(f"Топ-{top_n_revenue_movies} фильмов по выручке ({selected_year_range_revenue[0]}–{selected_year_range_revenue[1]})")
    df_top_revenue = get_top_revenue_movies(
        year_range=selected_year_range_revenue,
        top_n=top_n_revenue_movies,
        database_path=DATABASE_PATH
    )
    fig6 = plot_top_revenue_movies(df_top_revenue)
    st.plotly_chart(fig6, use_container_width=True)


if __name__ == "__main__":
    main()
