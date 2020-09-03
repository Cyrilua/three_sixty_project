let allQuestionNumbers = [1];


function removeQuestion(idQuestion) {
    let currentQuestion = Number(idQuestion.toString().split('-')[1]);

    document.getElementById(idQuestion).remove();
    let index = allQuestionNumbers.indexOf(currentQuestion);
    if (index > -1) {
        allQuestionNumbers.splice(index, 1);
    } else {
        alert("Error index in 'removeQuestion()' !!!");
        return;
    }
    if (allQuestionNumbers.length === 0) {
        document.getElementById("done").setAttribute("disabled", "disabled");
    }
    document.getElementById("allQuestionNumbers").value = allQuestionNumbers.toString();
}

function removeOption(idOption) {
    let currentOption = Number(idOption.toString().split("-")[2]);
    let currentQuestion = Number(idOption.toString().split("-")[1]);
    let countOption = Number(document.getElementById("countOption-" + currentQuestion).value);

    if (countOption === 1) {
        alert("Error 'removeOption()' !!!");
        return;
    }
    for (let i = currentOption; i <= countOption; i++) {
        if (countOption === i) {
            document.getElementById("forOption-" + currentQuestion + "-" + i).remove();
        } else {
            document.getElementById("option-" + currentQuestion + "-" + i).value =
                document.getElementById("option-" + currentQuestion + "-" + (i + 1)).value;
        }
    }
    if (countOption === 2) {
        document.getElementById("firstOptionFromQuestion-" + currentQuestion)
            .setAttribute("class", "col-md-11");
        document.getElementById("removeIconFromFirstOption-" + currentQuestion).remove();
    }

    document.getElementById("countOption-" + currentQuestion).value = (countOption - 1).toString();
}

function addNewOption(idQuestion) {
    let currentQuestion = Number(idQuestion.toString().split('-')[1]);
    let countOption = Number(document.getElementById("countOption-" + currentQuestion).value);
    let currentOption = countOption + 1;
    let currentTypeQuestion = document.getElementById("questionType-" + currentQuestion).value;
    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "row");
    newDiv.setAttribute("style", "margin-bottom: 10px");
    newDiv.setAttribute("id", "forOption-" + currentQuestion + "-" + currentOption);
    let htmlCode = "<div class='col-md-1'>" +
        "<div class='form-check'>";
    if (currentTypeQuestion === "radio") {
        htmlCode += "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>";
    } else if (currentTypeQuestion === "checkbox") {
        htmlCode += "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='checkbox' class='form-check-input' disabled>"
    } else {
        alert("Error 'addNewOption()' !!!");
        return;
    }

    newDiv.innerHTML = htmlCode +
        "</div>" +
        "</div>" +
        "<div class='col-md-10'>" +
        "<input type='text' class='form-control' name='option-" + currentQuestion + "-" + currentOption + "' id='option-" + currentQuestion + "-" + currentOption + "' placeholder='Вариант " + currentOption + "' required>" +
        "</div>" +
        "<div class='col-md-1' style='margin-top: 6px; margin-left: -15px'>" +
        "<div>" +
        "<button form='' onclick=\"removeOption('option-" + currentQuestion + "-" + currentOption + "');\" style='border-width: 0; background: #fafafa; outline: none'><i class='fas fa-times'></i></button>" +
        "</div>" +
        "</div>";

    document.getElementById("addNewOption-" + currentQuestion).insertAdjacentElement("beforebegin", newDiv);

    if (countOption === 1 && currentOption === 2) {
        document.getElementById("firstOptionFromQuestion-" + currentQuestion).setAttribute("class", "col-md-10");
        let removeDiv = document.createElement("div");
        removeDiv.setAttribute("class", "col-md-1");
        removeDiv.setAttribute("style", "margin-top: 6px; margin-left: -15px");
        removeDiv.setAttribute("id", "removeIconFromFirstOption-" + currentQuestion);
        removeDiv.innerHTML = "<div>" +
            "<button form='' onclick=\"removeOption('option-" + currentQuestion + "-1');\" style='border-width: 0; background: #fafafa; outline: none'><i class='fas fa-times'></i></button>" +
            "</div>";
        document.getElementById("firstOptionFromQuestion-" + currentQuestion).insertAdjacentElement("afterend", removeDiv);
    }

    document.getElementById("option-" + currentQuestion + "-" + currentOption).focus();
    document.getElementById("countOption-" + currentQuestion).value = currentOption.toString();
}

function addNewQuestion() {
    let lastQuestionNumber = document.getElementById("lastQuestionNumber").value;
    let newDiv = document.createElement("div");
    let currentQuestion = Number(lastQuestionNumber) + 1;
    newDiv.setAttribute("class", "form-group");
    newDiv.setAttribute("id", "newQuestion-" + currentQuestion);
    newDiv.innerHTML =
        // "<h5>Вопрос " + currentQuestion + "</h5>" +
        "<input type='hidden' id='countOption-" + currentQuestion + "' name='countOption-" + currentQuestion + "' value='1'>" +
        "<div class='row'>" +
        "<div class='col-md-6'>" +
        // "<input id='questionName-" + currentQuestion + "' name='questionName-" + currentQuestion + "' type='text' class='form-control' placeholder='Вопрос' required>" +
        "<textarea id='questionName-" + currentQuestion + "' name='questionName-" + currentQuestion + "' class='form-control' rows='1' style='resize: none; overflow-y: hidden' oninput='countLines(this);' placeholder='Вопрос'></textarea>" +
        "</div>" +
        "<div class='col-md-6'>" +
        "<select class='form-control' id='questionType-" + currentQuestion + "' name='questionType-" + currentQuestion + "' onchange='changeTypeQuestion(\"optionsAnswer-" + currentQuestion + "\", \"questionType-" + currentQuestion + "\")'>" +
        "<option value='radio'>Один из списка</option>" +
        "<option value='checkbox'>Несколько из списка</option>" +
        "<option value='range'>Шкала</option>" +
        "<option value='small_text'>Короткий текст</option>" +
        "<option value='big_text'>Длинный текст</option>" +
        "</select>" +
        "</div>" +
        "</div>" +
        "<br>" +
        "<div class='row'>" +
        "<div class='col-md-12' id='optionsAnswer-" + currentQuestion + "'>" +
        "<div class='row' style='margin-bottom: 10px' id='forOption-" + currentQuestion + "-1'>" +
        "<div class='col-md-1'>" +
        "<div class='form-check'>" +
        "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>" +
        "</div>" +
        "</div>" +
        "<div class='col-md-11' id='firstOptionFromQuestion-" + currentQuestion + "'>" +
        "<input type='text' class='form-control' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
        "</div>" +
        "</div>" +
        "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
        "<div class='col-md-1'>" +
        "<div class='form-check'>" +
        "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>" +
        "</div>" +
        "</div>" +
        "<div class='col-md-11' style='margin-top: 5px'>" +
        "<button form='' onclick=\"addNewOption('newQuestion-" + currentQuestion + "');\"  style='border-width: 0; background: #fafafa; outline: none'>Добавить другой вариант</button>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "<div class='row'>" +
        "<div class='col-md-8'></div>" +
        "<div class='col-md-4' style='margin-top: 7px'>" +
        "<button id='removeQuestion-" + currentQuestion + "' form='' onclick=\"removeQuestion('newQuestion-" + currentQuestion + "');\" style='border-width: 0; background: #fafafa; outline: none'>" +
        "<i class='far fa-trash-alt' style='transform: scale(1.3)' data-toggle='tooltip' data-placement='right' data-trigger='hover' title='Удалить вопрос'></i>" +
        "</button>" +
        "</div>" +
        "</div>" +
        "<hr>";

    document.getElementById("newPoll").insertAdjacentElement("beforeend", newDiv);
    document.getElementById("questionName-" + currentQuestion).focus();
    document.getElementById("lastQuestionNumber").value = currentQuestion.toString();
    allQuestionNumbers.push(currentQuestion);
    if (allQuestionNumbers.length !== 0) {
        document.getElementById("done").removeAttribute("disabled");
    }
    document.getElementById("allQuestionNumbers").value = allQuestionNumbers.toString();
}

function changeTypeQuestion(idDiv, idSelected) {
    let oldDiv = document.getElementById(idDiv);
    let typeQuestion = document.getElementById(idSelected).value;
    let newDiv = document.createElement("div");
    let currentQuestion = idDiv.toString().split("-")[1];
    newDiv.setAttribute("id", idDiv);
    newDiv.setAttribute("class", "col-md-12");

    if (typeQuestion === "radio") {
        newDiv.innerHTML = "<div class='row' style='margin-bottom: 10px' id='forOption-" + currentQuestion + "-1'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='radio' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11' id='firstOptionFromQuestion-" + currentQuestion + "'>" +
            "<input class='form-control' type='text' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
            "</div>" +
            "</div>" +
            "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='radio' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11' style='margin-top: 5px'>" +
            "<button form='' onclick=\"addNewOption('newQuestion-" + currentQuestion + "');\" style='border-width: 0; background: #fafafa; outline: none'>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "checkbox") {
        newDiv.innerHTML = "<div class='row' style='margin-bottom: 10px' id='forOption-" + currentQuestion + "-1'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'  id='firstOptionFromQuestion-" + currentQuestion + "'>" +
            "<input class='form-control' type='text' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
            "</div>" +
            "</div>" +
            "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11' style='margin-top: 5px'>" +
            "<button form='' onclick=\" addNewOption('newQuestion-" + currentQuestion + "');\" style='border-width: 0; background: #fafafa; outline: none'>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "range") {
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-4'>" +
            "<label for='min-" + currentQuestion + "'>Мин. значение</label>" +
            "<input type='number' class='form-control' name='min-" + currentQuestion + "' id='min-" + currentQuestion + "' min='0' max='1' value='0'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='max-" + currentQuestion + "'>Макс. значение</label>" +
            "<input type='number' class='form-control' name='max-" + currentQuestion + "' id='max-" + currentQuestion + "' min='2' max='100' value='10'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='step-" + currentQuestion + "'>Шаг</label>" +
            "<input type='number' class='form-control' name='step-" + currentQuestion + "' id='step-" + currentQuestion + "' min='1' max='10' value='1'>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "small_text") {
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-6'>" +
            "<input type='text' class='form-control' name='smallText-" + currentQuestion + "' id='smallText-" + currentQuestion + "' placeholder='Короткий ответ (50 символов)' disabled>" +
            "</div>" +
            "</div> ";
    } else if (typeQuestion === "big_text") {
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-10'>" +
            "<input type='text' class='form-control' name='bigText-" + currentQuestion + "' id='bigText-" + currentQuestion + "' placeholder='Длинный ответ (500 символов)' disabled>" +
            "</div>" +
            "</div> ";
    } else {
        alert("Error 'changeTypeQuestion()' !!!");
        return;
    }

    let parentDiv = oldDiv.parentNode;
    parentDiv.replaceChild(newDiv, oldDiv);
    document.getElementById("countOption-" + currentQuestion).value = "1";
}

function countLines(el) {
    el.style.height = '1px';
    el.style.height = (el.scrollHeight) + 'px';
}