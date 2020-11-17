cd "../../server"
start "server" call "server.bat"

ping 127.0.0.1 -n 1

cd "../client"
start "client1" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client2"
start "client2" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client3"
start "client3" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client4"
start "client4" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client5"
start "client5" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client6"
start "client6" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client7"
start "client7" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client8"
start "client8" call "client.bat"

ping 127.0.0.1 -n 1

cd "../client9"
start "client9" call "client.bat"

cd "../scripts/peer_8"
call "side.bat"
