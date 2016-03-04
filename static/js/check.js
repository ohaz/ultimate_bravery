function checkImage(image){
    console.log(image);
    var selected =" element-selected"
    if (image.className.indexOf(selected) == -1){
        image.className += selected;
    }else{
        image.className = image.className.replace(selected, "");
        console.log(image.className)
    }

}