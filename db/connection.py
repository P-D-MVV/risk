import pyodbc

SERVER = '10.5.0.203\DWPROD'
DATABASE = 'mine_risk'
USERNAME = 'mine_risk_app'
PASSWORD = 'bX}9Kfx634UZ2'

def conectar():
    # connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Trusted_Connection=yes;'
    # conn = pyodbc.connect(connectionString)
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')

    return conn

def consultar_contador():
    conn = conectar()
    cursor = conn.cursor()

    try:
        consulta = cursor.execute("SELECT contadorAcessos, contadorSimulacoes FROM dbo.ContadoresAcesso")
        s1, s2 = consulta.fetchone()
    except:
        s1, s2 = "Nan", "NaN"
    finally:
        conn.close()
    return s1, s2

def incrementar_acesso():
    conn = conectar()
    cursor = conn.cursor()

    try:
        s_acesso, s_simulador = consultar_contador()
        s_acesso += 1
        consulta = cursor.execute(f"UPDATE dbo.ContadoresAcesso SET contadorAcessos={s_acesso} WHERE id=1")
        cursor.commit()
    except:
        pass
    finally:
        conn.close()

def incrementar_simulador():
    conn = conectar()
    cursor = conn.cursor()

    s_acesso, s_simulador = consultar_contador()
    s_simulador += 1
    consulta = cursor.execute(f"UPDATE dbo.ContadoresAcesso SET contadorSimulacoes={s_simulador} WHERE id=1")
    cursor.commit()

    conn.close()

