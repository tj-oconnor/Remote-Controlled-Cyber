var buttons = document.getElementsByTagName("button");
var textInput = document.getElementsByTagName("input")[0];

function submit() {
    var data = {equation: textInput.value};
    fetch("/calculator", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => {res.text().then(answer => {
        textInput.value = answer;
    })});
}

// Define button behavior
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function() {
        if (this.textContent == "=") {
            submit();
        }
        textInput.value += this.textContent;
    });
}
