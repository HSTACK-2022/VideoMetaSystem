var vid = document.getElementById("video");
function inputMove(time) {
    timeStr = time.split(":");
    timeSec = Number(timeStr[0] * 3600) + Number(timeStr[1] * 60) + Number(timeStr[2]);
    vid.currentTime = timeSec;
    vid.play();
}

function searchPost(scripts) {
    var str = document.getElementById("searchContent").value;
    var parent = document.getElementById("searchResArea");
    removeAllChild(parent);
    scripts.forEach((line, index)=>{
        if (line.includes(str) && line != "ASR_NOTOKEN") {
            const tr = document.createElement("tr");
            tr.className = "metadataDetailTR";
            parent.appendChild(tr);

            const btnTd = document.createElement("td");
            tr.appendChild(btnTd);

            var timeSec = Number(index) * 10;
            var timeStr = sec2str(timeSec);

            const button = document.createElement("button");
            button.className = "indexTime";
            button.onclick = "inputMove(timeSec)";
            button.innerText = timeStr;
            btnTd.appendChild(button);

            const titleTd = document.createElement("td");
            tr.appendChild(titleTd);

            const title = document.createElement("div");
            title.className = "indexTitle";
            title.innerText = line;
            titleTd.appendChild(title);
        }
    });
}


function removeAllChild(tag){
    while (tag.hasChildNodes()) {
        tag.removeChild(tag.firstChild);
    }
}
function sec2str(sec){
    var hour = parseInt(sec / 3600);
    sec = sec % 3600;
    var min = parseInt(sec / 60);
    sec = sec % 60;

    if (hour < 10) { hour = '0' + hour; }
    if (min < 10)  { min = '0' + min; }
    if (sec < 10)  { sec = '0' + sec; }
    
    return hour + ":" + min + ":" + sec;
}