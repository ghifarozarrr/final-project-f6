# Final Project Kelompok F6

Mata kuliah Pemrograman Jaringan Kelas F

## Authors

* **Safira Vanillia Putri** - 05111640000001
* **Nuzha Musyafira** - 051116400000014
* **Ghifaroza Rahmadiana** - 051116400000057

## Tugas 4 - Spesifikasi Protokol

### Auth
- ##### Registrasi user
    User dapat membuat akun baru dengan memasukkan username serta password. Jika username yang dimasukkan sudah ada, user akan diminta untuk memasukkan username yang lain. Setelah berhasil membuat akun, user akan diminta untuk login menggunakan username dan passwordnya.
    
    ``auth_register [username] [password]``

- ##### Login user
    User dapat login ke akunnya dengan memasukkan username dan passwordnya.
    
    ``auth_login [username] [password]``

- ##### Logout user
    User yang sudah login, dapat logout.
    
    ``auth_logout``

- ##### Melihat list user lain
    ``ls``

### Personal Chatting

- ##### Mengirim pesan antar user
    User dapat mengirim pesan kepada user lainnya dengan memasukkan username tujuan dan pesan yang ingin dikirim.
    ``send [recceiver username] [message]``

- ##### Melihat pesan-pesan masuk dari user lain
    User dapat melihat pesan-pesan yang dikirimkan oleh user lain.
    
    ``inbox``

- ##### Mengirim file antar user
    User dapat mengirim pesan berupa file kepada user lainnya dengan memasukkan username tujuan dan nama file yang ingin dikirim. File yang dikirim akan disimpan pada folder upload yang berada di sisi server dengan prefix nama file timestamp file tersebut dikirim.
    
    ``send_file [receiver username] [file name]``

- ##### Mendownload file dari user lain
    User dapat mendownload file yang dikirimkan oleh user lain. File yang didownload user adalah file yang sebelumnya sudah diupload pada folder upload. File yang didownload user akan disimpan pada folder download/username.
    ``download_file [file name]``

### Group Messaging

- ##### Membuat grup baru
    ``mkgr [groupname]``

- ##### Bergabung di grup
    ``join [groupname]``

- ##### Melihat list grup yang ada
    ``ls_group``

- ##### Melihat anggota pada grup
    User dapat melihat daftar anggota pada grup setelah bergabung dengan grup tujuan.
    ``ls_member [groupname]``

- ##### Mengirim pesan ke grup
    ``sendgroup [groupname] [message]``

- ##### Mengecek pesan dari grup
    ``inboxgroup [groupname]``

- ##### Mengirim file ke grup
    ``sendgroup_file [groupname] [file name]``

- ##### Mendownload file dari grup
    ``downloadgroup_file [groupname] [file name]``

- ##### Keluar dari grup
    ``leave [groupname]``

## Tugas 5 - Hasil Pengujian Web Server

Synchronous

| Requests | Concurrency | Time/Request (ms) | Total Time (s) | Transfer Rate (Kbytes/s) | Request/Second |
|:--------:|:-----------:|:-----------------:|:--------------:|:------------------------:|:--------------:|
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

Berdasarkan hasil pengujian di atas, didapatkan bahwa semakin banyak request, maka semakin lama waktu yang dibutuhkan untuk melayani setiap request. Namun hasil asynchronous relatif lebih cepat dibandingkan synchronous.

Synchronous Load Balancer

| Requests | Concurrency | Time/Request (ms) | Total Time (s) | Transfer Rate (Kbytes/s) | Request/Second |
|:--------:|:-----------:|:-----------------:|:--------------:|:------------------------:|:--------------:|
|    10    |      1      |       1.517       |      0.015     |           0.00           |     658.98     |
|    10    |      5      |       1.242       |      0.012     |           0.00           |     804.96     |
|    10    |      10     |       1.269       |      0.013     |           0.00           |     788.15     |
|    100   |      1      |       1.216       |      0.122     |           0.00           |     822.67     |
|    100   |      5      |       1.096       |      0.110     |           0.00           |     912.38     |
|    100   |      10     |       1.100       |      0.110     |           0.00           |     908.69     |
|   1000   |      1      |       1.191       |      1.191     |           0.00           |     839.44     |
|   1000   |      5      |       1.138       |      1.138     |           0.00           |     879.06     |
|   1000   |      10     |       1.420       |      1.420     |           0.00           |     704.40     |
|   10000  |      1      |       1.005       |     10.051     |           0.00           |     994.90     |
|   10000  |      5      |       0.935       |      9.349     |           0.00           |     1069.63    |
|   10000  |      10     |       0.953       |      9.527     |           0.00           |     1049.61    |
|   20000  |      1      |       1.077       |     21.534     |           0.00           |     928.76     |
|   20000  |      5      |       1.000       |     19.996     |           0.00           |     1000.22    |
|   20000  |      10     |       1.113       |     22.251     |           0.00           |     898.82     |

Asynchronous Load Balancer

| Requests | Concurrency | Time/Request (ms) | Total Time (s) | Transfer Rate (Kbytes/s) | Request/Second |
|:--------:|:-----------:|:-----------------:|:--------------:|:------------------------:|:--------------:|
|    10    |      1      |       2.035       |      0.020     |           0.00           |     491.38     |
|    10    |      5      |       1.348       |      0.013     |           0.00           |     741.73     |
|    10    |      10     |       1.558       |      0.016     |           0.00           |     641.68     |
|    100   |      1      |       1.120       |      0.112     |           0.00           |     893.18     |
|    100   |      5      |       1.518       |      0.152     |           0.00           |     658.86     |
|    100   |      10     |       1.276       |      0.128     |           0.00           |     783.87     |
|   1000   |      1      |       1.242       |      1.242     |           0.00           |     804.89     |
|   1000   |      5      |       1.191       |      1.191     |           0.00           |     839.49     |
|   1000   |      10     |       1.422       |      1.442     |           0.00           |     693.39     |
|   10000  |      1      |       0.959       |      9.592     |           0.00           |     1042.57    |
|   10000  |      5      |       0.980       |      9.796     |           0.00           |     1020.81    |
|   10000  |      10     |       0.962       |      9.619     |           0.00           |     1039.58    |
|   20000  |      1      |       0.955       |     19.095     |           0.00           |     1047.37    |
|   20000  |      5      |       0.963       |     19.268     |           0.00           |     1038.01    |
|   20000  |      10     |       0.932       |     18.644     |           0.00           |     1072.72    |

Berdasarkan hasil pengujian di atas, didapatkan bahwa load balancer terbukti dapat meningkatkan kemampuan sistem dalam melayani lebih banyak request dengan lebih cepat.
