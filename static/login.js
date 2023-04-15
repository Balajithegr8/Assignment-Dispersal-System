function checkLogin() {
  event.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  if (email === "root@gmail.com" && password === "rootpass") {
      alert("Login Successful!");
      document.getElementById("login-btn").style.display = "none";
      document.getElementById("streamlit-btn").style.display = "inline";
      const streamlitBtn = document.getElementById("streamlit-btn");
      streamlitBtn.style.padding = "10px";
      streamlitBtn.style.borderRadius = "25px";
      streamlitBtn.style.border = "none";
      streamlitBtn.style.backgroundColor = "#000000";
      streamlitBtn.style.color = "#fff";
      streamlitBtn.style.fontWeight = "bold";
      streamlitBtn.style.cursor = "pointer";
      streamlitBtn.style.width = "250px";
      streamlitBtn.style.height = "60px";
      streamlitBtn.style.fontSize = "20px";
      streamlitBtn.style.marginLeft = "200px";
      
  } else {
      alert("Invalid Credentials! Please enter correct Email and Password.");
  }
}
