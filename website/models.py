from website import mysql

class Models:
    def __init__(self, query):
        self.query = query
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()

    def select(self):
        self.cursor.execute(self.query)
        row_headers = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()

        json_data = []
        for data in result:
            json_data.append(dict(zip(row_headers, data)))
    
        return json_data

    def query_sql(self, values):
        self.cursor.execute(self.query, values)
        self.conn.commit()
        self.cursor.close()

    def query_sql_multiple(self, values):
        self.cursor.executemany(self.query, values)
        self.conn.commit()
        self.cursor.close()

    def query_delete_all(self):
        self.cursor.execute(self.query)
        self.conn.commit()
        self.cursor.close()