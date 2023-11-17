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