document.addEventListener('DOMContentLoaded', function() {
    var today = new Date();
    var options = { weekday: 'long', month: 'long', day: 'numeric' };
    var time = today.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    var formattedTime = time.replace(/ /g, '');
    var formattedDate = today.toLocaleDateString('en-US', options);

    // Custom format: "Wednesdays, 15 November 4:00pm"
    formattedDate = formattedDate.replace(/day,/, 'days,');
    formattedDate = formattedDate + " " + formattedTime;
    
    var dateContainer = document.getElementById('todayDate');
    if (dateContainer) {
        dateContainer.textContent = formattedDate;
    }
});