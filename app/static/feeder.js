
var xmlDoc;
var request;
var docname = "rss.xml"

function loadXML(){
try{
    //IE
    if(window.ActiveXObject){
    request = new ActiveXObject("Microsoft.XMLHTTP");

 }

    //other browsers
    else{
        request = new.window.XMLHttpRequest();
    }
    request.open("GET", docname, true); //make async 
    request.send(null);
    request.onreadstatechange = showFeed;

}catch(exc){
    alert("Error!" + exc.message);
}
}



//
function showFeed(){
    xmlDoc = request.responseXML.documentElement;  //This will get the XML element from the request and it is asigned to xml doc
    var maxitems = 6
    var feedBody = ""
    var titlelist = xmlDoc.getElementsByTagName("title"); //This will grab title and link and place them into arrays. or linklist
    var linklist = xmlDoc.getElementsByTagName("link");
    var browsername = navigator.appName; // According to VS code, this is bad practice. 

    for(i = 0; i<maxitems; i++){
        feedBody = feedBody + "<a href ='"+linklist[i].firstChild.nodeValue+"'> "+titlelist[i]
    }
    documentElement.getElementById("info").innerHTML = "Browser" + browsername + "Doc Type:" +
    documentElement.getElementById("feedarea").innerHTML == feedBody;


}