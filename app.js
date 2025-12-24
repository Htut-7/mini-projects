// function login() {
//   fetch('http://127.0.0.1:5000/login', {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({
//       email: document.getElementById('email').value,
//       password: document.getElementById('password').value
//     })
//   })
//   .then(res => res.json())
//   .then(data => alert(data.message));
// }

// function register() {
//       console.log("Register button clicked!"); // Check your console to see this

//       // 1. Get values from inputs
//       const name = document.getElementById("name").value;
//       const email = document.getElementById("email").value;
//       const password = document.getElementById("password").value;

//       // 2. Simple Validation
//       if (name === "" || email === "" || password === "") {
//         alert("Please fill in all fields");
//         return;
//       }

//       // 3. Send Data to Python Backend
//       fetch("http://127.0.0.1:5000/register", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           name: name,
//           email: email,
//           password: password
//         })
//       })
//       .then(response => response.json())
//       .then(data => {
//         console.log("Server response:", data);
//         alert(data.message);

//         // 4. If successful, go to login page
//         if (data.message === "Registered successfully") {
//           window.location.href = "login.html";
//         }
//       })
//       .catch(error => {
//         console.error("Error:", error);
//         alert("Connection failed! Make sure your Python backend is running.");
//       });
//     }
