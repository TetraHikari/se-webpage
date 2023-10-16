// document.addEventListener("DOMContentLoaded", function() {
//     const loginButton = document.getElementById('loginButton');
//     const emailInput = document.getElementById('emailInput');
//     const passwordInput = document.getElementById('passwordInput');

//     loginButton.addEventListener('click', async () => {
//         const email = emailInput.value.trim();
//         const password = passwordInput.value.trim();
//         console.log(email);
//         console.log(password)


//         if (!email || !password) {
//             alert('Please provide both email and password.');
//             return;
//         }

//         const requestData = {
//             username: email,
//             password: password
//         };

//         try {
//             const response = await fetch('/login', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify(requestData)
//             });

//             if (response.status === 200) {
//                 // Handle successful login, e.g., redirecting to another page
//                 window.location.href = "/dashboard"; // replace with your success route
//             } else {
//                 // Handle unsuccessful login, e.g., show an error message
//                 alert('Incorrect email or password');
//             }
//         } catch (error) {
//             console.error("There was an error logging in:", error);
//         }
//     });
// });
