function Quiz(questions) {
    this.score = 0;
    this.questions = questions;  // ensemble des questions
    this.questionIndex = 0; // numéro de la question
}
 
Quiz.prototype.getQuestionIndex = function() {
    return this.questions[this.questionIndex];
}

// teste si la réponse est juste
Quiz.prototype.guess = function(answer) {
    if(this.getQuestionIndex().isCorrectAnswer(answer)) {
        this.score++;
    }
 
    this.questionIndex++;
}

// teste si le quiz est fini et renvoie le nombre de questions
Quiz.prototype.isEnded = function() {
    return this.questionIndex === this.questions.length;
}
 
 
function Question(text, choices, answer) {
    this.text = text;
    this.choices = choices;
    this.answer = answer;
}
 
Question.prototype.isCorrectAnswer = function(choice) {
    return this.answer === choice;
}
  
function populate() {
    if(quiz.isEnded()) {
        showScores();
    }
    else {
        // affiche la question
        var element = document.getElementById("question");
        element.innerHTML = quiz.getQuestionIndex().text;
 
        // affiche les options de réponses
        var choices = quiz.getQuestionIndex().choices;
        for(var i = 0; i < choices.length; i++) {
            var element = document.getElementById("choice" + i);
            element.innerHTML = choices[i];
            guess("btn" + i, choices[i]);
        }
 
        showProgress();
    }
};
 
function guess(id, guess) {
    var button = document.getElementById(id);
    button.onclick = function() {
        quiz.guess(guess);
        populate();
    }
};
 
// affiche la progression dans le quiz (questions faites / nbr total de questions) 
function showProgress() {
    var currentQuestionNumber = quiz.questionIndex + 1;
    var element = document.getElementById("progress");
    element.innerHTML = "Question " + currentQuestionNumber + " of " + quiz.questions.length;
};

// affiche le score final (quand le quizz est fini)
function showScores() {
    var gameOverHTML = "<h1>Resultats</h1>";
    gameOverHTML += "<h2 id='score'> Your scores: " + quiz.score + "</h2>";
    var element = document.getElementById("quiz");
    element.innerHTML = gameOverHTML;
};
 
// creation de questions ici  : question - choix - bonnes réponses
var questions = [     
    new Question("Hyper Text Markup Language signifie ?", ["JavaScript", "XHTML","CSS", "HTML"], "HTML"), 
	new Question("Quel langage s'exécute sur le serveur ?", ["PHP", "HTML","CSS", "Tous"], "PHP"), 
	new Question("En quelle année est née Arpanet ?", ["1943", "1946","1969", "1974"], "1969"), 
];
 
// creation du quiz
var quiz = new Quiz(questions);
 
// affiche le quiz
populate();