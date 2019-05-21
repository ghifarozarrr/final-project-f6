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


synchronous

| Requests | Concurrency | Time/Request (ms) | Total Time (s) | Transfer Rate (Kbytes/s) | Request/Second |
|----------|-------------|-------------------|----------------|--------------------------|----------------|
|    10    |      1      |       4.224       |      0.042     |           75.38          |     236.76     |
|    10    |      5      |       1.485       |      0.015     |          219.30          |     688.85     |
|    10    |      10     |       1.260       |      0.013     |          252.71          |     793.78     |
|    100   |      1      |       1.867       |      0.187     |          170.56          |     535.74     |
|    100   |      5      |       2.453       |      0.245     |          129.81          |     407.74     |
|    100   |      10     |       2.165       |      0.217     |          147.02          |     461.80     |
|   1000   |      1      |       2.159       |      2.159     |          147.45          |     463.15     |
|   1000   |      5      |       2.059       |      2.059     |          154.59          |     485.57     |
|   1000   |      10     |       1.999       |      1.999     |          159.30          |     500.37     |
|   10000  |      1      |       1.887       |     18.869     |          168.72          |     529.98     |
|   10000  |      5      |       1.950       |     19.504     |          163.23          |     512.73     |
|   10000  |      10     |       1.863       |     18.634     |          170.85          |     536.65     |
|   20000  |      1      |       1.881       |     37.625     |          169.23          |     531.56     |
|   20000  |      5      |       1.908       |     38.151     |          166.89          |     524.23     |
|   20000  |      10     |       1.894       |     37.878     |          168.10          |     528.01     |
