# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from msilib.schema import tables
from itemadapter import ItemAdapter
import psycopg2



class MediamarkPipeline:

    def open_spider(self, spider):
        user        = "postgres"
        password    = "5500"
        host        = "localhost"
        database    = "mediamark"
        # port        = "5432"
        # schema      = "laptops"
        # table       = "products"

        # creamos la conexion a la base de datos
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )

        # creamos el cursor el cual va a ejecutar comandos
        self.cur = self.connection.cursor()

        # creamos el schema
        self.cur.execute("""
        CREATE SCHEMA IF NOT EXISTS laptops
        """)

        # creamos la tabla laptops
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS laptops.products(
            id SERIAL PRIMARY KEY,
            date_time TIMESTAMP,
            modelo TEXT,
            precio_anterior FLOAT,
            precio_actual FLOAT
        )
        """)

    def close_spider(self, spider):
        # cerramos el cursos y la conexion a la base de datos
        self.connection.commit()
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        # definimos el proceso para insertar los items
        item = ItemAdapter(item)
        insert_query = """INSERT INTO laptops.products (modelo, date_time, precio_anterior, precio_actual)
                        VALUES (%s, %s, %s, %s)"""
        to_insert = (item['modelo'], item['date_time'], item['precio_anterior'], item['precio_actual'])

        self.cur.execute(insert_query, to_insert)
        self.connection.commit()
        return item


