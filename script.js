const getResourse = async(url) => {
    const response = await fetch(url);
    return await response.json();
};


getResourse('https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/options').then((data) => console.log(data))


function sendForm(e){
     
    // получаем значение поля key
    var keyBox = document.search.key;
    var val = keyBox.value;
    if(val.length>5){
        alert("Недопустимая длина строки");
        e.preventDefault();
    }   
    else
        alert("Отправка разрешена");
}
 
var sendButton = document.search.send;
sendButton.addEventListener("click", sendForm);