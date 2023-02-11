
const port = "8000";
var url;

min30.onclick = function() {
    url = "30min";
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}

hour1.onclick = function() {
    url = "hour";
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}

hours12.onclick = function() {
    url = "12hours";
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}

day1.onclick = function() {
    url = "day";
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}

month1.onclick = function() {
    url = "month";
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}

ChartRefresh1.onclick = function() {
    DataFetch("http://localhost:" + port + "/give_data/" + url);
}


var Chart1;		
var Chart2; 
var Chart3;					
moment.locale('ru');


async function DataFetch(strURL) {
    const Requ = new Request(strURL);
    const Resp = await fetch(Requ);
    const Sensor = await Resp.json();
    var time_per;
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
    console.log(time_per)
    var t_average;
    if (Chart1 != undefined) {	
        Chart1.data.datasets.forEach(dataset => {
            dataset.data = Sensor.air});
        Chart1.options.scales.x.time.minUnit = time_per;
       // t_average = (Sensor.air.t1 + Sensor.air.t2 + Sensor.air.t3 + Sensor.air.t4) / 4
            Chart1.update("resize");			
        } else {	
           // t_average = (Sensor.air.t1 + Sensor.air.t2 + Sensor.air.t3 + Sensor.air.t4) / 4
            Chart1 = new Chart('chart1', {			
                type: 'line',
                data: {
                    datasets: [
                {
                    label: 'Первый',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "t1"},	
                    showLine: true,
                    hidden: false,
                    lineTension: 0.3,
                    color: "#FF0000"},
                {
                    label: 'Второй',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "t2"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#00FF00"
                },
                {
                    label: 'Третий',
                    data: Sensor.air,
                    yAxisID: 'y',
                    parsing: {xAxisKey: "dt", yAxisKey: "t3"},
                    showLine: true,
                    hidden: true,
                    lineTension: 0.3,
                    color: "#0000FF"
                },
                {
                    label: 'Четвертый',
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
                text: 'Датчики температуры',
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
              text: "Время",
            color: "#000000"
            },
                time: {
            isoWeekday: true,
            minUnit: time_per,
            displayFormats: {				
                minute: 'D MMM hh:mm',
                hour: 'D MMM hh часов/-а',
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
                text: "Температура",
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
                label: 'Первый',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h1"},	
                showLine: true,
                hidden: false,
                lineTension: 0.3,
                color: "#FF0000"},
            {
                label: 'Второй',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h2"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#00FF00"
            },
            {
                label: 'Третий',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h3"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#0000FF"
            },
            {
                label: 'Четвертый',
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
            text: 'Датчики влажности воздуха',
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
  	    text: "Время",
        color: "#000000"
	    },
            time: {
	    isoWeekday: true,
	    minUnit: time_per,
        displayFormats: {				
            minute: 'D MMM hh:mm',
            hour: 'D MMM hh часов/-а',
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
	        text: "Температура",
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
                label: 'Первый',
                data: Sensor.ground,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h1"},	
                showLine: true,
                hidden: false,
                lineTension: 0.3,
                color: "#FF0000"},
            {
                label: 'Второй',
                data: Sensor.ground,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h2"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#00FF00"
            },
            {
                label: 'Третий',
                data: Sensor.ground,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h3"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#0000FF"
            },
            {
                label: 'Четвертый',
                data: Sensor.ground,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h4"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#FF00FF"
            },
            {
                label: 'Пятый',
                data: Sensor.ground,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "h5"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#FF00FF"
            },
            {
                label: 'Шестой',
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
            text: 'Датчики влажности почвы',
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
  	    text: "Время",
        color: "#000000"
	    },
            time: {
	    isoWeekday: true,
	    minUnit: time_per,
        displayFormats: {				
            minute: 'D MMM hh:mm',
            hour: 'D MMM hh часов/-а',
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
	        text: "Температура",
	    },  
        grid: {
            color: "#000000",
            }
        }}}});
    Chart3.update();
    }
  }
