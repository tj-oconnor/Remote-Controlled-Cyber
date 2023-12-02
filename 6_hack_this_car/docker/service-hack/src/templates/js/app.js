// Select event pane
var eventPane = document.getElementById("event-log-pane").getElementsByTagName("p")[0];

// Define movement button functionality
var lights_on = false;
function move (direction) {
    var data = {direction: direction};
    
    if (direction == "lights") {
        if (lights_on) {
            data = {direction: "lights_off"};
            lights_on = false;
        }
        else {
            data = {direction: "lights_on"};
            lights_on = true;
        }
    }
    
    fetch("/movement/", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => {res.text().then(text => {
        eventPane.textContent += "\n" + text;
    })});
}

// Collapsible help dialog
var coll = document.getElementsByClassName("collapsible");
for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = document.getElementById("help-dialog");
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.width = (document.body.clientWidth / 3) + "px";
            content.style.maxHeight = content.scrollHeight + "px";
        } 
    });
}

// Define button listeners
var sendButtons = document.getElementsByClassName("flag-input-button");
for (let i = 0; i < sendButtons.length; i++) {
    sendButtons[i].addEventListener("click", function() {
        var motor = this.parentNode.id;
        var inputBox = this.parentNode.getElementsByClassName("flag-input-text")[0];
        var flag = inputBox.value;
        var indicator = this.parentNode.getElementsByTagName("p")[0];
        
        var data = {motor: motor, flag: flag};
        fetch("/flag-auth/", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(res => {res.text().then(text => {
            if (text == "flag_correct") {
                indicator.style.backgroundColor = "#11bb11";
                indicator.textContent = indicator.textContent.substring(0, indicator.textContent.indexOf(":")) + ": ENABLED";
                eventPane.textContent += "\n" + "Correct flag submitted";
                inputBox.disabled = true;
                this.disabled = true;
                inputBox.value = "";
            } else {
                eventPane.textContent += "\n" + "Incorrect flag submitted";
            }
        })});
    });
}

// Initial cookie check for indicator styles
var indFL = document.getElementById("forward-movement").getElementsByTagName("p")[0];
var indFR = document.getElementById("left-movement").getElementsByTagName("p")[0];
var indRL = document.getElementById("right-movement").getElementsByTagName("p")[0];
var indRR = document.getElementById("backward-movement").getElementsByTagName("p")[0];

fetch("/", {method: "POST"}).then(res => res.json()).then(data => {
    console.log(data);
    if (data['forward-movement'] == "enabled") {
        indFL.style.backgroundColor = "#11bb11";
        indFL.textContent = indFL.textContent.substring(0, indFL.textContent.indexOf(":")) + ": ENABLED";
        indFL.parentElement.getElementsByClassName("flag-input-text")[0].disabled = true;
        indFL.parentElement.getElementsByClassName("flag-input-button")[0].disabled = true;
    }
    if (data['left-movement'] == "enabled") {
        indFR.style.backgroundColor = "#11bb11";
        indFR.textContent = indFR.textContent.substring(0, indFR.textContent.indexOf(":")) + ": ENABLED";
        indFR.parentElement.getElementsByClassName("flag-input-text")[0].disabled = true;
        indFR.parentElement.getElementsByClassName("flag-input-button")[0].disabled = true;
    }
    if (data['right-movement'] == "enabled") {
        indRL.style.backgroundColor = "#11bb11";
        indRL.textContent = indRL.textContent.substring(0, indRL.textContent.indexOf(":")) + ": ENABLED";
        indRL.parentElement.getElementsByClassName("flag-input-text")[0].disabled = true;
        indRL.parentElement.getElementsByClassName("flag-input-button")[0].disabled = true;
    }
    if (data['backward-movement'] == "enabled") {
        indRR.style.backgroundColor = "#11bb11";
        indRR.textContent = indRR.textContent.substring(0, indRR.textContent.indexOf(":")) + ": ENABLED";
        indRR.parentElement.getElementsByClassName("flag-input-text")[0].disabled = true;
        indRR.parentElement.getElementsByClassName("flag-input-button")[0].disabled = true;
    }
});
