function inputMove(time) {
    var vid = document.getElementById("video");
    timeStr = time.split(":");
    timeSec = Number(timeStr[0] * 3600) + Number(timeStr[1] * 60) + Number(timeStr[2]);
    var t = vid.currentTime;
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
            button.type = "button";
            button.addEventListener("click", function(event){
                inputMove(timeStr);
            });
            button.innerText = timeStr;
            btnTd.appendChild(button);

            const titleTd = document.createElement("td");
            tr.appendChild(titleTd);


            // 여기
            const title = document.createElement("div");
            title.className = "indexTitle";

            var regex = new RegExp(str, "g");
            line = line.replace(regex, "<span style='background-color:#FFE400;'>" + str + "</span>");

       

            title.innerHTML = line;
            
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



const zip = new JSZip();

function loadImg(folderName){
    var pptImage = document.getElementById("pptImage");
    var images = pptImage.childNodes;

    //var testdiv = document.getElementById("testdiv");

    for(var i=0, count=0; i<images.length; i++){
        if(images[i].nodeName != "IMG") continue;

        toDataURL(images.item(i).src, function(dataUrl){
            count++;
            var fileName = folderName + count.toString() + ".jpg";
            var imgFile = dataURLtoFile(dataUrl, fileName);
            zip.file(fileName, imgFile);
            //testdiv.innerText = fileName;
        });
    }
}

function toDataURL(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
    var reader = new FileReader();
    reader.onloadend = function() {
        callback(reader.result);
    }
    reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}

const dataURLtoFile = (dataurl, fileName) => {
    var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), 
        n = bstr.length, 
        u8arr = new Uint8Array(n);
        
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], fileName, {type:mime});
}

function downloadImg(folderName){
    console.log("clicked");
    var zipFileName = folderName + ".zip";
    zip.generateAsync({
        type: "blob",
        compression: "DEFLATE"
    },).then(
        function( zipContents ){
            download( zipContents, zipFileName, "application/octet-stream");
        }
    );
}

function downloadPPT(path, title){
    console.log(`hello ${path}, ${title}`);
    var element = document.createElement('form');
    element.setAttribute('method', 'GET');
    element.setAttribute('action', `http://localhost:5000/detail/download/${path}/${title}`);
    document.body.appendChild(element);
    element.submit();
    document.body.removeChild(element);
}