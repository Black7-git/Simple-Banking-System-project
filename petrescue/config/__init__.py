try:
    import pymysql  # type: ignore

    pymysql.install_as_MySQLdb()
except Exception:
    # PyMySQL is optional when using SQLite; ignore if unavailable
    pass

