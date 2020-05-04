function copyText(el) {
    let $tmp = $("<input>");
    $("body").append($tmp);
    $tmp.val($(el).text()).select();
    document.execCommand("copy");
    $tmp.remove();
}

function updateTextForRange(el1, el2) {
    let range = document.getElementById(el1);
    let label = document.getElementById(el2);
    label.innerText = range.value;
}

function getCounterSymbols(el1, el2) {
    let text = document.getElementById(el1);
    let counter = document.getElementById(el2);
    counter.innerText = (500 - text.value.length).toString();
}

function addNewOption(idQuestion) {
    let currentQuestion = Number(idQuestion.toString().split('-')[1]);
    let countOption = Number(document.getElementById("countOption-" + currentQuestion).value);
    let currentOption = countOption + 1;
    let currentTypeQuestion = document.getElementById("questionType-" + currentQuestion).value;
    let newDiv = document.createElement("div");
    newDiv.setAttribute("class", "row");
    newDiv.setAttribute("style", "margin-bottom: 10px");
    let htmlCode = "<div class='col-md-1'>" +
        "<div class='form-check'>";
    if (currentTypeQuestion === "radio") {
        htmlCode += "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>";
    } else if (currentTypeQuestion === "checkbox") {
        htmlCode += "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='checkbox' class='form-check-input' disabled>"
    } else {
        alert("Error!");
    }
    newDiv.innerHTML = htmlCode +
        "</div>" +
        "</div>" +
        "<div class='col-md-10'>" +
        "<input type='text' class='form-control' name='option-" + currentQuestion + "-" + currentOption + "' id='option-" + currentQuestion + "-" + currentOption + "' placeholder='Вариант " + currentOption + "' required>" +
        "</div>" +
        "<div class='col-md-1' style='left: -10px'>" +
        "<div>" +
        "<button class='btn' form='' onclick='' style='size: 10px'><i class='fas fa-times'></i></button>" +
        "</div>" +
        "</div>";

    document.getElementById("addNewOption-" + currentQuestion).insertAdjacentElement("beforebegin", newDiv);
    document.getElementById("countOption-" + currentQuestion).value = currentOption.toString();
}

function addNewQuestion() {
    let countQuestion = document.getElementById("countQuestion").value;
    let newDiv = document.createElement("div");
    let currentQuestion = Number(countQuestion) + 1;
    newDiv.setAttribute("class", "form-group");
    newDiv.setAttribute("id", "newQuestion-" + currentQuestion);
    newDiv.innerHTML = "<h5>Вопрос " + currentQuestion + "</h5>" +
        "<input type='hidden' id='countOption-" + currentQuestion + "' name='countOption-" + currentQuestion + "' value='1'>" +
        "<div class='row'>" +
        "<div class='col-md-6'>" +
        "<input id='questionName-" + currentQuestion + "' name='questionName-" + currentQuestion + "' type='text' class='form-control' placeholder='Вопрос' required>" +
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
        "<div class='row' style='margin-bottom: 10px'>" +
        "<div class='col-md-1'>" +
        "<div class='form-check'>" +
        "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>" +
        "</div>" +
        "</div>" +
        "<div class='col-md-10'>" +
        "<input type='text' class='form-control' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
        "</div>" +
        "<div class='col-md-1' style='left: -10px'>" +
        "<div>" +
        "<button class='btn' form='' onclick='' style='size: 10px'><i class='fas fa-times'></i></button>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
        "<div class='col-md-1'>" +
        "<div class='form-check'>" +
        "<input style='right: -10px; bottom: -25px; transform: scale(1.7); opacity: 0.9;' type='radio' class='form-check-input' disabled>" +
        "</div>" +
        "</div>" +
        "<div class='col-md-11'>" +
        "<button class='btn' form='' onclick='addNewOption(\"newQuestion-" + currentQuestion + "\")'>Добавить другой вариант</button>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "<hr>";

    document.getElementById("newPoll").insertAdjacentElement("beforeend", newDiv);
    document.getElementById("countQuestion").value = currentQuestion.toString();
}

function changeTypeQuestion(idDiv, idSelected) {
    let oldDiv = document.getElementById(idDiv);
    let typeQuestion = document.getElementById(idSelected).value;
    let newDiv = document.createElement("div");
    let currentQuestion = idDiv.toString().split("-")[1];
    newDiv.setAttribute("id", idDiv);
    newDiv.setAttribute("class", "col-md-12");
    // if (typeQuestion === "radio" || typeQuestion === "checkbox") {
    //     let newInput;
    //     let icon = document.createElement("input");
    //     icon.setAttribute("class", "form-check-input");
    //     icon.setAttribute("disabled", "true");
    //     icon.setAttribute("checked", "");
    //     newInput = document.createElement("input");
    //     newInput.setAttribute("class", "form-control");
    //     newInput.setAttribute("type", "text");
    //     newInput.setAttribute("name", "option-1-1");
    //     newInput.setAttribute("placeholder", "Вариант 1");
    //     if (typeQuestion === "radio") {
    //         newInput.setAttribute("id", "radio-1-1");
    //         icon.setAttribute("type", "radio");
    //     } else if (typeQuestion === "checkbox") {
    //         newInput.setAttribute("id", "checkbox-1-1");
    //         icon.setAttribute("type", "checkbox");
    //     }
    //     let buttonAddOption = document.createElement("button");
    //     buttonAddOption.setAttribute("form", "");
    //     buttonAddOption.setAttribute("class", "btn");
    //     buttonAddOption.setAttribute("onclick", "");
    //     buttonAddOption.innerText = "Добавить другой вариант";
    //
    //     newDiv.appendChild(icon);
    //     newDiv.appendChild(newInput);
    //     newDiv.appendChild(buttonAddOption);
    if (typeQuestion === "radio") {
        newDiv.innerHTML = "<div class='row' style='margin-bottom: 10px'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='radio' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-10'>" +
            "<input class='form-control' type='text' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
            "</div>" +
            "<div class='col-md-1' style='left: -10px'>" +
            "<div>" +
            "<button class='btn' form='' onclick='' style='size: 10px'><i class='fas fa-times'></i></button>" +
            "</div>" +
            "</div>" +
            "</div>" +
            "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='radio' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'>" +
            "<button form='' class='btn' onclick='addNewOption(\"newQuestion-" + currentQuestion + "\")'>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "checkbox") {
        newDiv.innerHTML = "<div class='row' style='margin-bottom: 10px'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-10'>" +
            "<input class='form-control' type='text' name='option-" + currentQuestion + "-1' id='option-" + currentQuestion + "-1' placeholder='Вариант 1' required>" +
            "</div>" +
            "<div class='col-md-1' style='left: -10px'>" +
            "<div>" +
            "<button class='btn' form='' onclick='' style='size: 10px'><i class='fas fa-times'></i></button>" +
            "</div>" +
            "</div>" +
            "</div>" +
            "<div class='row' id='addNewOption-" + currentQuestion + "'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'>" +
            "<button form='' class='btn' onclick='addNewOption(\"newQuestion-" + currentQuestion + "\")'>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "range") {
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-4'>" +
            "<label for='min'>Минимальное значение</label>" +
            "<input type='number' class='form-control' name='min-" + currentQuestion + "' id='min-" + currentQuestion + "' min='0' max='1' value='0'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='max'>Максимальное значение</label>" +
            "<input type='number' class='form-control' name='max-" + currentQuestion + "' id='max-" + currentQuestion + "' min='2' max='100' value='10'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='step'>Шаг</label>" +
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
        alert("Error!");
    }

    let parentDiv = oldDiv.parentNode;
    parentDiv.replaceChild(newDiv, oldDiv);
    document.getElementById("countOption-" + currentQuestion).value = "1";
}