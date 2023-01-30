

async function DataFetch(Url) {
    const Requ = new Request(Url);
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
            label: "Пятый",
            borderColor: "#822727",
            fill: false}, 
        {
            data: [],
            label: "Шестой",
            borderColor: "#05ffb4",
            fill: false
        }]};

    const options = {                                       
        responsive: true,
            legend: {
            display: true
        },
        title: {
            display: true,
            text: 'График влажности почвы'
        }
    };


    let key;
    for (key in D) {  
        let s = D[key].data.ground;
        let time = D[key].timeGROUND
        DB.labels.push(time)
    let update; 
    for (update in s) {       
        if (s[update].id == 1 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[0].data.push(s[update].humidity)
        } else if (s[update].id == 2 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[1].data.push(s[update].humidity)
        } else if (s[update].id == 3 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[2].data.push(s[update].humidity)
        } else if (s[update].id == 4 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[3].data.push(s[update].humidity)
        } else if (s[update].id == 5 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[4].data.push(s[update].humidity)
        } else if (s[update].id == 6 && typeof(s[update].humidity) != "undefined"){
            DB.datasets[5].data.push(s[update].humidity)}
        }}

    new Chart (document.getElementById("last-chart"), {type, data:DB, options})
}


let Url = 'https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/DATA';
DataFetch(URL);