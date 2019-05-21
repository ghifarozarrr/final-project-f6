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
## Hasil Pengujian Web Serve

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

Asynchronous

| Requests | Concurrency | Time/Request (ms) | Total Time (s) | Transfer Rate (Kbytes/s) | Request/Second |
|:--------:|:-----------:|:-----------------:|:--------------:|:------------------------:|:--------------:|
|    10    |      1      |       2.250       |      0.022     |          141.51          |     444.48     |
|    10    |      5      |       0.676       |      0.007     |          471.15          |     1479.95    |
|    10    |      10     |       0.648       |      0.006     |          491.30          |     1543.21    |
|    100   |      1      |       0.886       |      0.089     |          359.24          |     1128.41    |
|    100   |      5      |       0.823       |      0.082     |          386.92          |     1215.35    |
|    100   |      10     |       0.706       |      0.071     |          450.85          |     1416.17    |
|   1000   |      1      |       0.809       |      0.809     |          393.67          |     1236.55    |
|   1000   |      5      |       0.812       |      0.812     |          391.85          |     1230.83    |
|   1000   |      10     |       0.896       |      0.896     |          355.31          |     1116.06    |
|   10000  |      1      |       0.709       |      7.094     |          448.75          |     1409.56    |
|   10000  |      5      |       0.680       |      6.800     |          468.18          |     1470.62    |
|   10000  |      10     |       0.755       |      7.551     |          421.64          |     1324.40    |
|   20000  |      1      |       0.742       |     14.836     |          429.18          |     1348.11    |
|   20000  |      5      |       0.713       |     14.263     |          446.43          |     1402.27    |
|   20000  |      10     |       0.754       |     15.071     |          422.47          |     1327.03    |
