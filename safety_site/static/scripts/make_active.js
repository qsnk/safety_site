document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll(".nav-link");
    var currentPage = window.location.pathname;
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (link.getAttribute("href") === currentPage) {
            link.classList.remove("active");
            link.classList.add("active");
        }
    }
});