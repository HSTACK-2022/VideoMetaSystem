function search(){
    document.search.submit();
}

// 이하 상세검색
var isPressed = false;
function onloads(){
    console.log("onloads");

    var valCategory = document.getElementById('category').value;
    var valMethod = document.getElementById('method').value;
    var valNarrative = document.getElementById('narrative').value;

    var resetBtn = document.getElementById("resetBtn");
    if (valCategory != '' || valMethod != '' || valNarrative != ''){
        resetBtn.style.visibility = 'visible';
    }

    var hidden = document.getElementsByClassName("searchHidden");
    for (var i=0; i<hidden.length; i++) {
        hidden[i].style.display = 'none';
    }
}

function visible(){
    console.log(isPressed);
    // 버튼 안눌렸다가 눌릴때 -> 상세검색 해야함
    if (!isPressed) {
        isPressed = true;
        var shownInput = document.getElementById("searchShownInput");
        var shownSubmit = document.getElementById("searchShownSubmit");
        var detailBtn = document.getElementById("showDetailBtn");

        shownInput.value = '';
        shownInput.style.display = 'none';
        if (shownSubmit != null){
            shownSubmit.style.display = 'none';
        }

        detailBtn.innerText = "▲";

        var hidden = document.getElementsByClassName("searchHidden");
        for (var i=0; i<hidden.length; i++) {
            hidden[i].style.display = '';
        }
    }
    // 버튼 눌렸다가 안눌릴때 -> 상세검색 닫기
    else {
        isPressed = false;
        document.getElementById("searchShownInput").style.display = '';
        var shownSubmit = document.getElementById("searchShownSubmit");
        var detailBtn = document.getElementById("showDetailBtn");

        if (shownSubmit != null){
            shownSubmit.style.display = '';
        }

        detailBtn.innerText = "▼";

        var hidden = document.getElementsByClassName("searchHidden");
        for (var i=0; i<hidden.length; i++) {
            hidden[i].style.display = 'none';
        }

        document.getElementById("searchTextTitle").value = '';
        document.getElementById("searchTextKeyword").value = '';
        document.getElementById("searchTextPresenter").value = '';
    }
}

// detail 페이지에서 search시 로그 기록
function writeSearchLog(pk) {
    var content = document.getElementById("searchContent").value;
    console.log(content)
    var request = new XMLHttpRequest();
    request.open('GET', `/detail/${pk}/search/${content}`);
    request.send();
    request.onload = ()=>{
        console.log(JSON.parse(request.response));
    }
}

// detail 페이지에서 open시 로그 기록
function writeOpenLog(pk, flag){
    var request = new XMLHttpRequest();
    request.open('GET', `/detail/${pk}/time/${flag}`);
    request.send();
    request.onload = ()=>{
        console.log(JSON.parse(request.response));
    }
}