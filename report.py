#!/usr/bin/python
#
# Informative summary from logs.

import psycopg2

DBNAME = "news"


def report():
    '''Main function which prints report.'''

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # 1. What are the most popular three articles of all time?
    c.execute("select title, count(*) as views from articles, log"
              " where concat('/article/', articles.slug)=log.path"
              " group by articles.title order by views desc limit 3")
    top_news = c.fetchall()

    print("1. The most popular three articles of all time:")
    for news in top_news:
        print(' * "{}" - {} views'.format(news[0], news[1]))

    print("")

    # 2. Who are the most popular article authors of all time?
    c.execute("select authors.name, sum(views) as views from"
              " (select author, count(*) as views from articles, log"
              " where concat('/article/',articles.slug)=log.path"
              " group by articles.slug, author) as article_views, authors"
              " where article_views.author=authors.id"
              " group by article_views.author, authors.name"
              " order by views desc")
    top_authors = c.fetchall()

    print("2. The most popular article authors of all time:")
    for author in top_authors:
        print(' * {} - {} views'.format(author[0], author[1]))

    print("")

    # 3. On which days more than 1% of requests lead to errors?
    c.execute("select date, rate from"
              " (select to_char(time, 'Mon DD, YYYY') as date,"
              " round("
              "cast(100*sum(case when status!='200 OK' then 1 else 0 end)"
              "::float/sum("
              "case when status='200 OK' then 1 else 0 end) as numeric), 1)"
              " as rate"
              " from log group by date) as err where rate>1")
    top_errors = c.fetchall()

    print("3. Days which more than 1% of requests lead to errors:")
    for day in top_errors:
        print(' * {} - {}%'.format(day[0], day[1]))

    db.close()

if __name__ == '__main__':
    report()
