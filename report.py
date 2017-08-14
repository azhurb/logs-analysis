#!/usr/bin/env python
#
# Informative summary from logs.

import psycopg2

DBNAME = "news"


def print_top_articles():
    """What are the most popular three articles of all time?"""

    print("1. The most popular three articles of all time:")

    top_news = get_query_results(
                """
                SELECT title,
                       count(*) AS views
                FROM articles,
                     log
                WHERE concat('/article/', articles.slug)=log.path
                GROUP BY articles.title
                ORDER BY views DESC
                LIMIT 3
                """)

    for news in top_news:
        print(' * "{}" - {} views'.format(news[0], news[1]))


def print_top_authors():
    """Who are the most popular article authors of all time?"""

    print("2. The most popular article authors of all time:")

    top_authors = get_query_results(
                """
                SELECT authors.name,
                       sum(views) AS views
                FROM
                  (SELECT author,
                          count(*) AS views
                   FROM articles,
                        log
                   WHERE concat('/article/',articles.slug)
                        =log.path
                   GROUP BY articles.slug,
                            author) AS article_views,
                     authors
                WHERE article_views.author=authors.id
                GROUP BY article_views.author,
                         authors.name
                ORDER BY views DESC
                """)

    for author in top_authors:
        print(' * {} - {} views'.format(author[0], author[1]))


def print_top_error_days():
    """On which days more than 1% of requests lead to errors?"""

    print("3. Days which more than 1% of requests lead to errors:")

    top_errors = get_query_results(
                """
                SELECT date, rate
                FROM
                  (SELECT to_char(TIME, 'Mon DD, YYYY') AS date,
                          round(cast(100*sum(CASE
                                         WHEN status!='200 OK' THEN 1
                                         ELSE 0
                                     END)::float/sum(CASE
                                                 WHEN status='200 OK' THEN 1
                                                 ELSE 0
                                             END) AS numeric), 1) AS rate
                   FROM log
                   GROUP BY date) AS err
                WHERE rate>1
                """)

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
