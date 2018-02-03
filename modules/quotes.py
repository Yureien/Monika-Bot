import psycopg2
import os
from urllib import parse
from random import randint


class Quotes:
    def __init__(self):
        try:
            parse.uses_netloc.append("postgres")
            url = parse.urlparse(os.environ["DATABASE_URL"])
            self.conn = psycopg2.connect(database=url.path[1:], user=url.username,
                                         password=url.password, host=url.hostname, port=url.port)
        except KeyError:
            self.conn = psycopg2.connect(database="testdb", user="postgres",
                                         password="postgrespass", host="127.0.0.1", port="5432")
        self.cursor = self.conn.cursor()
        print("New table created: ", self.__createTable())

    def __createTable(self):
        self.cursor.execute("""select exists(
select * from information_schema.tables where table_name='quotes')""")
        if self.cursor.fetchone()[0]:
            return False
        else:
            command_create_table = """
            CREATE TABLE QUOTES
            (id BIGSERIAL PRIMARY KEY NOT NULL,
            cid BIGINT NOT NULL,
            mid BIGINT NOT NULL,
            qid BIGINT NOT NULL,
            qby BIGINT NOT NULL,
            txt TEXT NOT NULL
            );
            """
            self.cursor.execute(command_create_table)
            self.conn.commit()
            return True
        return False

    def add_quote(self, chat_id, msg_id, quote_by, quote):
        quote_id = self.count_quotes(chat_id) + 1
        self.cursor.execute("""INSERT INTO QUOTES (cid,mid,qid,qby,txt)
            VALUES ({0},{1},{2},{3},E'{4}');
            """.format(chat_id, msg_id, quote_id, quote_by, quote))
        self.conn.commit()
        return quote_id

    def get_quote(self, chat_id, quote_id=None):
        if quote_id is None:
            cqs = self.count_quotes(chat_id)
            if cqs:
                quote_id = randint(1, cqs)
            else:
                quote_id = 0
        self.cursor.execute("select * from quotes where cid={0} and qid={1}"
                            .format(chat_id, quote_id))
        q = self.cursor.fetchone()
        return {"id": q[0],
                "chat_id": q[1],
                "message_id": q[2],
                "quote_id": q[3],
                "quote_by": q[4],
                "quote": q[5]}

    def count_quotes(self, chat_id):
        self.cursor.execute("select count(*) from quotes where cid={}".format(chat_id))
        return self.cursor.fetchone()[0]

    def test(self):  # What? This is the first time I am using PostgreSQL.
        for i in range(10):
            self.add_quote(randint(1, 3), randint(1, 100),
                           1, str(randint(1, 1003)))

        print(self.get_quote(1))

        self.cursor.execute("SELECT *  FROM QUOTES")
        for r in self.cursor.fetchall()[-10:]:
            print(r)
