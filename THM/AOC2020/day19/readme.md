start target machine.

selanjutnya pergi ke target mesin. `http://IP-target/`. Terdapat 2 section pada website, yaitu list dan admin page.
kita utamakan list terlebih dahulu.

jika kita eksperimen dengan memasukkan nama pada kolom search untuk melihat list good kid kita akan mendapat
`nama on a naughty list`, namun saat kita lihat di bagian url, kita akan mendapat seperti berikut
```
http://10.10.75.241/?proxy=http%3A%2F%2Flist.hohoho%3A8080%2Fsearch.php%3Fname%3Dnama
```

yang mana ketika di decode akan menjadi
```
http://10.10.75.241/?proxy=http://list.hohoho:8080/search.php?name=nama
```

karena `.hohoho` bukan merupakan list domain atau top level domain (seperti .com), jadi dapat kita asumsikan bahwa
hostname me-refer pada back-end mesin di lokal target. Sepertinya website ini berjalan dengan cara mengambil URL,
lalu membuat request pada back-end dan return hasil ke front-end.

cara paling awal yang dapat kita coba adalah pergi ke root dari web back-end tersebut.
```
http://10.10.75.241/?proxy=http%3A%2F%2Flist.hohoho
```

dan hasilnya adalah "Not Found. The requested URL was not found on this server", yang mana seperti generic 404
yang mana mengindikasi bahwa kita dapat membuat server untuk melakukan request ke modified url dan memberikan
respon balik. Selain itu kita dapat melakukan berbagai hal, contohnya seperti coba mengganti port, atau mencari
valid URL untuk `list.hohoho`.

jika kita coba mengganti port 8080 dengan 80, kita akan mendapat "Failed to connect to list.hohoho port 80: Connection refused",
namun jika kita mencoba untuk connect ke port 22 (default ssh), kita akan mendapat error message yang berbeda
"Recv failure: Connection reset by peer" berarti port 22 terbuka, dan error tersebut terjadi karena port 80
mencoba untuk terhubung ke port 22 yang mana tidak akan bisa, dan port 22 akan memberi error message, sehingga
error message tersebut terdisplay ke front-end.

selanjutnya kita dapat mencoba menjadi `list.hohoho` ke  `localhost`
```
http://IP-target/?proxy=http%3A%2F%2Flocalhost
```

akan muncul "Your search has been blocked by our security team." yang mana berarti dev sudah cek atau
mengamankan metode ini. Sepertinya dev sudah block semua request kecuali ke `list.hohoho`. Kita dapat baypass
dengan mudah dengan membuat subdomain seperti `list.hohoho.mysubdomain.com` yang akan refer ke 127.0.0.1.
namun pada kali ini kita tidak perlu membuat domain, kita dapat memanfaatkan banyak domain yang sudah ada, seperti
`localhost.me`. Jika kita cek di terminal dengan `host anything.localhost.me` akan refer back ke 127.0.0.1.
Sehingga kita dapat memanfaatkannya untuk SSRF.
```
http://10.10.75.241/?proxy=http%3A%2F%2Flist.hohoho.localhost.me
```

dan berhasil, kita mendapat password Santa:
```
...
** **** *** ******** ****! 
```

dan kita dapat menggunakannnya untuk login ke halaman admin
