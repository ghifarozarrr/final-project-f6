## Tugas 4 - Spesifikasi Protokol

### Auth
- ##### Registrasi user
    User dapat membuat akun baru dengan memasukkan username serta password. Jika username yang dimasukkan sudah ada, user akan diminta untuk memasukkan username yang lain. Setelah berhasil membuat akun, user akan diminta untuk login menggunakan username dan passwordnya. Apabila user sudah dalam keadaan login, akan muncul pesan error untuk logout terlebih dahulu.
    
    ``auth_register [username] [password]``

- ##### Login user
    User dapat login ke akunnya dengan memasukkan username dan passwordnya. Apabila username atau password yang dimasukkan salah, akan muncul pesan error.
    
    ``auth_login [username] [password]``

- ##### Logout user
    User yang sudah login, dapat logout.
    
    ``auth_logout``

- ##### Melihat list user lain
    User dapat melihat daftar user lain.
    
    ``ls``

### Personal Chatting

- ##### Mengirim pesan antar user
    User dapat mengirim pesan kepada user lainnya dengan memasukkan username tujuan dan pesan yang ingin dikirim.
    
    ``send [recceiver username] [message]``

- ##### Melihat pesan-pesan masuk dari user lain
    User dapat melihat pesan-pesan yang dikirimkan oleh user lain.
    
    ``inbox``

- ##### Mengirim file antar user
    User dapat mengirim pesan berupa file kepada user lainnya dengan memasukkan username tujuan dan nama file yang ingin dikirim. File yang dikirim akan disimpan pada folder upload yang berada di sisi server dengan prefix nama file timestamp pada waktu file tersebut dikirim.
    
    ``send_file [receiver username] [file name]``

- ##### Mendownload file dari user lain
    User dapat mendownload file yang dikirimkan oleh user lain. File yang didownload user adalah file yang sebelumnya sudah diupload pada folder upload. File yang didownload user akan disimpan pada folder download/username_user.
    
    ``download_file [file name]``

### Group Messaging

- ##### Membuat grup baru
    User dapat membuat grup baru dengan nama yang berbeda-beda. Apabila nama grup sudah ada sebelumnya, maka akan muncul pesan error bahwa nama grup sudah ada.
    
    ``mkgr [groupname]``

- ##### Bergabung di grup
    User dapat bergabung dengan grup yang sudah tersedia dengan memasukkan nama grup. Apabila user bergabung dengan nama grup yang tidak tersedia, maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``join [groupname]``
    
- ##### Melihat list grup yang ada
    User dapat melihat daftar grup apa saja yang tersedia.
    
    ``ls_group``

- ##### Melihat anggota pada grup
    User dapat melihat daftar anggota pada grup setelah bergabung dengan grup tujuan. Apabila belum bergabung dengan grup tersebut, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``ls_member [groupname]``

- ##### Mengirim pesan ke grup
    User dapat mengirimkan pesan ke grup setelah bergabung dengan grup tujuan. Apabila belum bergabung dengan grup tersebut, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.

    ``sendgroup [groupname] [message]``

- ##### Melihat pesan dari grup
    User dapat melihat pesan yang masuk pada grup setelah bergabung dengan grup tujuan. Apabila belum bergabung dengan grup tersebut, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``inboxgroup [groupname]``

- ##### Mengirim file ke grup
    User dapat mengirim pesan berupa file ke grup setelah bergabung dengan grup tujuan, dengan cara memasukkan grup tujuan dan nama file yang ingin dikirim. File yang dikirim akan disimpan pada folder upload yang berada di sisi server dengan prefix nama file timestamp file tersebut dikirim. Apabila belum bergabung dengan grup tersebut, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``sendgroup_file [groupname] [file name]``

- ##### Mendownload file dari grup
    User dapat mendownload file yang dikirimkan oleh user lain setelah bergabung dengan grup tujuan. File yang didownload user adalah file yang sebelumnya sudah diupload pada folder upload. File yang didownload user akan disimpan pada folder downloadgroup/username_user. Apabila belum bergabung dengan grup tersebut, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``downloadgroup_file [groupname] [file name]``

- ##### Keluar dari grup
    User dapat meninggalkan grup apabila sudah terdaftar sebelumnya. Apabila belum terdaftar, maka akan muncul pesan error bahwa user belum menjadi anggota grup tersebut. Selain itu, apabila grup tidak tersedia maka akan muncul pesan error bahwa grup tidak ditemukan.
    
    ``leave [groupname]``
