
titleee = document.getElementById('title');

var titles = ['a', 'al', 'alF', 'alFo', 'alFor', 'alForu', 'alForum', 'alForum', 'alForum', 'alForu', 'alFor', 'alFo', 'alF', 'al', 'a'];
var indexx = 0;
function typewriteTitle(){
    titleee.textContent = titles[indexx];
    indexx = (indexx + 1) % titles.length
    setTimeout(typewriteTitle, 250)
}

typewriteTitle()