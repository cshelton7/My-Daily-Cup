function toggleWidget(widget, local) {
    var wid = document.getElementById(widget)
    if (wid.style.display === "none") {
        wid.style.display = "block";
        localStorage.setItem(local, 'false');
    }
    else {
        wid.style.display = "none";
        localStorage.setItem(local, 'true');
    }
}
function toggleSettings() {
    settings = document.getElementById("settings")
    if (settings.style.display === "none") {
        settings.style.display = "block";
        localStorage.setItem("s", 'false');
    }
    else {
        settings.style.display = "none";
        localStorage.setItem("s", 'true');
    }
}
