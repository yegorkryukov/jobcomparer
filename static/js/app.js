window.addEventListener( "load", function () {
    function sendData() {

        const url = '/jobs';
        const card = document.getElementById('job_left');

        // Bind the FormData object and the form element
        const FD = new FormData( form );

        // log the forms fields 
        for (var pair of FD.entries()) {
        console.log(pair[0]+ ': ' + pair[1]); 
        }

        fetch(url, {
            method: "POST",
            // headers: new Headers({'content-type': 'application/json'}),
            body: FD
        })
        .then((resp) => resp.json())
        .then(function(data){
            console.log('received this:', data);
            const newElement = document.createElement('p');
            newElement.innerHTML = data.job_title;
            card.appendChild(newElement);
        })
        .catch(function(error){
            console.log(error);
        })
    }
   
    // Access the form element...
    const form = document.getElementById( "search_form" );
  
    // ...and take over its submit event.
    form.addEventListener( "submit", function ( event ) {
      event.preventDefault();
  
      sendData();
    } );
  } );



