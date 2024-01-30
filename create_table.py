from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

MOD_SIZE = 256
table_name = "fingertable"
FEATURE_COLS = 640

engine = create_engine('sqlite:///./cloud.db', echo = True)

# ## Table initialize

meta = MetaData()

students = Table(
   table_name, meta, 
   Column('enc_roll', String(MOD_SIZE), primary_key = True), 
   Column('enc_sum_of_sqr', String(MOD_SIZE))
)

meta.create_all(engine)

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

for i in range(FEATURE_COLS):
    col_name = "enc_f" + str(i)
    column = Column(col_name, String(MOD_SIZE))
    add_column(engine, table_name, column)
