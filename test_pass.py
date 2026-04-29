import psycopg2

passwords = ['admin', 'root', '123456', '1234', 'password', 'postgres', 'admin123', 'admin1234', 'nexos']
for p in passwords:
    try:
        psycopg2.connect(dbname='nexos_db', user='postgres', password=p, host='localhost', port='5432')
        print(f'Success with password: {p}')
        break
    except Exception as e:
        pass
