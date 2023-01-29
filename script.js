const getResourse = async(url) => {
    const response = await fetch(url);
    
    return await response.json();
};


getResourse('https://my-json-server.typicode.com/valeriy-egorov/FakeOnlineRESTserver/options').then((data) => console.log(data))