


var queryString = decodeURIComponent(window.location.search);
queryString = queryString.substring(1);
var queries = queryString.split("&");
var token = queries[0].split("=")[1];

// var token = document.cookie.split("=")[1].split(";")[0] ;

// console.log(document.cookie.split("=")[1].split(";")[0]);


  let form = document.querySelector("form");
  form.addEventListener("submit",function (ev) {
    ev.preventDefault();

    const url = "http://younes313.pythonanywhere.com/driver/DriverSignup";
    request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.setRequestHeader("Authorization", "Token "+token);
    request.onload = function () {
      let json = JSON.parse(request.responseText);
      if (json["status"] == true) {
        alert("با موفقیت ثبت شد")
      }
      else
      {
        if (json["error"]==200)
          alert("راننده با مشخصات زیر قبلا ثبت شده است")
        else
          alert("خطایی رخ داد.لطفا دوباره ثبت نام کنید")
      }
    };

    request.send(new FormData(document.querySelector("#reg-form")));

  },false);

















//
// handleFormSubmit = (event) => {
//   let formData = new FormData(document.querySelector("#reg-form"));
//   const url = "http://46.4.213.215/driver/DriverSignup";
//   const req = fetch(url, {
//     method: "POST",
//     mode: "no-cors",
//     Accept: "*/*",
//     headers: new Headers({
//       "Authorization": "Token c55b1cc3f09c5eda2017034972ff310ec9ee9c83",
//       "Content-Type": "application/json"
//     }),
//     body: formData
//   }).then(function (response) {
//         return response.json()
//       })
//       .then(function (myjson) {
//         console.log(JSON.stringify(myjson))
//       })
//   ;
//   //     .then(res => res.json()).then((myJson) => {
//   //   console.log(myJson);
//   //   console.log("Hello I'm here");
//   // });
//   event.preventDefault();
// };
// const form = document.forms.namedItem("formData");
// form.addEventListener("submit", handleFormSubmit ,  true);
