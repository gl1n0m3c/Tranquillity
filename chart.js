const URL = "http://localhost:8000/give_data/30min";
var Chart1;							
moment.locale('ru');

//Обработка нажатий
ChartRefresh1.onclick = function() {
    DataFetch(URL);
    };

async function DataFetch(strURL) {
    const Requ = new Request(strURL);
    const Resp = await fetch(Requ);
    var Sensor = await Resp.json();
    
    if (Chart1 != undefined) {				
        Chart1.data.datasets.forEach(dataset => {
            dataset.data = Sensor.air;			
        });
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
	    },
            time: {
	    isoWeekday: true,
	    minUnit: 'minute',
                displayFormats: {				
  	        millisecond: 'mm:ss.SSS',
  	        second: 'hh:mm:ss',
	        minute: 'D hh:mm',
	        hour: 'D MMM hh:mm',
	        day: 'D MMM hh:mm',
	        week: 'D MMM hh:mm',
	        month: 'D MMM yyyy',
	        quarter: 'D MMM yyyy',
	        year: 'D MMM yyyy'
              }
            },
            ticks: {
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
