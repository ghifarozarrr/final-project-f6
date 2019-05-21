# Final Project Kelompok F6

Mata kuliah Pemrograman Jaringan Kelas F

## Authors

* **Safira Vanillia Putri** - 05111640000001
* **Nuzha Musyafira** - 051116400000014
* **Ghifaroza Rahmadiana** - 051116400000057

## Spesifikasi Protokol

register user

```
auth_register [username] [password]
```

login user

```
auth_login [username] [password]
```

melihat list user

```
ls
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

mengecek pesan dari user

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

melihat list grup

```
ls_group
```

melihat anggota pada grup

```
ls_member [groupname]
```

keluar dari grup

```
leave [groupname]
```

mengirim pesan ke grup

```
sendgroup [groupname] [message]
```

mengecek pesan dari grup

```
inboxgroup [groupname]
```

mengirim file ke grup

```
sendgroup_file [groupname] [file name]
```

mendownload file dari grup

```
downloadgroup_file [groupname] [file name]
```

keluar chat

```
auth_logout
```
