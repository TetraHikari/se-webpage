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

document.getElementById('newPostBtn').addEventListener('click', function(event) {
    var reservationCount = parseInt(document.getElementById('reservationCount').textContent);
    // endtime format is 04:00 and starttime format is 16:00 (get value like 4 and 16)
    var startTime = parseInt(document.getElementById('begin-time').value);
    var endTime = parseInt(document.getElementById('end-time').value);
    var total_time = endTime - startTime;

    var newPostBtn = document.getElementById('newPostBtn');
    var formWrapper = document.getElementById('formWrapper');

    console.log("reservationCount: " + reservationCount);
    console.log("startTime: " + startTime);
    console.log("endTime: " + endTime);
    console.log("total_time: " + total_time);

    if (total_time + reservationCount > 5) {
        alert("Can't reserve more than 5");
        event.preventDefault(); // Prevent form submission
        newPostBtn.style.display = "block";
        formWrapper.style.display = "none";
        
    } else if (reservationCount > 5) {
        alert("Can't reserve more than 5");
        event.preventDefault(); // Prevent form submission
        newPostBtn.style.display = "block";
        formWrapper.style.display = "none";
    }
});

document.getElementById('reservationForm').addEventListener('submit', function(event) {
    var beginTime = document.getElementById('begin-time').value;
    var endTime = document.getElementById('end-time').value;

    // Parse the hours from the begin and end times
    var beginHour = parseInt(beginTime.split(':')[0], 10);
    var endHour = parseInt(endTime.split(':')[0], 10);

    // Calculate the difference in hours
    var diffHours = endHour - beginHour;

    // Check if the difference is greater than 5 hours
    if (diffHours > 5) {
      alert("The total reservation time cannot exceed 5 hours.");
      event.preventDefault(); // Prevent the form from submitting
    } else if (diffHours <= 0) {
      // Also prevent submitting if the end time is before the begin time or the same as the begin time
      alert("End time must be after begin time.");
      event.preventDefault();
    }
});




