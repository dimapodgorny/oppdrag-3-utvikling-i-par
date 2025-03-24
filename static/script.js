let currentQuestion = 1;
let score = 0;

function startQuiz() {
    document.getElementById("startButton").style.display = "none";
    document.getElementById("quizForm").style.display = "block";
    document.getElementById("question1").style.display = "block";
    document.getElementById("nextButton").style.display = "inline-block";
}

function nextQuestion() {
    const svar1 = document.querySelector('input[name="svar1"]:checked');
    const svar2 = document.querySelector('input[name="svar2"]:checked');
    const svar3 = document.querySelector('input[name="svar3"]:checked');
    const svar4 = document.querySelector('input[name="svar4"]:checked');
    const svar5 = document.querySelector('input[name="svar5"]:checked');

    if (currentQuestion === 1 && svar1 && svar1.value === "2") {
        score++;
    }
    if (currentQuestion === 2 && svar2 && svar2.value === "8") {
        score++;
    }
    if (currentQuestion === 3 && svar3 && svar3.value === "6") {
        score++;
    }
    if (currentQuestion === 4 && svar4 && svar4.value === "21") {
        score++;
    }
    if (currentQuestion === 5 && svar5 && svar5.value === "4") {
        score++;
    }

    document.getElementById("question" + currentQuestion).style.display = "none";

    if (currentQuestion === 5) {
        const resultText = "Du fikk " + score + " av 5 riktig";
        document.getElementById("result").textContent = resultText;

        fetch('/submit_result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'score=' + score
        });

        document.getElementById("nextButton").style.display = "none";
    } else {
        currentQuestion++;
        document.getElementById("question" + currentQuestion).style.display = "block";
    }
}
