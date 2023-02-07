const URL = 'https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/DATA';
var Chart1;						//Экземпляр объекта Chart
var Sensor;						//Массив данных полученных от сервера
const ColorLeft = 'rgb(255, 100, 100)';			//Настройки графика
const ColorRight = 'rgb(100, 100, 255)';		//Настройки графика
moment.locale('ru');					//Настройки графика. Переключение языка на русский для строк с датой

var Index = 0;						//Для демонстрации

//Обработка нажатий
ChartRefresh1.onclick = function() {
    DataFetch(URL);
    };
  
//Функция получения и отображения данных с сервера
async function DataFetch(strURL) {
    const Requ = new Request(strURL);
    const Resp = await fetch(Requ);
    const Data = await Resp.json();
  
    //Для демонстрации
    Sensor = Data[Index % 2];				//Для демонстрации изменяющихся данных
    Index += 1;						//Для демонстрации
    console.log(Sensor);					//Для отладки

//Манипуляции с тэгами HTML
//  const TagHeader = document.querySelector('header');	//Запрашиваем элемент <header> из документа
//  const DataName = document.createElement('div');	//Создаём элемент DataName в блоке div
//  TagHeader.appendChild(DataName);			//Добавляем в элемент <header> подготовленный элемент DataName
//  const Section = document.querySelector('section');	//Запрашиваем элемент <selection> из документа
//  for (const Rec of Sensor.air) {			//Цикл по всем записям Sensor.air
//      const Article = document.createElement('article');	//Создаём элемент article
//      const Para = document.createElement('span');	//Создаём элемент span
//      Para.textContent = `Дата: ${Rec.dt}, t1=${Rec.t1}`;	//Заполняем свойства элемента
//      Article.appendChild(Para);				//Добавляем в элемент Article подготовленный элемент Para
//      Section.appendChild(Article);			//Добавляем в элемент <section> подготовленный элемент Article
//      }
    
  //Манипуляции с графиком
    if (Chart1 != undefined) {				//Экземпляр объекта Chart существует?
        Chart1.data.datasets.forEach(dataset => {
            dataset.data = Sensor.air;			//Обновить данные
        });
        Chart1.update("resize");				//Обновить график
        } else {
            Chart1 = new Chart('chart1', {			//Создаём один раз и потом используем
            type: 'line',
            data: {
                datasets: [
            {
                label: 'Первый',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "t1"},	//задание соответствия полей данных к осям
                showLine: true,
                hidden: false,
                lineTension: 0.3,
                borderColor: ColorLeft},
            {
                label: 'Второй',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "t2"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#00FF00",
                borderColor: ColorRight},
            {
                label: 'Третий',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "t3"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#0000FF",
                borderColor: ColorLeft},
            {
                label: 'Четвертый',
                data: Sensor.air,
                yAxisID: 'y',
                parsing: {xAxisKey: "dt", yAxisKey: "t4"},
                showLine: true,
                hidden: true,
                lineTension: 0.3,
                color: "#FFFFFF",
                borderColor: ColorRight}],
    },
        options: {
            locale: "ru-RU",
            animation: false,
            plugins: {
        title: {
            display: true,
            text: 'Датчики воздуха',
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
  	    text: "Ось времени ",
	    },
            time: {
	      isoWeekday: true,
	      minUnit: 'second',
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
  	    color: ColorLeft,
	    },
            ticks: {
                color: ColorLeft,
	    },
	    title: {
  	    display: true,
  	    color: ColorLeft,
	        text: "Температура",
	    },  
        grid: {
            color: ColorRight,
            }
          }}}});
    }
  }
