let currentQuestion = 1;
let score = 0;

function startQuiz() {
    document.getElementById("startButton").style.display = "none";
    document.getElementById("quizForm").style.display = "block";
    document.getElementById("question1").style.display = "block";
    document.getElementById("nextButton").style.display = "inline-block";
}

function answerQuestion(answer) {
    if (currentQuestion === 1 && answer === "2") {
        score++;
    }
    if (currentQuestion === 2 && answer === "8") {
        score++;
    }
    if (currentQuestion === 3 && answer === "6") {
        score++;
    }
    if (currentQuestion === 4 && answer === "21") {
        score++;
    }
    if (currentQuestion === 5 && answer === "4") {
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
