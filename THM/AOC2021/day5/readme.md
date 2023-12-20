login dengan creds `McSkidy:password`
selanjutnya ke bagian setting dan ubah password ke `password123`,
nantinya link pada kolom url akan menjadi
`http://IP-target/settings?new_password=password123`
selanjutnya coba buat comment dengan `hello <u>grinch</u>` pada
post milik Grinch. dan nantinya hasil komentar di forum akan menjadi
`hello grinch` dengan kata `grinch` terunderline.
selanjutnya kita dapat implementasi XSS ke kolom komentar
dengan `hey grinch<script>fetch('/settings?new_password=password123');</script>
sehingga nanti siapapun yang membuka page yang berisi komentar tersebut
akan terganti passwordnya menjadi `password123`
