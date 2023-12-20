- `Get-FileHash -Algorithm MD5 deebee.exe`

- `C:\Tools\strings64.exe -accepteula deebee.exe`

- `Get-Item -Path deebee.exe -Stream *`

	- Dapatkan nama stream di bagian `Stream` hasil run.

- `wmic process call create $(Resolve-Path .\deebee.exe:<nama_stream>)` 