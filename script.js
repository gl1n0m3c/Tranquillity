const getResourse = async(url) => {
    const response = await fetch(url);
    console.log(response)
};


getResourse('https://jsonplaceholder.typicode.com/todos/1')