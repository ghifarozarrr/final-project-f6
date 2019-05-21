# Final Project Kelompok F6

Mata kuliah Pemrograman Jaringan Kelas F

## Authors

* **Safira Vanillia Putri** - 05111640000001
* **Nuzha Musyafira** - 051116400000014
* **Ghifaroza Rahmadiana** - 051116400000057

### Protocol yang sudah dibuat

register user

```
auth_register [username] [password]
```

login user

```
auth_login [username] [password]
```

mengirim pesan antar user

```
send [username] [message]
```

mengirim file antar user

```
send_file [receiver username] [file name]
```

mendownload file dari user lain

```
download_file [file name]
```

mengecek pesan

```
inbox
```

membuat grup

```
mkgr [groupname]
```

bergabung di grup

```
join [groupname]
```

keluar chat

```
auth_logout
```

## Protocol yang akan dibuat

* Mengirim dan menerima pesan grup
* Mengirim dan menerima file pada grup
* Mengirim dan menerima file antar user
