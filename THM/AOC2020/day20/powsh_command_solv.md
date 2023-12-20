- `Get-ChildItem Documents -File -Hidden -ErrorAction SilentlyContinue`

- `Get-ChildItem Desktop -Directory -Hidden -ErrorAction SilentlyContinue`

- `Get-ChildItem -Directory -Hidden -Filter *3* -Recurse -ErrorAction SilentlyContinue`

- `Get-ChildItem C:\\Windows\\System32\\3lfthr3e -File -Hidden -Recurse -ErrorAction SilentlyContinue`

- `Get-Content -Path C:\\Windows\\System32\\3lfthr3e\\1.txt | Measure-Object -Word`

- `(Get-Content -Path C:\\Windows\\System32\\3lfthr3e\\1.txt)[551]`

- `(Get-Content -Path C:\\Windows\\System32\\3lfthr3e\\1.txt)[6991]`

- `Select-String -Path C:\\Windows\\System32\\3lfthr3e\\2.txt -Pattern redryder`