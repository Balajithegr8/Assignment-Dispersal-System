function checkLogin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if (email === "root@gmail.com" && password === "rootpass") {
        alert("Login Successful!");
        window.location.href = "dashboard.html";
    } else {
        alert("Invalid Credentials! Please enter correct Email and Password.");
    }
}
