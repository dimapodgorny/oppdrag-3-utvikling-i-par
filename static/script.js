function quiz() {
    let score = 0;

    const svar1 = prompt("Hva er 1 + 1?");
    if (svar1 == "2") {
        score++;
    }

    const svar2 = prompt("Hva er 5 + 3?");
    if (svar2 == "8") {
        score++;
    }

    const svar3 = prompt("Hva er 10 - 4?");
    if (svar3 == "6") {
        score++;
    }

    const svar4 = prompt("Hva er 7 x 3?");
    if (svar4 == "21") {
        score++;
    }

    const svar5 = prompt("Hva er 16 ÷ 4?");
    if (svar5 == "4") {
        score++;
    }

    const resultText = "Du fikk " + score + " av 5 riktig";
    document.getElementById("result").textContent = resultText;

    fetch('/submit_result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'score=' + score
    });
}
