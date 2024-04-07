def search(name: str, connection):
    sql=f"select * from users where pseudonym='{name.strip()}' or ip='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows if rows else None