import mysql.connector
import pandas as pd
import pymysql
from sqlalchemy import create_engine
#PlaceRelationTypes  = preps
#PlaceTypes = place
class Connector():
    def __init__(self):
        self.mydb = mysql.connector.connect(
                        user="myuser",
                        password="mypass",
                        host="132.75.249.84",
                        port=3306,
                        database="yakutz")
        self.cursor = self.mydb.cursor()
        self.engine = create_engine(
            "mysql://myuser:mypass@132.75.249.84/yakutz")

    def update_rule_table(self,df):
        df = df.fillna('')
        mySql_insert_query = """INSERT INTO Rules (id, PlaceName, rule,Rule_text) 
                               VALUES (%s, %s, %s, %s) """
        records_to_insert = [(x[0],x[1],str(x[2]),x[3]) for x in df.values]
        self.cursor.executemany(mySql_insert_query, records_to_insert)
        self.mydb.commit()
        print(self.cursor.rowcount, "Record inserted successfully into Rules table")




    def get_PlaceRelationTypes(self):
        mySql_query =  " select * from  PlaceRelationTypes ;"
        self.cursor.execute(mySql_query)
        myresult = set(self.cursor.fetchall())
        return  set([x[2] for x in myresult])


    def get_PlaceTypes(self):
        mySql_query =  " select * from  PlaceTypes ;"
        self.cursor.execute(mySql_query)
        myresult = set(self.cursor.fetchall())
        return  set([x[1] for x in myresult])



if __name__ == '__main__':
    Connector().get_PlaceTypes()
