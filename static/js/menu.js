
document.addEventListener('DOMContentLoaded', function() {
        var today = new Date();
        var options = { weekday: 'long', month: 'long', day: 'numeric' };
        var formattedDate = today.toLocaleDateString('en-US', options);
    
        // Custom format: "Wednesdays, 15 November"
        formattedDate = formattedDate.replace(/day,/, 'days,');
    
        var dateContainer = document.getElementById('todayDate');
        if (dateContainer) {
            dateContainer.textContent = formattedDate;
        }
});


