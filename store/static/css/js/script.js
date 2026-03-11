
document.addEventListener("DOMContentLoaded", function(){

    const text = document.querySelector(".moving-text");

    let position = -window.innerWidth;

    function animateText(){
        position += 2;

        if(position > window.innerWidth){
            position = -text.offsetWidth;
        }

        text.style.transform = "translateX(" + position + "px)";
    }

    setInterval(animateText, 10);


    
})
