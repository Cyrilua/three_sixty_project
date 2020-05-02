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

function addNewQuestion() {

}

function viewOptionsAnswers(idDiv, idSelected) {
    let oldDiv = document.getElementById(idDiv);
    let typeQuestion = document.getElementById(idSelected).value;
    // alert(typeQuestion);
    let newDiv = document.createElement("div");
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
            "<div class='col-md-11'>" +
            "<input class='form-control' type='text' name='option-1-1' id='radio-1-1' placeholder='Вариант 1'>" +
            "</div>" +
            "</div>" +
            "<div class='row'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='radio' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'>" +
            "<button form='' class='btn' onclick=''>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "checkbox") {
        newDiv.innerHTML = "<div class='row' style='margin-bottom: 10px'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'>" +
            "<input class='form-control' type='text' name='option-1-1' id='checkbox-1-1' placeholder='Вариант 1'>" +
            "</div>" +
            "</div>" +
            "<div class='row'>" +
            "<div class='col-md-1'>" +
            "<div class='form-check'>" +
            "<input style='right: -10px; bottom: -25px; transform: scale(1.7);' type='checkbox' class='form-check-input' disabled>" +
            "</div>" +
            "</div>" +
            "<div class='col-md-11'>" +
            "<button form='' class='btn' onclick=''>Добавить другой вариант</button>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "range") {
        // alert("range");
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-4'>" +
            "<label for='min'>Минимальное значение</label>" +
            "<input type='number' class='form-control' name='min' id='min' value='1'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='max'>Максимальное значение</label>" +
            "<input type='number' class='form-control' name='max' id='max' value='10'>" +
            "</div>" +
            "<div class='col-md-4'>" +
            "<label for='step'>Шаг</label>" +
            "<input type='number' class='form-control' name='step' id='step' min='0' value='1'>" +
            "</div>" +
            "</div>";
    } else if (typeQuestion === "small_text") {
        // alert("small_text");
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-6'>" +
            "<input type='text' class='form-control' placeholder='Короткий ответ (50 символов)' disabled>" +
            "</div>" +
            "</div> ";
    } else if (typeQuestion === "big_text") {
        // alert("big_text");
        newDiv.innerHTML = "<div class='row'>" +
            "<div class='col-md-10'>" +
            "<input type='text' class='form-control' placeholder='Длинный ответ (500 символов)' disabled>" +
            "</div>" +
            "</div> ";
    }

    let parentDiv = oldDiv.parentNode;
    parentDiv.replaceChild(newDiv, oldDiv);
}