import time , logging , os.path 
import psycopg2
import pandas as pd
logging.basicConfig(format="%(asctime)s  %(filename)s %(levelname)s,%(message)s",filename=os.path.join(os.getcwd(),'log.log'),level=logging.INFO)

def getData(id , start_date ,end_date):
    try :
        ip="192.168.31.121"
        with  psycopg2.connect(dbname='et_writer',user='pi',password='2doigxxi',host=ip,port=5432) as conn:
            with conn.cursor() as cur:
                sql =f"select  * from stock_date where id ='{id}' and date between to_date('{start_date}','YYYY-MM-DD') and to_date('{end_date}','YYYY-MM-DD') and id = '{id}' order by date asc"
                logging.info(f"sql:{sql}")
                print(f"sql:{sql}")
                df=pd.read_sql(sql,conn)
                logging.info(f"df:{df.head()}")
                return df
    except Exception as err:
        logging.error(f"getData error:{err}")
        print(err)  
    
    

    