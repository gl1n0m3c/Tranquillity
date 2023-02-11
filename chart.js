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
    url = "month"
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
    var Sensor = await Resp.json();
    if (Chart1 != undefined) {	
        Chart1.data.datasets.forEach(dataset => {
            dataset.data = Sensor.air});
            Chart1.update("resize");			
        } else {
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
	    //minUnit: 'minute',
        //maxUnit: 'day',
        displayFormats: {				
  	        millisecond: 'D MMM mm:ss',
  	        second: 'D MMM hh:mm',
	        minute: 'D MMM hh:mm',
	        hour: 'D MMM hh:mm',
	        day: 'D MMM hh',
	        week: 'D MMM hh',
	        month: 'D MMM yyyy',
	        quarter: 'D MMM yyyy',
	        year: 'D MMM yyyy'
              }
            },
            ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                maxRotation: 60,
                minRotation: 60,
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
    }

    if (Chart2 != undefined) {
        Chart2.data.datasets.forEach(dataset => {
            dataset.data = Sensor.air});
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
	    //minUnit: 'minute',
        //maxUnit: 'day',
        displayFormats: {				
            millisecond: 'D MMM mm:ss',
            second: 'D MMM hh:mm',
            minute: 'D MMM hh:mm',
            hour: 'D MMM hh:mm',
            day: 'D MMM hh',
            week: 'D MMM hh',
            month: 'D MMM yyyy',
            quarter: 'D MMM yyyy',
            year: 'D MMM yyyy'
            }
            },
            ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                maxRotation: 60,
                minRotation: 60,
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
    }


    if (Chart3 != undefined) {
        Chart3.data.datasets.forEach(dataset => {
            dataset.data = Sensor.ground});
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
	    //minUnit: 'minute',
        //maxUnit: 'day',
        displayFormats: {				
            millisecond: 'D MMM mm:ss',
            second: 'D MMM hh:mm',
            minute: 'D MMM hh:mm',
            hour: 'D MMM hh:mm',
            day: 'D MMM hh',
            week: 'D MMM hh',
            month: 'D MMM yyyy',
            quarter: 'D MMM yyyy',
            year: 'D MMM yyyy'
            }
            },
            ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                maxRotation: 60,
                minRotation: 60,
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
    }
  }
