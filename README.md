# yamix

### Instalation

1. `mkdir -p /opt/yamix; cd /opt/yamix`
2. `git clone https://github.com/netinstall/yamix.git .`
3.  `virtualenv .`
4.  `./bin/pip3 install git+https://github.com/netinstall/yamix.git`

### Configuring
#### Examples:
##### /etc/yamix/config.json:
```
{
    "example.com": "/etc/yamix/example.json",
}
```

##### /etc/yamix/example.json:

```
{
  "destination": {
    "uid": 37409387,
    "playlist_id": 1028,
    "music_oauth_token": "***"
  },
  "source_playlists": [
    {
      "login": "camchatka",
      "uid": 12917571,
      "playlist_id": 1026
    },
    {
      "login": "netinstall",
      "uid": 37409387,
      "playlist_id": 3
    }
  ]
}
```
#### Retrive music_oauth_token:
https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d

#### Systemd:
```
sudo cp /opt/yamix/yamix.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable yamix.service
```
