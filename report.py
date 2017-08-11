#!/usr/bin/env python
#
# Informative summary from logs.

import psycopg2

DBNAME = "news"


def print_top_articles():
    """What are the most popular three articles of all time?"""

    print("1. The most popular three articles of all time:")

    top_news = get_query_results(
              "select title, count(*) as views from articles, log"
              " where concat('/article/', articles.slug)=log.path"
              " group by articles.title order by views desc limit 3")

    for news in top_news:
        print(' * "{}" - {} views'.format(news[0], news[1]))


def print_top_authors():
    """Who are the most popular article authors of all time?"""

    print("2. The most popular article authors of all time:")

    top_authors = get_query_results(
              "select authors.name, sum(views) as views from"
              " (select author, count(*) as views from articles, log"
              " where concat('/article/',articles.slug)=log.path"
              " group by articles.slug, author) as article_views, authors"
              " where article_views.author=authors.id"
              " group by article_views.author, authors.name"
              " order by views desc")

    for author in top_authors:
        print(' * {} - {} views'.format(author[0], author[1]))


def print_top_error_days():
    """On which days more than 1% of requests lead to errors?"""

    print("3. Days which more than 1% of requests lead to errors:")

    top_errors = get_query_results(
              "select date, rate from"
              " (select to_char(time, 'Mon DD, YYYY') as date,"
              " round("
              "cast(100*sum(case when status!='200 OK' then 1 else 0 end)"
              "::float/sum("
              "case when status='200 OK' then 1 else 0 end) as numeric), 1)"
              " as rate"
              " from log group by date) as err where rate>1")

    for day in top_errors:
        print(' * {} - {}%'.format(day[0], day[1]))


def connect(database_name):
    """Connect to the PostgreSQL database. Returns a database connection."""

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def get_query_results(query):
    """Executes query and returns result"""

    db, c = connect(DBNAME)
    c.execute(query)
    results = c.fetchall()
    db.commit()
    db.close()

    return results


if __name__ == '__main__':
    print_top_articles()
    print("")
    print_top_authors()
    print("")
    print_top_error_days()
