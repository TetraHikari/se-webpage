const holidays = [
  {
      hdate: "01-01-2023",
      holiday: "New Year's Day",
  },
  {
      hdate: "02-01-2023",
      holiday: "Day off for New Year's Day",
  },
  {
      hdate: "14-01-2023",
      holiday: "National Children's Day",
  },
  {
      hdate: "16-01-2023",
      holiday: "Teachers' Day",
  },
  {
      hdate: "22-01-2023",
      holiday: "Lunar New Year's Day",
  },
  {
      hdate: "23-01-2023",
      holiday: "Second Day of Lunar New Year",
  },
  {
      hdate: "24-01-2023",
      holiday: "Third Day of Lunar New Year",
  },
  {
      hdate: "06-03-2023",
      holiday: "Makha Bucha",
  },
  {
      hdate: "06-04-2023",
      holiday: "Chakri Day",
  },
  {
      hdate: "13-04-2023",
      holiday: "Songkran",
  },
  {
      hdate: "14-04-2023",
      holiday: "Songkran",
  },
  {
      hdate: "01-05-2023",
      holiday: "Labor Day",
  },
  {
      hdate: "04-05-2023",
      holiday: "Coronation Day",
  },
  {
      hdate: "05-05-2023",
      holiday: "Bridge Public Holiday",
  },
  {
      hdate: "17-05-2023",
      holiday: "Royal Ploughing Ceremony Day",
  },
  {
      hdate: "03-06-2023",
      holiday: "Visakha Bucha",
  },
  {
      hdate: "03-06-2023",
      holiday: "Queen Suthida's Birthday",
  },
  {
      hdate: "05-06-2023",
      holiday: "Day off for Visakha Bucha",
  },
  {
      hdate: "05-06-2023",
      holiday: "Day off for Queen Suthida's Birthday",
  },
  {
      hdate: "28-07-2023",
      holiday: "King Vajiralongkorn's Birthday",
  },
  {
      hdate: "31-07-2023",
      holiday: "Bridge Public Holiday",
  },
  {
      hdate: "01-08-2023",
      holiday: "Buddhist Lent Day",
  },
  {
      hdate: "12-08-2023",
      holiday: "The Queen's Birthday",
  },
  {
      hdate: "14-08-2023",
      holiday: "Day off for The Queen's Birthday",
  },
  {
      hdate: "13-10-2023",
      holiday: "Anniversary of the Death of King Bhumibol",
  },
  {
      hdate: "16-11-2023",
      holiday: "Test"
  },
  {
      hdate: "23-10-2023",
      holiday: "Chulalongkorn Day",
  },
  {
      hdate: "05-12-2023",
      holiday: "King Bhumibol's Birthday/Father's Day",
  },
  {
      hdate: "10-12-2023",
      holiday: "Constitution Day",
  },
  {
      hdate: "11-12-2023",
      holiday: "Substitute Holiday for Constitution Day",
  },
  {
      hdate: "31-12-2023",
      holiday: "New Year's Eve",
  },
];

  const calendar = document.querySelector("#calendar");
  const monthBanner = document.querySelector("#month");
  let navigation = 0;
  let clicked = null;
  let events = localStorage.getItem("events") ? JSON.parse(localStorage.getItem("events")) : [];
  const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  
  function loadCalendar() {
    const dt = new Date();
  
    if (navigation != 0) {
      dt.setMonth(new Date().getMonth() + navigation);
    }
    const day = dt.getDate();
    const month = dt.getMonth();
    const year = dt.getFullYear();
    monthBanner.innerText = `${dt.toLocaleDateString("en-us", {
      month: "long",
    })} ${year}`;
    calendar.innerHTML = "";
    const dayInMonth = new Date(year, month + 1, 0).getDate();
    const firstDayofMonth = new Date(year, month, 1);
    const dateText = firstDayofMonth.toLocaleDateString("en-us", {
      weekday: "long",
      year: "numeric",
      month: "numeric",
      day: "numeric",
    });
  
    const dayString = dateText.split(", ")[0];
    const emptyDays = weekdays.indexOf(dayString);
  
    for (let i = 1; i <= dayInMonth + emptyDays; i++) {
      const dayBox = document.createElement("div");
      dayBox.classList.add("day");
      const monthVal = month + 1 < 10 ? "0" + (month + 1) : month + 1;
      const dateVal = i - emptyDays < 10 ? "0" + (i - emptyDays) : i - emptyDays;
      const dateText = `${dateVal}-${monthVal}-${year}`;
      if (i > emptyDays) {
        dayBox.innerText = i - emptyDays;
        //Event Day
        const eventOfTheDay = events.find((e) => e.date == dateText);
        //Holiday
        const holidayOfTheDay = holidays.find((e) => e.hdate == dateText);
  
        if (i - emptyDays === day && navigation == 0) {
          dayBox.id = "currentDay";
        }
  
        if (eventOfTheDay) {
          const eventDiv = document.createElement("div");
          eventDiv.classList.add("event");
          eventDiv.innerText = eventOfTheDay.title;
          dayBox.appendChild(eventDiv);
        }
        if (holidayOfTheDay) {
          const eventDiv = document.createElement("div");
          eventDiv.classList.add("event");
          eventDiv.classList.add("holiday");
          eventDiv.innerText = holidayOfTheDay.holiday;
          dayBox.appendChild(eventDiv);
        }
        dayBox.addEventListener("click", () => {
          showModal(dateText);
        });
      } else {
        dayBox.classList.add("plain");
      }
      calendar.append(dayBox);
    }
  }
  function buttons() {
    const btnBack = document.querySelector("#btnBack");
    const btnNext = document.querySelector("#btnNext");
    const btnDelete = document.querySelector("#btnDelete");
    const btnSave = document.querySelector("#btnSave");
    const closeButtons = document.querySelectorAll(".btnClose");
    const txtTitle = document.querySelector("#txtTitle");
  
    btnBack.addEventListener("click", () => {
      navigation--;
      loadCalendar();
    });
    btnNext.addEventListener("click", () => {
      navigation++;
      loadCalendar();
    });

    closeButtons.forEach((btn) => {
      btn.addEventListener("click", closeModal);
    });
    btnDelete.addEventListener("click", function () {
      events = events.filter((e) => e.date !== clicked);
      localStorage.setItem("events", JSON.stringify(events));
      closeModal();
      updateEventBoxes();
    });
  
    btnSave.addEventListener("click", function () {
      if (txtTitle.value) {
        txtTitle.classList.remove("error");
        events.push({
          date: clicked,
          title: txtTitle.value.trim(),
        });
        txtTitle.value = "";
        localStorage.setItem("events", JSON.stringify(events));
        closeModal();
      } else {
        txtTitle.classList.add("error");
      }
      updateEventBoxes();
    });
  }
  
  const viewEventForm = document.querySelector("#viewEvent");
  const addEventForm = document.querySelector("#addEvent");
  
  function showModal(dateText) {
    closeModal();
    clicked = dateText;
    const eventOfTheDay = events.find((e) => e.date == dateText);
    if (eventOfTheDay) {
      //Event already Preset
      document.querySelector("#eventText").innerText = eventOfTheDay.title;
      viewEventForm.style.display = "block";
    } else {
      //Add new Event
      addEventForm.style.display = "block";
    }
  }
  
  //Close Modal
  function closeModal() {
    viewEventForm.style.display = "none";
    addEventForm.style.display = "none";
    clicked = null;
    loadCalendar();
  }

  function updateEventBoxes() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const formatDateString = (date) => {
        return `${date.getDate().toString().padStart(2, '0')}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getFullYear()}`;
    };

    const todayStr = formatDateString(today);
    const tomorrowStr = formatDateString(tomorrow);

    const todayEventDiv = document.getElementById('todayEvent');
    const tmrEventDiv = document.getElementById('tmrEvent');

    const todayEvents = events.filter(e => e.date === todayStr);
    const todayHolidays = holidays.filter(h => h.hdate === todayStr);

    const tmrEvents = events.filter(e => e.date === tomorrowStr);
    const tmrHolidays = holidays.filter(h => h.hdate === tomorrowStr);

    todayEventDiv.innerHTML = '';
    tmrEventDiv.innerHTML = '';

    const createListItem = (text, color) => {
        const li = document.createElement('li');
        li.textContent = text;
        li.style.color = color;
        return li;
    };

    if (todayEvents.length === 0 && todayHolidays.length === 0) {
        todayEventDiv.appendChild(createListItem('None', 'grey'));
    } else {
        todayEvents.forEach(e => {
            todayEventDiv.appendChild(createListItem(e.title, 'red'));
        });
        todayHolidays.forEach(h => {
            todayEventDiv.appendChild(createListItem(h.holiday, 'green'));
        });
    }

    if (tmrEvents.length === 0 && tmrHolidays.length === 0) {
        tmrEventDiv.appendChild(createListItem('None', 'grey'));
    } else {
        tmrEvents.forEach(e => {
            tmrEventDiv.appendChild(createListItem(e.title, 'red'));
        });
        tmrHolidays.forEach(h => {
            tmrEventDiv.appendChild(createListItem(h.holiday, 'green'));
        });
    }
}

  buttons();
  loadCalendar();
  updateEventBoxes();