const getResourse = async(url) => {
   const response = await fetch(url);
    return await response.json();
}
const m = '8001'
let k = 0
let k1 = 0
let k2 = 0
let k3 = 0
let k4 = 0
let k5 = 0
let k6 = 0
let k7 = 0
let e = 0
function extra(){
e=1
}

function auto(){
e=0
}
async function zapros(n){
    const Requ = new Request(n)
    const Resp = await fetch(Requ);
    const D = await Resp.json()
};
function get(n){
if (n==1){
  let input1 = document.getElementById('MaxT')
  zapros('http://localhost:'+m+'/save_temperature/'+input1.value)
  console.log(input1.value);
}
if (n==2){
    let input2 = document.getElementById('MaxH')
    zapros('http://localhost:'+m+'/save_air_humidity/'+input2.value)
    console.log(input2.value);
}
if (n==3){
    let input3 = document.getElementById('MaxHb')
    zapros('http://localhost:'+m+'/save_ground_humidity/'+input3.value)
    console.log(input3.value);
}
};
function knopki(){
    k+=1
    if (k%2==1){  
        if (1==2){             //if 1==2 заменить на ответ от сервера(отрицательный)
            document.getElementById("1").classList.remove('toggle-checkbox');
            document.getElementById("1").classList.add('toggle-checkbox1');
            document.getElementById("1").classList.remove('toggle-checkbox2');
            k=k-1
            alert('ответ от сервера отрицательный')
        }
        if(1==1){                               //if 1==1 заменить на ответ от сервера(положительный)
            document.getElementById("1").classList.remove('toggle-checkbox1');
            document.getElementById("1").classList.add('toggle-checkbox');
            alert('ответ от сервера положительный')
                zapros('http://localhost:'+m+'/open_windows')
                console.log('Open Windows')}
    }
    if (k%2==0){  
        if (1==2){             //if 1==2 заменить на ответ от сервера(отрицательный)
            document.getElementById("1").classList.remove('toggle-checkbox');
            document.getElementById("1").classList.add('toggle-checkbox1');
            k=k-1
            alert('ответ от сервера отрицательный')
        }
        if(1==1){                               //if 1==1 заменить на ответ от сервера(положительный)
            document.getElementById("1").classList.remove('toggle-checkbox1');
            document.getElementById("1").classList.add('toggle-checkbox');
            alert('ответ от сервера положительный')
            zapros('http://localhost:'+m+'/close_windows')
            console.log('Close Windows')

                } 
                }
}
function knopki2(){
    k1+=1   
    if (1==2){                                     //if 1==2 заменить на ответ от сервера( отрицательный)
        document.getElementById("2").classList.remove('toggle-checkbox');
        document.getElementById("2").classList.add('toggle-checkbox1');
        k1=k1-1
        alert('ответ от сервера отрицательный')
}   
    if(1==1){                                      //if 1==1 заменить на ответ от сервера(положительный)
    document.getElementById("2").classList.remove('toggle-checkbox1');
    document.getElementById("2").classList.add('toggle-checkbox');
    alert('ответ от сервера положительный')
        if (k1%2==1){
            zapros('http://localhost:'+m+'/start_humidity_system')
            console.log('Start humidity system')
                    }
        if (k1%2==0){
            zapros('http://localhost:'+m+'/stop_humidity_system')
            console.log('Stop humidity system')
                }

            }
        }
function knopki3(){
    k2+=1
    if (1==2){
    document.getElementById("3").classList.remove('toggle-checkbox');
    document.getElementById("3").classList.add('toggle-checkbox1');
    k2=k2-1
    alert('ответ от сервера отрицательный')
            }   
    if(1==1){
    document.getElementById("3").classList.remove('toggle-checkbox1');
    document.getElementById("3").classList.add('toggle-checkbox');
    alert('ответ от сервера положительный')
        if (k2%2==1){
            zapros('http://localhost:'+m+'/start_wattering/1')
            console.log('Start wattering 1')}
        if (k2%2==0){
            zapros('http://localhost:'+m+'/stop_wattering/1')
            console.log('Stop wattering 1')
}
}
}

function knopki4(){
    k3+=1
    if (1==2){
    document.getElementById("4").classList.remove('toggle-checkbox');
    document.getElementById("4").classList.add('toggle-checkbox1');
    k3=k3-1
    alert('ответ от сервера отрицательный')
            }   
    if(1==1){
    document.getElementById("4").classList.remove('toggle-checkbox1');
    document.getElementById("4").classList.add('toggle-checkbox');
    alert('ответ от сервера положительный')
        if (k3%2==1){
            zapros('http://localhost:'+m+'/start_wattering/2')
            console.log('Start wattering 2')}
        if (k3%2==0){
            zapros('http://localhost:'+m+'/stop_wattering/2')
            console.log('Stop wattering 2')
    }
}
}
function knopki5(){
    k4+=1
    if (1==1 && e==0){
    document.getElementById("5").classList.remove('toggle-checkbox');
    document.getElementById("5").classList.add('toggle-checkbox1');
    k4=k4-1
    alert('ответ от сервера отрицательный')
            }   
    if (1==2 || e==1){
    document.getElementById("5").classList.remove('toggle-checkbox1');
    document.getElementById("5").classList.add('toggle-checkbox');
    alert('ответ от сервера положительный')
        if (k4%2==1){
            zapros('http://localhost:'+m+'/start_wattering/3')
            console.log('Start wattering 3')}
        if (k4%2==1){
            zapros('http://localhost:'+m+'/stop_wattering/3')
            console.log('Stop wattering 3')
}
}
}
function knopki6(){
    k5+=1
    if (1==1){
        document.getElementById("6").classList.remove('toggle-checkbox');
        document.getElementById("6").classList.add('toggle-checkbox1');
        k5=k5-1
        alert('ответ от сервера отрицательный')
                }   
    if(1==2){
    document.getElementById("6").classList.remove('toggle-checkbox1');
    document.getElementById("6").classList.add('toggle-checkbox');
    alert('ответ от сервера положительный')
        if (k5%2==1){
            zapros('http://localhost:'+m+'/start_wattering/4')
            console.log('Start wattering 4')}
        if (k5%2==1){
            zapros('http://localhost:'+m+'/stop_wattering/4')
            console.log('Stop wattering 4')
}
}
}
function knopki7(){
    k6+=1
    if (1==1){
        document.getElementById("7").classList.remove('toggle-checkbox');
        document.getElementById("7").classList.add('toggle-checkbox1');
        k6=k6-1
        alert('ответ от сервера отрицательный')
                }   
    if(1==2){
        document.getElementById("7").classList.remove('toggle-checkbox1');
        document.getElementById("7").classList.add('toggle-checkbox');
        alert('ответ от сервера положительный')
        if (k6%2==1){
            zapros('http://localhost:'+m+'/start_wattering/5')
            console.log('Start wattering 5')}
        if (k6%2==1){
            zapros('http://localhost:'+m+'/stop_wattering/5')
            console.log('Stop wattering 5')
}
}
}
function knopki8(){
    k7+=1
    if (1==1){
        document.getElementById("8").classList.remove('toggle-checkbox');
        document.getElementById("8").classList.add('toggle-checkbox1');
        k7=k7-1
        alert('ответ от сервера отрицательный')
                }   
        if(1==2){
        document.getElementById("8").classList.remove('toggle-checkbox1');
        document.getElementById("8").classList.add('toggle-checkbox');
        alert('ответ от сервера положительный')
            if (k7%2==1){
                zapros('http://localhost:'+m+'/start_wattering/6')
                console.log('Start wattering 6')}
            if (k7%2==1){
                zapros('http://localhost:'+m+'/stop_wattering/6')
                console.log('Stop wattering 6')
}
}
}
