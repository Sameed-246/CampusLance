try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ModuleNotFoundError:
    # PyMySQL is optional during local development when the project is
    # configured to use SQLite instead of MySQL.
    pass