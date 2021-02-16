import requests
import json
import datetime
import os 
import sys

args = sys.argv
if len(args) > 1:
  token = args[1]
else:
  print("引数が指定されていません")

BASE_URL = "https://qiita.com/api/v2/items"

dt_now = datetime.datetime.now()
print(str(dt_now.date()))

def file_delete(dir_name, lines_to_delete):
  file_name = (f"article/{dir_name}/index.mdx")
  initial_line = 1
  file_lines = {}
  with open(file_name) as f:
    content = f.readlines() 
  for line in content:
    file_lines[initial_line] = line.strip()
    initial_line += 1

  line_to_delete = lines_to_delete + 1
  for i in range(1, line_to_delete):
    file_lines.pop(i)

  ex = os.path.splitext(file_name)
  output_filename = ex[0] + '.md'

  f = open(output_filename, "w")
  for line_number, line_content in file_lines.items():
    f.write('{}\n'.format(line_content))
  f.close()

if __name__ == "__main__":
  dir_name = str(dt_now.date())
  file_delete(dir_name, 6)
  print('line deleted!')
  print(token)
  print("==========================================================")
