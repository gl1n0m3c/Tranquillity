
document.getElementById("TABLE").style.display = "none";
document.getElementById("CONFIGURATION").style.display = "block";

TABLE_SHOW.onclick = function() {
    document.getElementById("CHART").style.display = "none";
    document.getElementById("TABLE").style.display = "block";
    document.getElementById("CONFIGURATION").style.display = "none";
}

CHART_SHOW.onclick = function() {
    document.getElementById("TABLE").style.display = "none";
    document.getElementById("CHART").style.display = "block";
    document.getElementById("CONFIGURATION").style.display = "block";
} 

AIR.onclick = function() {
    document.getElementById("CONFIGURATION").style.display = "block";
    document.getElementById("chart1").style.display = "block";
    document.getElementById("chart2").style.display = "block";
    document.getElementById("chart3").style.display = "none";
    document.getElementById("chart_AVG").style.display = "none";
} 

SHOW_ALL.onclick = function() {
    document.getElementById("CONFIGURATION").style.display = "block";
    document.getElementById("chart1").style.display = "block";
    document.getElementById("chart2").style.display = "block";
    document.getElementById("chart3").style.display = "block";
    document.getElementById("chart_AVG").style.display = "block";
} 

GROUND.onclick = function() {
    document.getElementById("CONFIGURATION").style.display = "block";
    document.getElementById("chart1").style.display = "none";
    document.getElementById("chart2").style.display = "none";
    document.getElementById("chart3").style.display = "block";
    document.getElementById("chart_AVG").style.display = "none";
}

AVERAGE.onclick = function() {
    document.getElementById("CONFIGURATION").style.display = "block";
    document.getElementById("chart1").style.display = "none";
    document.getElementById("chart2").style.display = "none";
    document.getElementById("chart3").style.display = "none";
    document.getElementById("chart_AVG").style.display = "block";
}


const TagError = document.querySelector('h2');	
moment.locale('ru');						
var RowAirFragment = TableRowCreate(1+5+5);		
var RowGroundFragment = TableRowCreate(1+6);	
var coFixed = 1;
const port = "27314";
const host = "http://localhost:" + port;
var url = "30min";
var text = "???????????? ??????";


min30.onclick = function() {
    url = "30min";
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)});
}

hour1.onclick = function() {
    url = "hour";
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)});
}

hours12.onclick = function() {
    url = "12hours";
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)});
}

day1.onclick = function() {
    url = "day";
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)});
}

month1.onclick = function() {
    url = "month";
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)});
}

ChartRefresh1.onclick = function() {
    DataFetch(host + "/give_data/").catch(error => {alert(`????????????! ${error}`)})
}



var Sensor;
var Chart1;		
var Chart2; 
var Chart3;	
var Chart4;				

DataFetch(host + "/give_data/")

//???????????????????? ?????????????? ???????????? ?????????????? ?? ?????????????????? ?? ?????????????????? Columns ?????????????????????? ??????????
function TableRowCreate(Columns) {
    let RowFragment = new DocumentFragment();  //???????????? ???????????? ??????????????
    let TR = document.createElement('tr');
    for (let i=1; i <= Columns; i++) {
        TR.append(document.createElement('td'))
    }
    RowFragment.append(TR);
    return RowFragment;
}



//?????????????????????? ???????????????????? ?????????? ?? ?????????????? TableBody ???? ???????????? ???? Sensor.air. RowFragment ???????????????????????? ?????? ???????????? ???????????? ??????????????
function TableRowSetAir(TableBody, RowFragment) {
    if (Sensor.air != null || Sensor.air != undefined){
        let Delta = Sensor.air.length - TableBody.rows.length;  //?????????????? ?????????? ?????????? ?????????????? ?? ????????????????
        if (Delta < 0) {
            for (Delta = Delta; Delta < 0; Delta++) {
                TableBody.deleteRow(-1)  //?????????????? ???????????? ????????????
            }
        } else if (Delta > 0) {
            for (Delta = Delta; Delta > 0; Delta--) {
                TableBody.append(RowFragment.cloneNode(true));  //???????????????? ?????????????????????? ???????????? ?????? ?????????? ??????????????
        }}
    } else {
        alert("????????????. ???????????? ???????????? ???? ?? ???????????? ????????????")
    }
}

//?????????????????????? ???????????????????? ?????????? ?? ?????????????? TableBody ???? ???????????? ???? Sensor.ground. RowFragment ???????????????????????? ?????? ???????????? ???????????? ??????????????
function TableRowSetGround(TableBody, RowFragment) {
    if (Sensor.ground != null || Sensor.ground != undefined){
        let Delta = Sensor.ground.length - TableBody.rows.length;  //?????????????? ?????????? ?????????? ?????????????? ?? ????????????????
        if (Delta < 0) {
            for (Delta = Delta; Delta < 0; Delta++) {
                TableBody.deleteRow(-1)  //?????????????? ???????????? ????????????
            }
        } else if (Delta > 0) {
            for (Delta = Delta; Delta > 0; Delta--) {
                TableBody.append(RowFragment.cloneNode(true));  //???????????????? ?????????????????????? ???????????? ?????? ?????????? ??????????????
        }}
    } else {
        alert("????????????. ???????????? ???????????? ???? ?? ???????????? ????????????")
    }
}


// ???????????????????? ??????????????
function TableAirRefresh(TableId) {
    let TableBody = document.getElementById(TableId).tBodies[0];  //?????????????????????? ???????? ??????????????
    TableRowSetAir(TableBody, RowAirFragment);
    //?????????????????? HTML ???????????????? ?????????????? ???? Sensor.air ?????????????? ?? ???????????? ????????????
    let TableRow = TableBody.firstElementChild; // ???????????????????? tr 
    if (Sensor.air != null || Sensor.air != undefined){
        for (const Rec of Sensor.air) {  //???????? ???? ???????? ?????????????? Data.sensor
            
            TableRow.cells[0].textContent = moment(Rec.dt).format('LLLL');
            if (Rec.t1 != null){
                TableRow.cells[1].textContent = Rec.t1.toFixed(coFixed)
            } else { 
                TableRow.cells[1].textContent = text}

            if (Rec.t2 != null){
                TableRow.cells[2].textContent = Rec.t2.toFixed(coFixed)
            } else {
                TableRow.cells[2].textContent = text}

            if (Rec.t3 != null){
                TableRow.cells[3].textContent = Rec.t3.toFixed(coFixed)
            } else {
                TableRow.cells[3].textContent = text}

            if (Rec.t4 != null){
                TableRow.cells[4].textContent = Rec.t4.toFixed(coFixed)
            } else {
                TableRow.cells[4].textContent = text}
            
            if (Rec.avg_temp != null){
                TableRow.cells[5].textContent = Rec.avg_temp.toFixed(coFixed)
            } else {
                TableRow.cells[5].textContent = text}

            if (Rec.h1 != null){
                TableRow.cells[6].textContent = Rec.h1.toFixed(coFixed)
            } else {
                TableRow.cells[6].textContent = text}

            if (Rec.h2 != null){
                TableRow.cells[7].textContent = Rec.h2.toFixed(coFixed)
            } else {
                TableRow.cells[7].textContent = text}

            if (Rec.h3 != null){
                TableRow.cells[8].textContent = Rec.h3.toFixed(coFixed)
            } else {
                TableRow.cells[8].textContent = text}

            if (Rec.h4 != null){
                TableRow.cells[9].textContent = Rec.h4.toFixed(coFixed)
            } else {
                TableRow.cells[9].textContent = text}

            if (Rec.avg_hum != null){
                TableRow.cells[10].textContent = Rec.avg_hum.toFixed(coFixed)
            } else {
                TableRow.cells[10].textContent = text}

            TableRow = TableRow.nextElementSibling;
        }
    } else {
        alert("????????????. ???????????? ???????????? ???? ?? ???????????? ????????????")
    }
}



//???????????????? ?????????????? ?????????? ???? ???????????? ???? Data.ground
function TableGroundRefresh(TableId) {
    //if (document.getElementById(TableId) != undefined) { !!! } ?????????? ?????????????????
    let TableBody = document.getElementById(TableId).tBodies[0];//?????????????????????? ???????? ??????????????
    TableRowSetGround(TableBody, RowGroundFragment);
    //?????????????????? HTML ???????????????? ?????????????? ???? Sensor.ground ?????????????? ?? ???????????? ????????????
    let TableRow = TableBody.firstElementChild;
    if (Sensor.ground != null || Sensor.ground != undefined){
        for (const Rec of Sensor.ground) {  //???????? ???? ???????? ?????????????? Data.air
            TableRow.cells[0].textContent = moment(Rec.dt).format('LLLL');
            if (Rec.h1 != null){
                TableRow.cells[1].textContent = Rec.h1.toFixed(coFixed)
            } else {
                TableRow.cells[1].textContent = text}

            if (Rec.h2 != null){
                TableRow.cells[2].textContent = Rec.h2.toFixed(coFixed)
            } else {
                TableRow.cells[2].textContent = text}

            if (Rec.h3 != null){
                TableRow.cells[3].textContent = Rec.h3.toFixed(coFixed)
            } else {
                TableRow.cells[3].textContent = text}

            if (Rec.h4 != null){
                TableRow.cells[4].textContent = Rec.h4.toFixed(coFixed)
            } else {
                TableRow.cells[4].textContent = text}

            if (Rec.h5 != null){
                TableRow.cells[5].textContent = Rec.h5.toFixed(coFixed)
            } else {
                TableRow.cells[5].textContent = text}

            if (Rec.h6 != null){
                TableRow.cells[6].textContent = Rec.h6.toFixed(coFixed)
            } else {
                TableRow.cells[6].textContent = text}

            TableRow = TableRow.nextElementSibling}
    } else {
        alert("????????????. ???????????? ???????????? ???? ?? ???????????? ????????????")
    }
}




async function DataFetch(strURL) {
    // ???????????????? ?????????????????? ???? ????????????
    TagError.textContent = '';
    const Requ = new Request(strURL + url);
    const Resp = await fetch(Requ);
    Sensor = await Resp.json();
    var time_per;
    if (!Resp.ok) {  // ?????????? ?????????????? 200?
        TagError.textContent = Resp;  // ?????????????????? ???? ????????????
        return;
    }
    // ???????????????????? ??????????????
    if (Sensor.air != null || Sensor.air != undefined){
        TableAirRefresh('TableAir')}
    if (Sensor.ground != null || Sensor.ground != undefined){
        TableGroundRefresh('TableGround')}

    if  (url == "30min") {
        time_per = "minute";
    } else if (url == "hour") {
         time_per = "minute";
    } else if (url == "day") {
         time_per = "hour";
    } else if (url == "12hours") {
         time_per = "hour";
    } else if (url == "month") {
         time_per = "day";
    }
    if ((Sensor.air != null || Sensor.air != undefined) && (Sensor.ground != null || Sensor.ground != undefined)){
        if (Chart1 != undefined) {	
            Chart1.data.datasets.forEach(dataset => {
                dataset.data = Sensor.air});
            Chart1.options.scales.x.time.minUnit = time_per;
                Chart1.update("resize");			
            } else {	
                Chart1 = new Chart('chart1', {			
                    type: 'line',
                    data: {
                        datasets: [
                    {
                        label: '????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "t1"},	
                        showLine: true,
                        hidden: false,
                        lineTension: 0.3,
                        color: "#FF0000"},
                    {
                        label: '????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "t2"},
                        showLine: true,
                        hidden: true,
                        lineTension: 0.3,
                        color: "#00FF00"
                    },
                    {
                        label: '????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "t3"},
                        showLine: true,
                        hidden: true,
                        lineTension: 0.3,
                        color: "#0000FF"
                    },
                    {
                        label: '??????????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "t4"},
                        showLine: true,
                        hidden: true,
                        lineTension: 0.3,
                        color: "#FF00FF"
                    }],
            },
                options: {
                    locale: "ru-RU",
                    animation: true,
                    plugins: {
                title: {
                    display: true,
                    text: '?????????????? ??????????????????????',
                    color: "#000000"
                  },
                legend: {
                    labels: {
                        font: {
                    family: "GOST",				
                        size: 14
                        }
                      }
                    }	  
                },
                layout: {
                    padding: {
                        top: 80
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                title: {
                  display: true,
                  text: "??????????",
                color: "#000000"
                },
                    time: {
                isoWeekday: true,
                minUnit: time_per,
                displayFormats: {					
                    minute: 'D MMM HH:mm',
                    hour: 'D MMM HH ??????????',
                    day: 'D MMM'}
                },
                ticks: {
                        autoSkip: true,
                        maxTicksLimit: 20,
                        maxRotation: 60,
                        minRotation: 30,
                        source: "data",
                        color: "black",
                    display: true,
                        font: {
                  },
                    },
                    grid: {
                        drawTicks: true,
                        borderColor: "black",
                  enabled: true,
                  drawTicks: true,
                  lineWidth: 1,					
                    },
                  },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                border: {
                  color: "#000000",
                },
                    ticks: {
                        color: "#000000",
                },
                title: {
                  display: true,
                  color: "#000000",
                    text: "??????????????????????",
                },  
                grid: {
                    color: "#000000",
                    }
                }}}});
            Chart1.update();
            }	

        if (Chart2 != undefined) {
            Chart2.data.datasets.forEach(dataset => {
                dataset.data = Sensor.air});
                Chart2.options.scales.x.time.minUnit = time_per;
                Chart2.update("resize");			
            } else {
                Chart2 = new Chart('chart2', {			
                type: 'line',
                data: {
                    datasets: [
                {
                    label: '????????????',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h1"},	
                    showLine: true,
                    hidden: false,
                    lineTension: 0.3,
                    color: "#FF0000"},
                {
                    label: '????????????',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h2"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#00FF00"
                },
                {
                    label: '????????????',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h3"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#0000FF"
                },
                {
                    label: '??????????????????',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h4"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#FF00FF"
                }],
        },
            options: {
                locale: "ru-RU",
                animation: true,
                plugins: {
            title: {
                display: true,
                text: '?????????????? ?????????????????? ??????????????',
                color: "#000000"
              },
            legend: {
                labels: {
                    font: {
	            family: "GOST",				
                    size: 14
                    }
                  }
                }	  
            },
            layout: {
                padding: {
                    top: 80
                }
            },
            scales: {
                x: {
                    type: 'time',
	        title: {
  	        display: true,
  	        text: "??????????",
            color: "#000000"
	        },
                time: {
	        isoWeekday: true,
	        minUnit: time_per,
            displayFormats: {				
                minute: 'D MMM HH:mm',
                hour: 'D MMM HH ??????????',
                day: 'D MMM'}},
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 20,
                    maxRotation: 60,
                    minRotation: 30,
                    source: "data",
                    color: "black",
	            display: true,
                    font: {
	          },
                },
                grid: {
                    drawTicks: true,
                    borderColor: "black",
	        enabled: true,
	        drawTicks: true,
	        lineWidth: 1,					
                },
              },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
	        border: {
  	        color: "#000000",
	        },
                ticks: {
                    color: "#000000",
	        },
	        title: {
  	        display: true,
  	        color: "#000000",
	            text: "??????????????????????",
	        },  
            grid: {
                color: "#000000",
                }
            }}}});
        Chart2.update();
        }


        if (Chart3 != undefined) {
            Chart3.data.datasets.forEach(dataset => {
                dataset.data = Sensor.ground});
                Chart3.options.scales.x.time.minUnit = time_per;
                Chart3.update("resize");		
            } else {
                Chart3 = new Chart('chart3', {			
                type: 'line',
                data: {
                    datasets: [
                {
                    label: '????????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h1"},	
                    showLine: true,
                    hidden: false,
                    lineTension: 0.3,
                    color: "#FF0000"},
                {
                    label: '????????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h2"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#00FF00"
                },
                {
                    label: '????????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h3"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#0000FF"
                },
                {
                    label: '??????????????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h4"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#FF00FF"
                },
                {
                    label: '??????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h5"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#FF00FF"
                },
                {
                    label: '????????????',
                    data: Sensor.ground,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "h6"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#FF00FF"
                }],
        },
            options: {
                locale: "ru-RU",
                animation: true,
                plugins: {
            title: {
                display: true,
                text: '?????????????? ?????????????????? ??????????',
                color: "#000000"
              },
            legend: {
                labels: {
                    font: {
	            family: "GOST",				
                    size: 14
                    }
                  }
                }	  
            },
            layout: {
                padding: {
                    top: 80
                }
            },
            scales: {
                x: {
                    type: 'time',
	        title: {
  	        display: true,
  	        text: "??????????",
            color: "#000000"
	        },
                time: {
	        isoWeekday: true,
	        minUnit: time_per,
            displayFormats: {				
                minute: 'D MMM HH:mm',
                hour: 'D MMM ??????????',
                day: 'D MMM'}},
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 20,
                    maxRotation: 60,
                    minRotation: 30,
                    source: "data",
                    color: "black",
	            display: true,
                    font: {
	          },
                },
                grid: {
                    drawTicks: true,
                    borderColor: "black",
	          enabled: true,
	          drawTicks: true,
	          lineWidth: 1,					
                },
              },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
	        border: {
  	        color: "#000000",
	        },
                ticks: {
                    color: "#000000",
	        },
	        title: {
  	        display: true,
  	        color: "#000000",
	            text: "??????????????????????",
	        },  
            grid: {
                color: "#000000",
                }
            }}}});
        Chart3.update();
        }
        if (Chart4 != undefined) {	
            Chart4.data.datasets.forEach(dataset => {
                dataset.data = Sensor.air});
            Chart4.options.scales.x.time.minUnit = time_per;
                Chart4.update("resize");			
            } else {	
                Chart4 = new Chart('chart_AVG', {			
                    type: 'line',
                    data: {
                        datasets: [
                    {
                        label: '?????????????? ?????????????????????? ??????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "avg_temp"},	
                        showLine: true,
                        lineTension: 0.3,
                        color: "#FF0000"},
                    {
                        label: '?????????????? ?????????????????? ??????????????',
                        data: Sensor.air,
                        yAxisID: 'y',
                        parsing: {xAxisKey: "dt", yAxisKey: "avg_hum"},
                        showLine: true,
                        lineTension: 0.3,
                        color: "#00FF00"
                    }],
            },
                options: {
                    locale: "ru-RU",
                    animation: true,
                    plugins: {
                title: {
                    display: true,
                    text: '?????????????? ?????????????? ??????????????????',
                    color: "#000000"
                  },
                legend: {
                    labels: {
                        font: {
                    family: "GOST",				
                        size: 14
                        }
                      }
                    }	  
                },
                layout: {
                    padding: {
                        top: 80
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                title: {
                  display: true,
                  text: "??????????",
                color: "#000000"
                },
                    time: {
                isoWeekday: true,
                minUnit: time_per,
                displayFormats: {				
                    minute: 'D MMM HH:mm',
                    hour: 'D MMM HH ??????????',
                    day: 'D MMM'}
                    },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 20,
                        maxRotation: 60,
                        minRotation: 30,
                        source: "data",
                        color: "black",
                    display: true,
                        font: {
                  },
                    },
                    grid: {
                        drawTicks: true,
                        borderColor: "black",
                  enabled: true,
                  drawTicks: true,
                  lineWidth: 1,					
                    },
                  },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                border: {
                  color: "#000000",
                },
                    ticks: {
                        color: "#000000",
                },
                title: {
                  display: true,
                  color: "#000000",
                    text: "??????????????????????",
                },  
                grid: {
                    color: "#000000",
                    }
                }}}});
            Chart4.update();
            }	
        } else {
            alert("????????????. ???????????? ??????!")
        }


}
