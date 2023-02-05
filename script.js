const getResourse = async(url) => {
    const response = await fetch(url);
    return await response.json();
};

let k = 0
let k2 = 0
let k3 = 0
let k4 = 0
let k5 = 0
let k6 = 0
let k7 = 0
let k8 = 0
getResourse('https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/options').then((data) => console.log(data))

async function zapros(n){
    const Requ = new Request(n)
    const Resp = await fetch(Requ);
    const D = await Resp.json()
};




async function get(num){
    if (num==1){
    
        const ajaxSend = async (formData) => {
            const response = await fetch("http://localhost:8000/save_temperature/", {
                method: "GET",
            });
        };
    
        if (document.querySelector("form")) {
            const forms = document.querySelectorAll("form");
    
            forms.forEach(form => {
                form.addEventListener("submit", function (e) {
                    e.preventDefault();
                    const formData = new FormData(this);
    
                    ajaxSend(formData)
                        .then((response) => {
                            console.log('hi');
                            form.reset();
                        })
                });
            });
        }

        
    } if (num==2){
                const ajaxSend = async (formData) => {
                const response = await fetch("http://localhost:8000/save_air_humidity/", {
                    method: "GET",
                });
            };

            if (document.querySelector("form")) {
                const forms = document.querySelectorAll("form");

                forms.forEach(form => {
                    form.addEventListener("submit", function (e) {
                        e.preventDefault();
                        const formData = new FormData(this);

                        ajaxSend(formData)
                            .then((response) => {
                                console.log('hello');
                                form.reset(); 

                            })
                    });
                });
            }
        } if(num==3){


            
                const ajaxSend = async (formData) => {
                    const response = await fetch("http://localhost:8000/save_ground_humidity/", {
                        method: "GET",
                    });
                };
                
                if (document.querySelector("form")) {
                    const forms = document.querySelectorAll("form");
                
                    forms.forEach(form => {
                        form.addEventListener("submit", function (e) {
                            e.preventDefault();
                            const formData = new FormData(this);
                
                            ajaxSend(formData)
                                .then((response) => {
                                    console.log('gutentag');
                                    form.reset();
                                })
                        });
                    });
                } 
        }};
function knopki(n){
    k=k+1
    if (k%2==1){
        zapros(n+'/open_windows')
        console.log('Open Windows')}
    if (k%2==0){
        zapros(n+'/close_windows')
        console.log('Close Windows')
}
}

function knopki2(n){
    k2=k2+1
    if (k2%2==1){
        zapros(n+'/start_humidity_system')
        console.log('Start humidity system')}
    if (k2%2==0){
        zapros(n+'/stop_humidity_system')
        console.log('Stop humidity system')
}
}

function knopki3(n){
    k3=k3+1
    if (k3%2==1){
        zapros(n+'/start_wattering/1')
        console.log('Start wattering 1')}
    if (k3%2==0){
        zapros(n+'/stop_wattering/1')
        console.log('Stop wattering 1')
}
}

function knopki4(n){
    k4=k4+1
    if (k4%2==1){
        zapros(n+'/start_wattering/2')
        console.log('Start wattering 2')}
    if (k4%2==0){
        zapros(n+'/stop_wattering/2')
        console.log('Stop wattering 2')
}
}
function knopki5(n){
    k5=k5+1
    if (k5%2==1){
        zapros(n+'/start_wattering/3')
        console.log('Start wattering 3')}
    if (k5%2==0){
        zapros(n+'/stop_wattering/3')
        console.log('Stop wattering 3')
}
}
function knopki6(n){
    k6=k6+1
    if (k6%2==1){
        zapros(n+'/start_wattering/4')
        console.log('Start wattering 4')}
    if (k6%2==0){
        zapros(n+'/stop_wattering/4')
        console.log('Stop wattering 4')
}
}
function knopki7(n){
    k7=k7+1
    if (k7%2==1){
        zapros(n+'/start_wattering/5')
        console.log('Start wattering 5')}
    if (k7%2==0){
        zapros(n+'/stop_wattering/5')
        console.log('Stop wattering 5')
}
}
function knopki8(n){
    k8=k8+1
    if (k8%2==1){
        zapros(n+'/start_wattering/6')
        console.log('Start wattering 6')}
    if (k8%2==0){
        zapros(n+'/stop_wattering/6')
        console.log('Stop wattering 6')
}
}