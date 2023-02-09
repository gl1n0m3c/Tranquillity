//const getResourse = async(url) => {
//    const response = await fetch(url);
//    return await response.json();
//};
//
//getResourse('https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/options').then((data) => console.log(data))

async function zapros(n){
    const Requ = new Request(n)
    const Resp = await fetch(Requ);
    const D = await Resp.json()
};
function get(n){
if (n==1){
  let input1 = document.getElementById('MaxT')
  zapros('http://localhost:8000/save_temperature/'+input1)
  console.log(input1.value);
}
if (n==2){
    let input2 = document.getElementById('MaxH')
    zapros('http://localhost:8000/save_air_humidity/'+input2)
    console.log(input2.value);
}
if (n==3){
    let input3 = document.getElementById('MaxHb')
    zapros('http://localhost:8000/save_ground_humidity/'+input3)
    console.log(input3.value);
}
};
function knopki(n){
    if (n==1){
        zapros('http://localhost:8000/open_windows')
        console.log('Open Windows')}
    if (n==0){
        zapros('http://localhost:8000/close_windows')
        console.log('Close Windows')
}
}

function knopki2(n){
    if (n==1){
        zapros('http://localhost:8000/start_humidity_system')
        console.log('Start humidity system')}
    if (n==0){
        zapros('http://localhost:8000/stop_humidity_system')
        console.log('Stop humidity system')
}
}

function knopki3(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/1')
        console.log('Start wattering 1')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/1')
        console.log('Stop wattering 1')
}
}

function knopki4(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/2')
        console.log('Start wattering 2')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/2')
        console.log('Stop wattering 2')
}
}
function knopki5(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/3')
        console.log('Start wattering 3')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/3')
        console.log('Stop wattering 3')
}
}
function knopki6(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/4')
        console.log('Start wattering 4')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/4')
        console.log('Stop wattering 4')
}
}
function knopki7(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/5')
        console.log('Start wattering 5')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/5')
        console.log('Stop wattering 5')
}
}
function knopki8(n){
    if (n==1){
        zapros('http://localhost:8000/start_wattering/6')
        console.log('Start wattering 6')}
    if (n==0){
        zapros('http://localhost:8000/stop_wattering/6')
        console.log('Stop wattering 6')
}
}
