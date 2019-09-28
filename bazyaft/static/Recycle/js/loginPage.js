
function handleLoginRequest(e) {
  const usr = document.querySelector("#username-field");
  const pass = document.querySelector("#password-field");
  const myFormData = new FormData();
  myFormData.append("username", usr.value);
  myFormData.append("password", pass.value);
  const url = "http://younes313.pythonanywhere.com/adm/AdminLogin";

  xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var json = JSON.parse(xhr.responseText);

    }
  };
  xhr.onload = function () {
  var queryString = "?token=" +JSON.parse(xhr.responseText)["token"];
  // document.cookie = "token="+JSON.parse(xhr.responseText)["token"];
  window.location.href = "RegisterDrivers.html"+queryString;
  };
  // var data = JSON.stringify(myFormData);
  var data = new Object();
  data.username = usr.value ;
  data.password = pass.value ;
  xhr.send(JSON.stringify(data));
}



const loginBtn = document.getElementById("login-btn");
loginBtn.addEventListener("click",handleLoginRequest, true )
