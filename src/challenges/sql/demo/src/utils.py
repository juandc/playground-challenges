import sqlite3
import sqlparse

def get_headers(desc):
  headers = []
  for item in desc:
    headers.append(item[0])
  return headers

def get_values(data):
  body = []
  for item in data:
    body.append(list(item))
  return body

def run_sql(connection):
  cursor = connection.cursor()
  outputs = []

  try:
    setup = open("./setup.sql", "r").read()
    cursor.executescript(setup)
  except sqlite3.OperationalError as error:
    print("Error en setup.sql")
    print(error)

  try:
    exercise = open("./exercise.sql", "r").read()
    formated = sqlparse.format(exercise, strip_comments=True).strip()
    for query in sqlparse.split(formated):
      execute = cursor.execute(query)
      if query.upper().startswith('SELECT'):
        headers = get_headers(execute.description)
        body = get_values(execute.fetchall())
        output_dict = { 'headers': headers, 'body': body }
        outputs.append(output_dict)
  except Exception as error:
    print("Error en exercise.sql")
    print(error)
  
  return outputs
