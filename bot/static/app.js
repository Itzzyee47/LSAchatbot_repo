

document.getElementById('message-form').addEventListener('submit', (event) => {
    event.preventDefault();
    let message = document.getElementById('userInput').value;
    console.log(message);
    //asynchronus request sent to backend...
    fetch('/send_message', {method: 'POST', 
    headers:{'Content-Type':'application/x-www-form-urlencoded'}, 
    body: 'message=' + encodeURIComponent(message)
    }).then(Response => Response.json()).then(data =>{
        var chatwin = document.getElementById('chatWindow');
        var userQ = document.createElement('li');

        userQ.classList.add('umess');
        chatwin.appendChild(userQ);
        var resposeM = document.createElement('li');
        resposeM.classList.add('bmess');
        // chatwin.appendChild(resposeM);
        console.log(data, 12344);
        document.getElementById('userInput').value = '';

    });

});