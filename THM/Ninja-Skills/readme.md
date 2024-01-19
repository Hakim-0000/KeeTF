- cari file yang dimiliki oleh `best-group` group:
    `find / type f -group best-group 2>/dev/null`

- cari file yang berisi IP:
    `for i in $(cat list_file); do echo $i && grep -E -o '([0-9]{1,3}\.){3}[0-9]{1,3}' $i;done`

- cari file dengan SHA1 hash `9d54da7584015647ba052173b84d45e8007eba94`
    `for i in $(cat list_file); do sha1sum $i;done | grep -i '9d54da7584015647ba052173b84d45e8007eba94'`

- file dengan line total 230
    `for i in $(cat list_file); do wc -l $i;done`

- file dengan file owner ID 502
    `for i in $(cat list_file); do ls -ln $i;done| awk '$3 == 502'`

- file yang executable oleh semua orang
    `for i in $(cat list_file); do ls -l $i;done| awk '$1 ~ /x[^\ ]*x[^\ ]*x/'`
