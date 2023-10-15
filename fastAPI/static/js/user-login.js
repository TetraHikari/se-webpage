// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function () {
    // Find the "Login" button by its ID
    const loginButton = document.getElementById('loginButton');

    // Add a click event listener to the button
    loginButton.addEventListener('click', function () {
        // Get the input values
        const username = document.getElementById('emailInput').value;
        const password = document.getElementById('passwordInput').value;
        console.log(username);
        console.log(password);

        // Perform POST request
        fetch('/userlogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        })
        .then(response => {
            // Check if the response is a successful redirect (status code 3xx)
            if (response.ok || (response.status >= 300 && response.status < 400)) {
                // Handle successful login, e.g., redirect to a dashboard or show a success message
                window.location.href = response.url;
            } else {
                // Handle other responses, e.g., show an error message
                alert('Login failed. Please try again.');
            }
        });
    });
});
