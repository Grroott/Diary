function viewPassword() {
    var x = document.getElementById("view-pwd");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
    var x = document.getElementById("view-pwd1");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

