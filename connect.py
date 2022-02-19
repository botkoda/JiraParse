import cx_Oracle

def connect():
    try:
        conn = cx_Oracle.connect('un_stage/bibase@10.226.90.165/bi')
        print('Есть подключение')
    except:
        print('Нет подключения')
        exit(0)
    conn.close()
def main():

    
    total_pages = connect()

    pass


if __name__ == '__main__':
    main()