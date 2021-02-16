import requests
import json
import datetime
import os

BASE_URL = "https://qiita.com/api/v2/items"
token = ['ACCSESS_WRITE_TOKEN']

dt_now = datetime.datetime.now()
print(str(dt_now.date()))

def file_delete(dir_name, lines_to_delete):
  file_name = (f"./article/{dir_name}/index.mdx")
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

def submit_article(dir_name):
  with open(f"./article/{dir_name}/config.json") as f:
      conf = f.read()
  with open(f"./article/{dir_name}/index.md") as f:
      body = f.read()
  headers = {"Authorization": f"Bearer {token}"}
  item = json.loads(conf)
  item["body"] = body

  if item["id"] == "":
      res = requests.post(BASE_URL, headers=headers, json=item)
      with open(f"./article/{dir_name}/config.json", "w") as f:
          item["id"] = res.json()["id"]
          item["body"] = ""
          f.write(json.dumps(item))
      return res

  else:
      now = datetime.datetime.now()
      item["title"] += now.strftime("【%Y/%m/%d %H時更新】")
      item_id = item["id"]
      res = requests.patch(BASE_URL + f"/{item_id}", headers=headers, json=item)
      return res


if __name__ == "__main__":
  dir_name = str(dt_now.date())
  file_delete(dir_name, 6)
  print('line deleted!')
  res = submit_article(dir_name).json()
  print(res["title"], res["url"])
  print("==========================================================")
  print("投稿しました")