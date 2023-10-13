document.querySelector('.mainpageuserlogin-login button').addEventListener('click', function() {
    const email = document.getElementById('emailInput').value; // Assuming you have an input field with id="emailInput"
    const password = document.getElementById('passwordInput').value; // Assuming you have an input field with id="passwordInput"
    console.log("helloworld")

    fetch('/login', {  // Assuming '/login' is your backend endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/dashboard';  // Redirect to dashboard or whatever page you'd like
        } else {
            alert('Invalid email or password.');  // Show an error message
        }
    });
});
