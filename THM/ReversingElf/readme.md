# Task 1
Untuk task 1 ini kita dapat langsung mendapatkan flagnya dengan cara run file `crackme1`. Namun untuk dapat run program tersebut, kita perlu mengubah file permissionnya dengan menambahkan x atau executable dengan cara
```bash
chmod +x crackme1
```
selanjutnya kita dapat langsung run program tersebut dengan cara `./crackme1`

# Task 2
Untuk task 2 ini kita perlu untuk mendapatkan password terlebih dahulu lalu run file `crackme2` dengan password tersebut untuk mendapatkan flag. Kita dapat mendapatkan passwordnya dengan mudah, dengan cara menggunakan `strings` pada file tersebut.
```bash
strings crackme2
...
...
Usage: %s password
super_secret_password
Access denied.
...
```
Setelah kita mendapatkan passwordnya, kita dapat mengubah file permissionnya menjadi executable dan run file `crackme2` bersamaan dengan password yang didapat
```bash
chmod +x crackme2
./crackme2 super_secret_password
```

# Task 3
Untuk task3 memiliki proses yang hampir sama dengan task 2, hanya saja disini kita mendapatkan versi encoded password setelah kita cek dengan `strings`.
```bash
strings crackme3
...
...
Usage: %s PASSWORD
        
malloc failed
    
ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==                                          
Correct password!
...
```
Dari bentuknya, kita dapat simpulkan bahwa encoded password tersebut menggunakan base64, jadi kita dapat melakukan decode dengan cara
```bash
echo "ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==" | base64 -d
...
f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
```
Selanjutnya kita dapat run program dengan cara seperti biasanya
```bash
chmod +x crackme3
./crackme3 f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
```

# Task 4
Untuk task 4 ini, kita akan menggunakan tools `gdb debugger`. Sebelum itu, kita buat file menjadi executable.
```bash
chmod +x crackme4
```
Selanjutnya kita buka `gdb`
```bash
gdb crackme4
```
Kita dapat menampilkan semua function yang ada dengan command `info functions`
```bash
(gdb) info functions
      
All defined functions:
    

           
Non-debugging symbols:
    
0x00000000004004b0  _init
 
0x00000000004004e0  puts@plt
0x00000000004004f0  __stack_chk_fail@plt
0x0000000000400500  printf@plt
0x0000000000400510  __libc_start_main@plt
0x0000000000400520  strcmp@plt
0x0000000000400530  __gmon_start__@plt
0x0000000000400540  _start
0x0000000000400570  deregister_tm_clones
0x00000000004005a0  register_tm_clones
0x00000000004005e0  __do_global_dtors_aux
0x0000000000400600  frame_dummy
0x000000000040062d  get_pwd
0x000000000040067a  compare_pwd
0x0000000000400716  main
0x0000000000400760  __libc_csu_init
0x00000000004007d0  __libc_csu_fini
0x00000000004007d4  _fini
```
Terdapat beberapa function yang menarik seperti  `main`, `get_pwd`, dan `compare_pwd`. Namun disini kita akan fokus ke `strcmp@plt` karena dari sekilas yang kita lihat, kita dapat menyimpulkan bahwa program ini akan melakukan komparasi input password dan password yang sebenarnya, yang mana akan menggunakan function `strcmp()` dalam bahasa C yang merupakan built-in function yang digunakan untuk string comparison. Maka selanjutnya kita dapat set breakpoint pada memory addres `strcmp@plt`.
```bash
(gdb) b *0x0000000000400520
Breakpoint 1 at 0x400520
```
Breakpoint merupakan intentional stopping atau tempat pause program ketika di run. Untuk tujuan debugging yang mana membantu mendapatkan knowledge tentang program pada saat eksekusi. Kita dapat run program dengan cara
```bash
(gdb) run test
Starting program: /home/kali/KeeTF/THM/ReversingElf/crackme4 test
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, 0x0000000000400520 in strcmp@plt ()
```
File akan tereksekusi dan akan berhenti pada set breakpoint. Selanjutnya kita dapat melihat registers yang ada. Register pada dasarnya adalah tempat penyimpanan kecil di prosesor yang dapat digunakan untuk menyimpan apa pun yang dapat diwakili dengan 8 byte atau kurang.
```bash
(gdb) info registers
      
rax            0x7fffffffd960      140737488345440                                                        
rbx            0x7fffffffdab8      140737488345784                                                        
rcx            0x11                17                                                                     
rdx            0x7fffffffde10      140737488346640                                                        
rsi            0x7fffffffde10      140737488346640                                                        
rdi            0x7fffffffd960      140737488345440                                                        
rbp            0x7fffffffd980      0x7fffffffd980                                                         
rsp            0x7fffffffd948      0x7fffffffd948                                                         
r8             0x4007d0            4196304                                                                
r9             0x7ffff7fcfb10      140737353939728
r10            0x7ffff7fcb858      140737353922648
r11            0x7ffff7fe1e30      140737354014256
r12            0x0                 0
r13            0x7fffffffdad0      140737488345808
r14            0x0                 0
r15            0x7ffff7ffd000      140737354125312
rip            0x400520            0x400520 <strcmp@plt>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
```
Selanjutnya, kita dapat melihat isi string dari beberapa register value(hexadecimal). Dengan cara
```bash
(gdb) x/s 0x7fffffffd960
0x7fffffffd960: "my_m0r3_secur3_pwd"
(gdb) x/s 0x7fffffffde10
0x7fffffffde10: "test"
(gdb) x/s 0x7fffffffdab8
0x7fffffffdab8: "\345\335\377\377\377\177"
```
Dan kita mendapat passwordnya, selanjutnya kita dapat run program
```bash
./crackme4 my_m0r3_secur3_pwd
```

# Task 5
Untuk task 5 ini, ketika kita run file `crackme5` kita akan mendapat output
```bash
Enter your input:
AAAAAA
Always dig deeper
```
Jika kita cek di `gdb`, kita akan mendapat beberapa function yang menarik
```bash
(gdb) info functions
All defined functions:
Non-debugging symbols:
0x0000000000400528  _init
0x0000000000400560  strncmp@plt
0x0000000000400570  puts@plt
0x0000000000400580  strlen@plt
0x0000000000400590  __stack_chk_fail@plt
0x00000000004005a0  __libc_start_main@plt
0x00000000004005b0  atoi@plt
0x00000000004005c0  __isoc99_scanf@plt
0x00000000004005d0  __gmon_start__@plt
0x00000000004005e0  _start
0x0000000000400610  deregister_tm_clones
0x0000000000400650  register_tm_clones
0x0000000000400690  __do_global_dtors_aux
0x00000000004006b0  frame_dummy
0x00000000004006d6  strcmp_
0x0000000000400773  main
0x000000000040086e  check
0x00000000004008d0  __libc_csu_init
0x0000000000400940  __libc_csu_fini
0x0000000000400944  _fini
```
Salah satu yang menarik adalah `strncmp@plt` yang mana merupakan function pembanding yang hampir sama dengan `strcmp@plt` pada task 4, hanya saja dengan `strncmp@plt` memungkinkan kita untuk membatasi jumlah karakter yang dibandingkan. Selanjutnya kita bisa coba untuk memasang breakpoint function `strncmp@plt`
```bash
(gdb) b * 0x0000000000400560
Breakpoint 1 at 0x400560
```
Lalu run program
```bash
(gdb) run test
Starting program: /home/kali/KeeTF/THM/ReversingElf/crackme5 test
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Enter your input:
AAAAAAAAAAAAAAAAAAAAAAAA

Breakpoint 1, 0x0000000000400560 in strncmp@plt ()
```
Selanjutnya kita bisa melihat register hasil run
```bash
(gdb) info registers
rax            0x7fffffffdc20      140737488346144
rbx            0x18                24
rcx            0x7fffffffdc40      140737488346176
rdx            0x1c                28
rsi            0x7fffffffdc40      140737488346176
rdi            0x7fffffffdc20      140737488346144
rbp            0x7fffffffdbf0      0x7fffffffdbf0
rsp            0x7fffffffdbb8      0x7fffffffdbb8
r8             0x18                24
r9             0x7ffff7f9daa0      140737353734816
r10            0x7ffff7dd9328      140737351881512
r11            0x7ffff7f1f140      140737353216320
r12            0x0                 0
r13            0x7fffffffdda0      140737488346528
r14            0x0                 0
r15            0x7ffff7ffd000      140737354125312
rip            0x400560            0x400560 <strncmp@plt>
eflags         0x246               [ PF ZF IF ]
```
Kita dapat coba untuk melihat isi dari mem address di `rax` dan `rcx`
```bash
(gdb) x/s 0x7fffffffdc20
0x7fffffffdc20: 'A' <repeats 24 times>
(gdb) x/s 0x7fffffffdc40
0x7fffffffdc40: "OfdlDSA|3tXb32~X3tX@sX`4tXtz\377\177"
```
Pada memory address `0x7fffffffdc40` kita mendapat isi string ```"OfdlDSA|3tXb32~X3tX@sX`4tXtz\377\177"```. Namun `\377\177` tidak perlu dihitung, karena hal tersebut merupakan escape character yaitu DEL (delete) character yang mana berarti memberi sinyal bahwa itu adalah akhir dari block of data atau juga bisa menjadi marking deleted characters di text file. Jadi string yang dapat kita jadikan input agar mendapat result `Good Game` adalah
```bash
OfdlDSA|3tXb32~X3tX@sX`4tXtz
```

# Task 6
Untuk task 6 ini, jika kita run `./crackme6`, nantinya akan mendapat output
```bash
./crackme6 password
password "password" not OK
```
Unutk itu, disini kita akan menggunakan `ghidra`. Buat project baru, selanjutnya buka file `crackme6` yang sudah terdownload. Jika sudah kita dapat fokus ke kotak `Symbol Tree` yang ada di sebelah kiri, lalu kita fokus ke folder yang memiliki nama `Functions`. Dari icon folder functions tersebut, kita mendapat beberapa functions yang menarik
```bash
...
compare_pwd
...
frame_dummy
...
my_secure_test
...
```
Jika kita cek satu persatu, yang paling stand out adalah function `my_secure_test`
```C
undefined8 my_secure_test(char *param_1)

{
  undefined8 uVar1;
  
  if ((*param_1 == '\0') || (*param_1 != '1')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[1] == '\0') || (param_1[1] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[2] == '\0') || (param_1[2] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[3] == '\0') || (param_1[3] != '7')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[4] == '\0') || (param_1[4] != '_')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[5] == '\0') || (param_1[5] != 'p')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[6] == '\0') || (param_1[6] != 'w')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[7] == '\0') || (param_1[7] != 'd')) {
    uVar1 = 0xffffffff;
  }
  else if (param_1[8] == '\0') {
    uVar1 = 0;
  }
  else {
    uVar1 = 0xffffffff;
  }
  return uVar1;
}
```
Kita mendapat potensial password `1337_pwd`, dan ternyata setelah dicoba ketika run `./crackme6` kita berhasil mendapatkan output OK
```bash
./crackme6 1337_pwd
password OK
```

# Task 7
Untuk task 7 ini, ketika kita run `./crackme7`, kita akan diberi pilihan dimana `1` akan memberi output `hi nama`, lalu `2` akan memberi output operasi aritmatika tambah (+), dan `3` adalah keluar dari program. 
```bash
./crackme7
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>]
```
Disini kita akan menggunakan `ghidra` lagi. Untuk kali ini load file, dan kita fokuskan lagi ke kotak `Symbol Tree`, dan pergi ke bagian `Functions`. Untuk kali ini kita  mendapat beberapa function yang menarik
```bash
...
giveFlag
...
```
Namun didalam function give flag, kita tidak mendapat banyak informasi, dan kita dapat asumsikan bahwa function ini akan terpanggil pada input tertentu dari kita. Maka dari itu, kita dapat coba untuk examine function `main`. Dan kita menemukan hal menarik
```C
...
    if (local_14 != 2) {
      if (local_14 == 3) {
        puts("Goodbye!");
      }
      else if (local_14 == 0x7a69) {
        puts("Wow such h4x0r!");
        giveFlag();
      }
      else {
        printf("Unknown choice: %d\n",local_14);
      }
      return 0;
    }
...
```
Dari code tersebut, kita dapat tahu bahwa jika input selain `2` adalah `3` maka kita akan exit atau keluar dari program. Namun jika input selain `2` adalah `0x7a69` maka nantinya akan menghasilkan output `"Wow such h4x0r!"` dan memanggil function `giveFlag()`. Namun jika kita inputkan langsung `0x7a69`, maka kita akan mendapat output `"Unknown choice: 0"`. Maka artinya, kita dapat coba untuk decode ke desimal dengan cara klik kanan pada `0x7a69`lalu pilih `Decimal` maka nanti akan berganti valuenya menjadi `31337`. Jika kita inputkan, maka kita akan mendapatkan output yang sesuai.
```bash
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 31337
Wow such h4x0r!
flag{xxx}
```

# Task 8
Untuk task 8 ini, ketika kita run `./crackme8`, kita akan diminta untuk memasukkan password. Untuk itu kita sekali lagi menggunakan `ghidra`. Jika kita langsung fokus ke `Functions` seperti biasa, dan langsung menuju ke `main`, kita akan menemukan metode yang hampir sama seperti di `task 7`
```C
...
  if (param_1 == 2) {
    iVar2 = atoi((char *)param_2[1]);
    if (iVar2 == -0x35010ff3) {
      puts("Access granted.");
      giveFlag();
      uVar1 = 0;
    }
    else {
      puts("Access denied.");
      uVar1 = 1;
    }
  }
...
```
Dimana jika input adalah `-0x35010ff3` maka kita akan mendapat akses dan mendapatkan flag, selain itu kita tidak mendapat akses atau `"Access denied."`. Jika kita langsung input `-0x35010ff3`, maka akan `"Access denied."`, maka kita bisa mengubahnya dengan cara klik kanan pada `-0x35010ff3` lalu pilih `decimal`, dan akan berubah valuenya menjadi `-889262067`. Jika kita inputkan, kita akan mendapat jawaban yang benar.
```bash
./crackme8 -889262067
Access granted.
flag{xxx}
```