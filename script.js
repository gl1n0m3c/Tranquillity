const getResourse = async(url) => {
    const response = await fetch(url);
    return await response.json();
};


getResourse('https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/options').then((data) => console.log(data))

async function get1(){
    
        
    
    };



async function get(num){
    if (num==1){
    
        const ajaxSend = async (formData) => {
            const response = await fetch("http://localhost:8000//save_temperature/", {
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
                            form.reset(); // очищаем поля формы
                        })
                });
            });
        }
    }   if (num==2){
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
                                form.reset(); // очищаем поля формы

                            })
                    });
                });
            }
        } if(num==3){


            
                const ajaxSend = async (formData) => {
                    const response = await fetch("http://localhost:8000//save_ground_humidity/", {
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
                                    form.reset(); // очищаем поля формы
                                })
                        });
                    });
                }
            
        }};