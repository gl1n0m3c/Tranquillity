const getResourse = async(url) => {
    const response = await fetch(url)
    return await response.json()
}



const m = '8000'
let k = 0
let k1 = 0
let k2 = 0
let k3 = 0
let k4 = 0
let k5 = 0
let k6 = 0
let k7 = 0
let e = 0



 function extra() {
    let e = 1
}
 


 function auto() {
    let e = 0
}



async function zapros(n){
    const Requ = new Request(n)
    const Resp = await fetch(Requ);
    const D = await Resp.json()
}



function get(n) {
    if (n==1){
        let input1 = document.getElementById('MaxT')
        zapros('http://localhost:' + m + '/save_temperature/' + input1.value)
        console.log(input1.value)
}   if (n==2){
        let input2 = document.getElementById('MaxH')
        zapros('http://localhost:' + m + '/save_air_humidity/' + input2.value)
        console.log(input2.value)
}   if (n==3){
        let input3 = document.getElementById('MaxHb')
        zapros('http://localhost:' + m + '/save_ground_humidity/' + input3.value)
        console.log(input3.value)}}



async function windows(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_window = D.message
        if (message_window == "Форточка открыта!"){             
            document.getElementById("1").classList.remove('toggle-checkbox1')
            document.getElementById("1").classList.add('toggle-checkbox')
            alert("Форточка открыта!")} 
        if (message_window == "Форточка не может быть открыта в связи со слишком малой температурой в теплице!"){    
            k = k - 1                           
            document.getElementById("1").classList.remove('toggle-checkbox')
            document.getElementById("1").classList.add('toggle-checkbox1')
            alert("Форточка не может быть открыта в связи со слишком малой температурой в теплице!")}
        if (message_window == "Сервер теплицы не отвечает!"){  
            k = k - 1                           
            document.getElementById("1").classList.remove('toggle-checkbox')
            document.getElementById("1").classList.add('toggle-checkbox1')
            alert("Сервер теплицы не отвечает!")}
        if (message_window == "Форточка закрыта!"){
            document.getElementById("1").classList.remove('toggle-checkbox1')
            document.getElementById("1").classList.add('toggle-checkbox')
            alert("Форточка закрыта!")}}



async function humidity(url){
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_humidity = D.message
        if (message_humidity == "Система увлажнения воздуха не может быть включена в связи с избыточной влажностью в теплице!"){
            k1 = k1 - 1
            document.getElementById("2").classList.remove('toggle-checkbox')
            document.getElementById("2").classList.add('toggle-checkbox1')
            alert("Система увлажнения воздуха не может быть включена в связи с избыточной влажностью в теплице!")
        }
        if (message_humidity == "Система увлажнения включена!"){
            document.getElementById("2").classList.remove('toggle-checkbox1')
            document.getElementById("2").classList.add('toggle-checkbox')
            alert("Система увлажнения включена!")
        }
        if (message_humidity == "Сервер теплицы не отвечает!"){
            k1 = k1 - 1
            document.getElementById("2").classList.remove('toggle-checkbox')
            document.getElementById("2").classList.add('toggle-checkbox1')
            alert("Сервер теплицы не отвечает!")}
        if (message_humidity == "Система увлажнения воздуха выключена!"){
            document.getElementById("2").classList.remove('toggle-checkbox1')
            document.getElementById("2").classList.add('toggle-checkbox')
            alert("Система увлажнения воздуха выключена!")}}



async function borozdka1(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_1 = D.message
        if (message_ground_1 == "Система полива бороздки включена!"){
            document.getElementById("3").classList.remove('toggle-checkbox1')
            document.getElementById("3").classList.add('toggle-checkbox')
            alert("Система полива первой бороздки включена!")}
        if (message_ground_1 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
            k2 = k2 - 1
            document.getElementById("3").classList.remove('toggle-checkbox')
            document.getElementById("3").classList.add('toggle-checkbox1')
            alert("Система полива не может быть включена в связи с избыточной влажностью в первой бороздке!")
        }
        if (message_ground_1 == "Сервер теплицы не отвечает!"){
            k2 = k2 - 1
            document.getElementById("3").classList.remove('toggle-checkbox')
            document.getElementById("3").classList.add('toggle-checkbox1')
            alert("Сервер теплицы не отвечает")}
        if (message_ground_1 == "Система полива бороздки выключена!"){
            document.getElementById("3").classList.remove('toggle-checkbox1')
            document.getElementById("3").classList.add('toggle-checkbox')
            alert("Система полива первой бороздки выключена!")}}



async function borozdka2(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_2 = D.message
    if (message_ground_2 == "Система полива бороздки включена!"){
        document.getElementById("4").classList.remove('toggle-checkbox1')
        document.getElementById("4").classList.add('toggle-checkbox')
        alert("Система полива второй бороздки включена!")}
    if (message_ground_2 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
        k3 = k3 - 1
        document.getElementById("4").classList.remove('toggle-checkbox')
        document.getElementById("4").classList.add('toggle-checkbox1')
        alert("Система полива не может быть включена в связи с избыточной влажностью во второй бороздке!")
    }
    if (message_ground_2 == "Сервер теплицы не отвечает!"){
        k3 = k3 - 1
        document.getElementById("4").classList.remove('toggle-checkbox')
        document.getElementById("4").classList.add('toggle-checkbox1')
        alert("Сервер теплицы не отвечает")}
    if (message_ground_2 == "Система полива бороздки выключена!"){
        document.getElementById("4").classList.remove('toggle-checkbox1')
        document.getElementById("4").classList.add('toggle-checkbox')
        alert("Система полива второй бороздки выключена!")}}



async function borozdka3(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_3 = D.message
    if (message_ground_3 == "Система полива бороздки включена!"){
        document.getElementById("5").classList.remove('toggle-checkbox1')
        document.getElementById("5").classList.add('toggle-checkbox')
        alert("Система полива третьей бороздки включена!")}
    if (message_ground_3 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
        k4 = k4 - 1
        document.getElementById("5").classList.remove('toggle-checkbox')
        document.getElementById("5").classList.add('toggle-checkbox1')
        alert("Система полива не может быть включена в связи с избыточной влажностью в третьей бороздке!")
    }
    if (message_ground_3 == "Сервер теплицы не отвечает!"){
        k4 = k4 - 1
        document.getElementById("5").classList.remove('toggle-checkbox')
        document.getElementById("5").classList.add('toggle-checkbox1')
        alert("Сервер теплицы не отвечает")}
    if (message_ground_3 == "Система полива бороздки выключена!"){
        document.getElementById("5").classList.remove('toggle-checkbox1')
        document.getElementById("5").classList.add('toggle-checkbox')
        alert("Система полива третьей бороздки выключена!")}}       



async function borozdka4(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_4 = D.message
    if (message_ground_4 == "Система полива бороздки включена!"){
        document.getElementById("6").classList.remove('toggle-checkbox1')
        document.getElementById("6").classList.add('toggle-checkbox')
        alert("Система полива четвертой бороздки включена!")}
    if (message_ground_4 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
        k5 = k5 - 1
        document.getElementById("6").classList.remove('toggle-checkbox')
        document.getElementById("6").classList.add('toggle-checkbox1')
        alert("Система полива не может быть включена в связи с избыточной влажностью в четвертой бороздке!")
    }
    if (message_ground_4 == "Сервер теплицы не отвечает!"){
        k5 = k5 - 1
        document.getElementById("6").classList.remove('toggle-checkbox')
        document.getElementById("6").classList.add('toggle-checkbox1')
        alert("Сервер теплицы не отвечает")}
    if (message_ground_4 == "Система полива бороздки выключена!"){
        document.getElementById("6").classList.remove('toggle-checkbox1')
        document.getElementById("6").classList.add('toggle-checkbox')
        alert("Система полива четвертой бороздки выключена!")}}



async function borozdka5(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_5 = D.message
    if (message_ground_5 == "Система полива бороздки включена!"){
        document.getElementById("7").classList.remove('toggle-checkbox1')
        document.getElementById("7").classList.add('toggle-checkbox')
        alert("Система полива пятой бороздки включена!")}
    if (message_ground_5 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
        k6 = k6 - 1
        document.getElementById("7").classList.remove('toggle-checkbox')
        document.getElementById("7").classList.add('toggle-checkbox1')
        alert("Система полива не может быть включена в связи с избыточной влажностью в пятой бороздке!")
    }
    if (message_ground_5 == "Сервер теплицы не отвечает!"){
        k6 = k6 - 1
        document.getElementById("7").classList.remove('toggle-checkbox')
        document.getElementById("7").classList.add('toggle-checkbox1')
        alert("Сервер теплицы не отвечает")}
    if (message_ground_5 == "Система полива бороздки выключена!"){
        document.getElementById("7").classList.remove('toggle-checkbox1')
        document.getElementById("7").classList.add('toggle-checkbox')
        alert("Система полива пятой бороздки выключена!")}}



async function borozdka6(url) {
    const Requ = new Request(url)
    const Resp = await fetch(Requ)
    const D = await Resp.json()
    message_ground_6 = D.message
    if (message_ground_6 == "Система полива бороздки включена!"){
        document.getElementById("8").classList.remove('toggle-checkbox1')
        document.getElementById("8").classList.add('toggle-checkbox')
        alert("Система полива шестой бороздки включена!")}
    if (message_ground_6 == "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"){
        k7 = k7 - 1
        document.getElementById("8").classList.remove('toggle-checkbox')
        document.getElementById("8").classList.add('toggle-checkbox1')
        alert("Система полива не может быть включена в связи с избыточной влажностью в шестой бороздке!")
    }
    if (message_ground_6 == "Сервер теплицы не отвечает!"){
        k7 = k7 - 1
        document.getElementById("8").classList.remove('toggle-checkbox')
        document.getElementById("8").classList.add('toggle-checkbox1')
        alert("Сервер теплицы не отвечает")}
    if (message_ground_6 == "Система полива бороздки выключена!"){
        document.getElementById("8").classList.remove('toggle-checkbox1')
        document.getElementById("8").classList.add('toggle-checkbox')
        alert("Система полива шестой бороздки выключена!")}}



function knopki(){
    k += 1
    if (k % 2 == 1){ 
        windows("http://localhost:" + m + "/open_windows")
}   if (k % 2 == 0){ 
        windows("http://localhost:" + m + "/close_windows")}}

function knopki2(){
    k1 += 1   
    if (k1 % 2 == 1){
        humidity("http://localhost:" + m + "/start_humidity_system")}
    if (k1 % 2 == 0){
        humidity("http://localhost:" + m + "/stop_humidity_system")}} 

function knopki3(){
    k2 += 1
    if (k2 % 2 == 1){
        borozdka1("http://localhost:" + m + "/start_wattering/1")}
    if (k2 % 2 == 0){
       borozdka1("http://localhost:" + m + "/stop_wattering/1")}}
 
function knopki4(){
    k3 += 1
    if (k3 % 2 == 1){
        borozdka2("http://localhost:" + m + "/start_wattering/2")}
    if (k3 % 2 == 0){
        borozdka2("http://localhost:" + m + "/stop_wattering/2")}}

function knopki5(){
    k4 += 1
    if (k4 % 2 == 1){
        borozdka3("http://localhost:" + m + "/start_wattering/3")
}   if (k4 % 2 == 0) {
        borozdka3("http://localhost:" + m + "/stop_wattering/3")}}

function knopki6(){
    k5 += 1
    if (k5 % 2 == 1){
        borozdka4("http://localhost:" + m + "/start_wattering/4")
}   if (k5 % 2 == 0){
        borozdka4("http://localhost:" + m + "/stop_wattering/4")}}

function knopki7(){
    k6 += 1
    if (k6 % 2 == 1){
        borozdka5("http://localhost:" + m + "/start_wattering/5")
}   if (k6 % 2 == 0){
        borozdka5("http://localhost:" + m + "/stop_wattering/5")}}

function knopki8(){
    k7 += 1
    if (k7 % 2 ==1){
        borozdka6("http://localhost:" + m + "/start_wattering/6")
}   if (k7 % 2 == 0){
        borozdka6("http://localhost:" + m + "/stop_wattering/6")}}
