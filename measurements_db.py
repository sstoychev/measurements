import os
import sqlite3

DB = 'measurements.db'

class Measurements_db(object):

    conn = None
    cur = None

    fields = {
        'datetime_int': 'int',
        'temperature': 'float',
        'pressure': 'float',
        'humidity': 'float',
        'gas_resistances': 'float',
        'lux': 'int',
        'proximity': 'int',
    }

    def __init__(self):
        self.create_table()

    def __del__(self):
        if self.conn is not None:
            self.cur.close()
            self.conn.close()

    def create_table(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        if not os.path.isfile(DB):
            vals = [f'{key} {self.fields[key]}' for key in self.fields.keys()]
            sql = f'CREATE TABLE measurements ({", ".join(vals)})'
            cur.execute(sql)

        self.conn = conn
        self.cur = cur

    def insert_records(self, records):
        # check the length of each record, not to have errors on insert
        record_len = len(self.fields)
        if any([length != record_len for length in map(len, records)]):
            raise Exception('incorrect number of values on insert')
        fields = ', '.join(self.fields.keys())
        values = ', :'.join(self.fields.keys())
        sql = (f"""
            INSERT INTO
                {DB}
                ({fields})
            VALUES
                (:{values})""", records)
        self.cur.executemany(sql)

if __name__ == 'main':
    db = Measurements_db()
