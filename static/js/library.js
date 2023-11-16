function toggleBookInfo(clickedBook) {
    const booksContainer = document.querySelector('.books-container');
    const bookInfo = clickedBook.querySelector('.book-info');
    const isBookInfoVisible = bookInfo.style.display === 'block';

    // Close any open book info
    document.querySelectorAll('.book .book-info').forEach(info => {
        info.style.display = 'none';
    });

    // Remove blur effect
    booksContainer.classList.remove('blur-effect');

    // If the clicked book info was not already visible, display it and blur the background
    if (!isBookInfoVisible) {
        bookInfo.style.display = 'block';
        booksContainer.classList.add('blur-effect');
    }
}

// Close book info when clicking on the 'Close' button or outside the book info
window.addEventListener('click', function(event) {
    const booksContainer = document.querySelector('.books-container');
    const bookInfos = document.querySelectorAll('.book .book-info');

    // Check if the clicked target is not a book-info or a child of book-info
    if (![...bookInfos].some(info => info.contains(event.target) || event.target.classList.contains('book-cover'))) {
        // Close all book infos and remove the blur
        bookInfos.forEach(info => {
            info.style.display = 'none';
        });
        booksContainer.classList.remove('blur-effect');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const confirmed = confirm('Are you sure you want to delete this book?');
            if (confirmed) {
                this.closest('form').submit();
            }
        });
    });
});


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



