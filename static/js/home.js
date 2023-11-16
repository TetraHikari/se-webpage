var siteWidth = 1280;
var scale = screen.width /siteWidth;
document.querySelector('meta[name="viewport"]').setAttribute('content', 'width='+siteWidth+', initial-scale='+scale+'');

function myFunction() {
    var z = document.getElementById("sideBar");
    if (z.style.display === "none") {
        z.style.display = "flex";
    } else {
        z.style.display = "none";
    }
}
