# Overview
SQLI di produk kategori filter

Hint:
- db memiliki tabel lain dengan nama `users` yang memiliki kolom `username` dan `password`
- gunakan `union`

Goals:
- retrieve all username dan passwords, dan gunakan informasi untuk login sebagai `administrator` 

# Analisis
cek apakah vuln terhadap sqli dengan `'`

gunakan payload `'+union+sleect+username,password+from+users--`