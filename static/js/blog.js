function showForm() {
    var form = document.getElementById('postForm');
    form.style.display = 'block'; // Show the form
    form.scrollIntoView({ behavior: 'smooth', block: 'start' }); // Scroll to the form smoothly
    document.getElementById('newPostBtn').style.display = 'none'; // Hide the button
}

function cancelPost() {
    var form = document.getElementById('postForm');
    form.style.display = 'none'; // Hide the form
    document.getElementById('newPostBtn').style.display = 'block'; // Show the button
}
