# Juice Shop OWASP
Spawn menggunakan docker:
- `sudo service docker start`
- `docker run --rm -p 3000:3000 bkimminich/juice-shop`

Catatan ini merupakan salah satu write up yang saya buat untuk belajar cybersecurity. Saya akan berusaha semaksimal mungkin untuk dapat menjelaskan apa yang saya lakukan sehingga bisa dimengerti, so tanpa basa-basi, mari kita gaskan!!!

# Challenge

## Find The Score Board - 1 Star
- Goals : Find the carefully hidden 'Score Board' page.

Namanya CTF, pasti sangat kurang rasanya jika kita nggak bisa lihat score yang sudah didapat. Untuk menemukan score board disini, saya nggak sengaja menemukannya dengan cara guessing nama direktori, dan ternyata langsung benar yaitu ada di `/score-board` 😂. Oke, kita lanjut ke challenge lain .

## Error Handling - 1 Star
- Goals : Provoke an error that is neither very gracefully nor consistently handled.
- Hint : Try to submit bad URL forms. Alternatively tamper with URL paths or parameter. 

Challenge selanjutnya yaitu **Error Handling**, untuk mendapatkan error disini, kita bisa menggunakan tools direktori fuzzing seperti `gobuster`, `dirsearch`, `ffuf`, dll. Disini saya menggunakan `dirsearch` dengan wordlist defaultnya
```bash
dirsearch -u http://localhost:3000
...
[09:05:03] 200 -  407B  - /.well-known/security.txt                    
[09:05:45] 301 -  183B  - /api-docs  ->  /api-docs/
[09:05:45] 500 -    3KB - /api
[09:05:45] 500 -    3KB - /api.log
[09:05:45] 500 -    3KB - /api.php
[09:05:45] 500 -    3KB - /api.py
...
```
Kita akan mendapat banyak response code 500 yang menandakan server internal error dan docker akan otomatis berhenti. Ketika kita run lagi, kita akan mendapati bahwa challenge **Error Handling** solved.

## Security Policy - 1 Star
Hasil dari dir fuzzing sebelumnya tidak sepenuhnya sampah. Jika kalian jeli, meskipun mungkin hasil dari dir fuzzing kita mostly memiliki response code 500, tapi masih terdapat beberapa hasil yang cukup informatif
```bash
...
[09:05:03] 200 -  407B  - /.well-known/security.txt                    
[09:05:45] 301 -  183B  - /api-docs  ->  /api-docs/
...
[09:05:50] 301 -  179B  - /assets  ->  /assets/       
[09:06:05] 200 -    9KB - /common.js                  
[09:06:27] 200 -   11KB - /ftp                        
[09:06:55] 200 -  480KB - /main.js
```
Dari hasil diatas, terdapat `/.well-known/security.txt`, yang jika kita buka, file ini hampir mirip dengan `robots.txt`. Kita dapat melihat informasinya
```
# /.well-known/security.txt
Contact: mailto:donotreply@owasp-juice.shop
Encryption: https://keybase.io/bkimminich/pgp_keys.asc?fingerprint=19c01cb7157e4645e9e2c863062a85a8cbfbdcda
Acknowledgements: /#/score-board
Preferred-languages: en, ar, az, bg, bn, ca, cs, da, de, ga, el, es, et, fi, fr, ka, he, hi, hu, id, it, ja, ko, lv, my, nl, no, pl, pt, ro, ru, si, sv, th, tr, uk, zh
Hiring: /#/jobs
Expires: Sun, 02 Feb 2025 02:55:51 GMT
```
Dan ternyata isinya kurang begitu menarik untuk sekarang karena `/#/score-board` sudah dilewati dan `/#/jobs` tidak return apapun, mungkin kita bisa simpan terlebih dahulu. Ngomong-ngomong soal `robots.txt`, kita juga bisa sekalian melihat isinya
```
# robots.txt
User-agent: *
Disallow: /ftp
```
Oh, ternyata isinya sama dengan isi salah satu hasil dir fuzzing kita, yaitu `/ftp`. Jika kita buka dir `/ftp` tersebut, kita akan mendapat beberapa file dan folder
```
d    quarantine
f    acquisitions.md
f    announcement_encrypted.md
f    coupons_2013.md.bak
f    eastere.gg
f    encrypt.pyc
f    incident-support.kdbx
f    legal.md
f    package.json.bak
f    suspicious_errors.yml
```
Dan file `legal.md` inilah yang membuat kita menyelesaikan challenge **Security Policy**.

## Confidential Document - 1 Star
Untuk challenge ini, kita dapat menyelesaikannya dengan melihat isi dari file `acquisitions.md` di dir `/ftp`
```
curl http://localhost:3000/ftp/acquisitions.md                                            
...
> This document is confidential! Do not distribute!
...
Our shareholders will be excited. It's true. No fake news.
```

## Login Admin - 2 Star
Untuk dapat melakukan login, disini diperlukan email. Jika kita lihat di beberapa produk yang ada di dashboard, akan terlihat kita dapat beberapa email, dan salah satunya adalah `admin@juice-sh.op`. Kita dapat email admin, selanjutnya kita bisa pergi ke page login.

Hal paling pertama yang saya coba di page admin adalah memasukkan karakter `'` untuk mencoba apakah login page ini vuln terhadap SQLI, yang mana jika hasilnya adalah error, berarti login page vulnerable terhadap SQLI. Hal ini bisa terjadi karena ketika kita melakukan POST request, kita mengirimkan query ke database, contoh query yang dikirimkan `select * from users where email='admin' & password='admin'`. Sedangkan jika kita memasukkan karakter `'` pada bagian email, makan akan menjadi seperti berikut `select * from users where email='admin'' & password='admin'`, hal ini akan menghasilkan error karena terdapat `'` setelah input kolom `email` yang membuat baris belakangnya masuk ke dalam string input, jadi dari sql membacanya seperti ini `select * from users where email='admin''& password=' admin'`, dimana string kedua tidak masuk ke input manapun.

Kembali ke target, Jika kita coba memasukkan `admin@juice-sh.op'` dan password random, maka akan return error `[object Object]` pada login page, mengartikan login page vuln terhadap SQLI. Selanjutnya kita dapat menggunakan payload yang umum digunakan seperti `' or '1'='1'--`. Jika kita tambahkan ke input email kita, maka akan menjadi `admin@juice-sh.op' or '1'='1'--`, selanjutnya isi password dengan string random, dan klik login. Yes kita berhasil login sebagai admin! 🎉🎉

## Privacy Policy - 1 Star
Karena kita sudah login ke web, kita dapat melihat privacy policy di bagian menu Account -> Privacy&Security -> Privacy Policy.

## Repetitive Registration - 1 Star



## DOM XSS - 1 Star
- Goals : Lakukan DOM XSS dengan payload ``<iframe src="javascript:alert(`xss`)">``.
- Hint : Cari input field yang kontennya tampil dalam bentuk HTML ketika disubmit.

DOM XSS, atau Document Object Model Cross-Site Scripting, merupakan salah satu tipe XSS yang terjadi ketika attacker memasukkan malicious code kedalam Document Object Model (DOM) dari web app. DOM merupakan representasi dari struktur web yang dapat digunakan untuk sebuah scripts berinteraksi dengan HTML dan memodifikasi kontennya.

Input field yang paling stand out pertama kali adalah search bar. Jika kita mencoba input ``<iframe src="javascript:alert(`xss`)">`` pada search bar, maka hasilnya akan berhasil. Hal ini terjadi karena ketika kita menggunakan search bar, kita dapat menampilkan objek yang hanya kita inginkan, yang mana berarti mengubah konten yang ditampilkan.

## Bonus Payload - 1 Star
- Goals : melakukan XSS dengan payload `<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>` saat DOM challenge

Untuk challenge kali ini, kita hanya perlu copy paste payload tersebut ke search bar.

## Missing Encoding - 1 Star
- Goals : memunculkan foto kucing dari Bjorn saat "melee combat-mode"
- Hints : Cek page Photo Wall dan cari gambar yang tidak bisa ter load

Untuk challenge kali ini, kita bisa pergi langsung ke `/#/photo-wall`. Dalam page tersebut, akan ada gambar yang tidak ter load secara benar, kita dapat coba untuk melihat link fotonya di Developer Mode.

Jika kita perhatikan di bagian link gambar (`<img class='image' ... src="assets/public/images/uploads/..`), terdapat simbol `😼`, `#`, dan `-` pada link nya `src="assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg"`. Kita dapat mencoba untuk mengubah beberapa simbol berikut ke format url encoded. Namun sebelum itu, jika kita lihat di link gambar lainnya, terdapat simbol `-` dan tidak ada masalah sama sekali, jadi kemungkinan penyebabnya adalah `😼`atau `#`.

Jika kita encode `😼`, akan menjadi `%F0%9F%98%BC` dan jika kita replace simbol pada bagian link gambar menjadi `.../%F0%9F%98%BC-#zatschi-#whoneedsfourlegs-1572600969477.jpg`, tidak ada perubahan sama sekali, berarti simbol atau emoji tidak berpengaruh disini. Selanjutnya kita coba encode `#` yang akan menjadi `%23`, dan jika kita coba mengganti simbol pada link gambar menjadi `.../😼-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg`, maka gambar kucing akan muncul dan kita berhasil menyelesaikan challenge.

## Outdated Allowlist - 1 Star
- Goals : redirect ke crypto currency link
- Hints : Mungkin lupa untuk membersihkan link tersebut dari source code

Untuk challenge kali ini, kita dapat mencarinya di source code. Buka developer mode dan pergi ke tab Debugger. Kita pergi ke file `main.js`, lalu kita klik kanan dan pilih wrap lines. Selanjutnya, kita pakai tools terkenal, CTRL+F 😎. Kita masukkan keyword `redirect` dan kita cari yang berhubungan dengan crypto. Dan kita akan menemukan `...{data:"bitcoin:1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",url:"./redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",address:"1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm",title:"TITLE_BITCOIN_ADDRESS"}...`, kita bisa ambil url nya `/redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm` dan kita masukkan ke link utama menjadi `http://localhost:3000/redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm`, dan kita akan menyelesaikan challenge nya.