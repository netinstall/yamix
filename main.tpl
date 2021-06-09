<html>
<head>

  <link rel="stylesheet" href="/static/main.css">
  <link rel="stylesheet" href="/static/button.css">
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
  <script type="text/javascript">
    function shuffle() {
      document.getElementById("shuffle-button").src="./static/shuffle-dark.png"
      document.getElementById("tracks").innerHTML="<div class='shuffling'>mixing</div>"
    $.get('/shuffle').done(function(data) {

  document.getElementById("tracks").innerHTML=data
  document.getElementById("shuffle-button").src="./static/shuffle.png"
  document.getElementById("playlist_button").style.visibility="visible"

});


}
  </script>

</head>
<body>
<center>
<img onClick="shuffle()" src="./static/shuffle.png" id="shuffle-button">

<div class="playlist_button" id="playlist_button">
<a href="https://music.yandex.ru/users/netinstall/playlists/{{playlist_id}}">
  <button class="button2 button2_rounded">
    <span class="button2__label">Слушать</span>
  </button>
</a>
</div>

<div id="tracks" class="tracks">
</div>

</center>
</body>
</html>
