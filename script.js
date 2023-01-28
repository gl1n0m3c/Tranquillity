document.addEventListener("DOMContentLoaded", () => {

    const Send = (formData) => {
        fetch("mail.php", { // файл-обработчик
            method: "POST",
            headers: {
                "Content-Type": "application/json", // отправляемые данные
            },
            body: JSON.stringify(formData)
        })
            .then(response => alert("Сообщение отправлено"))
            .catch(error => console.error(error))
    };

    if (document.getElementsByTagName("form")) {
        const forms = document.getElementsByTagName("form");

        for (let i = 0; i < forms.length; i++) {
            forms[i].addEventListener("submit", function (e) {
                e.preventDefault();

                let formData = new FormData(this);
                formData = Object.fromEntries(formData);

                Send(formData)
                    .then((response) => {
                        console.log(response);
                    })
                    .catch((err) => console.error(err))
            });
        };
    }
});

