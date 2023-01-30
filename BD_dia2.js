

async function DataFetch(url) {
    const Requ = new Request(url);
    const Resp = await fetch(Requ);
    const D = await Resp.json();


    const type = 'line';                               
    let DB = {                                     
        labels: [],
        datasets: [{
            data: [],
            label: "Первый",
            borderColor: "#000000",
            fill: false}, 
        {
            data: [],
            label: "Второй",
            borderColor: "#0000FF",
            fill: false}, 
        {
            data: [],
            label: "Третий",
            borderColor: "#00FF00",
            fill: false},
        { 
            data: [],
            label: "Четвертый",
            borderColor: "#FF0000",
            fill: false}, 
        {
            data: [],
            label: "Средняя влажность",
            borderColor: "#5c0000",
            fill: false
        }]};

    const options = {                                       
        responsive: true,
            legend: {
            display: true
        },
        title: {
            display: true,
            text: 'График влажности воздуха'
        }
    };


    let key;
    for (key in D) {  
        let s = D[key].data.air;
        let time = D[key].timeAIR
        DB.labels.push(time)
    let update; 
    let count = 0; 
    let number = 0;
    for (update in s) {       
        if (s[update].id == 1 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[0].data.push(s[update].humidity)
            number += s[update].humidity
            count += 1
        } else if (s[update].id == 2 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[1].data.push(s[update].humidity)
            number += s[update].humidity
            count += 1
        } else if (s[update].id == 3 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[2].data.push(s[update].humidity)
            number += s[update].humidity
            count += 1
        } else if (s[update].id == 4 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[3].data.push(s[update].humidity)
            number += s[update].humidity
            count += 1}
    }
    DB.datasets[4].data.push(number/count)


    new Chart (document.getElementById("humidity-chart"), {type, data:DB, options})
}}


let url = 'https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/DATA';
DataFetch(URL);