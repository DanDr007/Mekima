var videoWidth = 320;
var videoHeight = 240;
var videoTag = document.getElementById('theVideo');
var canvasTag = document.getElementById('theCanvas');
var csrf = document.getElementsByName("csrfmiddlewaretoken")
var msg = document.getElementById("message")

function getCookie(c_name) {
  if(document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if(c_start != -1) {
          c_start = c_start + c_name.length + 1;
          c_end = document.cookie.indexOf(";", c_start);
          if(c_end == -1) c_end = document.cookie.length;
          return unescape(document.cookie.substring(c_start,c_end));
      }
  }
  return "";
}

videoTag.setAttribute('width', videoWidth);
videoTag.setAttribute('height', videoHeight);
canvasTag.setAttribute('width', videoWidth);
canvasTag.setAttribute('height', videoHeight);
window.onload = () => {
  navigator.mediaDevices.getUserMedia({
  audio: false,
  video: {
    width: videoWidth,
    height: videoHeight
  }}).then(stream => {
    videoTag.srcObject = stream;
  }).catch(e => {
    document.getElementById('errorTxt').innerHTML = 'ERROR: ' + e.toString();
  });
  var canvasContext = canvasTag.getContext('2d');
  window.onkeydown =  (e) => {
    canvasContext.drawImage(videoTag, 0, 0, videoWidth, videoHeight);
    var data = canvasTag.toDataURL("image/png")
    console.log("presionada: "+e.key)
    $.ajax({
      headers:{
        "X-CSRFToken": getCookie("csrftoken")
      },
      type: 'POST',
      url: '/normal-cam/',
      data: {
        imagen: data,
        letra: e.key
      },
      dataType: 'json',
      success: function (response) {
        document.getElementById("message").innerHTML = response.msg
        document.getElementById("estado").innerHTML = response.estado
      }
    })
  };
};