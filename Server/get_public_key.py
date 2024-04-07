def get_public_key(name: str, connection)->str:
    sql=f"select public_key from users where pseudonym='{name.strip()}' or ip='{name.strip()}';"
    cursor=connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    return rows[0][0]