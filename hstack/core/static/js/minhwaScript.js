function getItcategory(){

    var category_it = document.getElementById('category_it');
    var category_meta = document.getElementById('videoMetaList');
    category_it.addEventListener('click', function(){
        var listid = document.getElementById('videoIdList').value;
        // alert(listid);
        alert(category_meta);

        //if(category_it.value == ){
            alert(category_it.value);

        //}

        

        for(var i=1; i<listid.length; i++){
            document.write(listid[i]+" ");
            
        }
    })
    
}