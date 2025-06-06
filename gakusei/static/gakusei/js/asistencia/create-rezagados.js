document.addEventListener("DOMContentLoaded", function(){
    
    // Select2 Configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        containerCssClass : 'select form-select mb-3',
        theme: "bootstrap-5",
        width: 'auto',
    }
    
    $("#id_clase").select2(opciones);


    // Buscamos formulario de Asistencia de Rezagados
    $("#id_clase").on("select2:select", () => get_asistencia_form( $("#id_clase").val() ));


    // Reactivacion con valores anteriores
    if( $("#id_clase").val() ) {
        val = $("#id_clase").val();

        $("#id_clase").val(null).trigger("change");
        $("#id_clase").val(val).trigger("change");

        get_asistencia_form(val);   
    }


    // Al limpiar el campo, se resetea el resto.
    $("#id_clase").on("select2:clear", () => {
        document.querySelector("#rezagados-form").innerHTML = "";
        document.querySelector("#rezagados-form").innerHTML = "<p>Seleccione una clase primero.</p>";


        document.querySelector("#submit-button").disabled = true;
    });



    // Intersepcion de los datos enviados por el formulario
    document.querySelector("#asistencia-form").addEventListener("submit", function(event) {
        event.preventDefault();

        let form = event.target;
        let form_data = new FormData(form);

        let status, error_form, url_redirect;
        fetch(form.action, {
            method: form.method,
            body: form_data,
        })
        .then(r => {
            status = r.ok;
            return r.json();
        })
        .then(r => {
            if(status){
                url_redirect = r.url_redirect;
            }
            else {
                error_form = r.error_form;
            }
        })
        .finally(() => {
            if(status){
                window.location.href = url_redirect;
            }
            else {
                document.querySelector("#rezagados-form").innerHTML = "";
                document.querySelector("#rezagados-form").innerHTML = error_form;
            }
        });
        

    });

});

async function get_asistencia_form(clase_id) {

    let url = document.querySelector("#asistencia-form").dataset.asistencia;
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let request = {
        method: "POST",
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({"pk": clase_id}),
    }
    
    let response = await fetch(url, request);
    let obj      = await response.json()

    let status = response.ok;
    
    if (status) {
        document.querySelector("#rezagados-form").innerHTML = "";
        document.querySelector("#rezagados-form").innerHTML = obj.form;

        document.querySelector("#submit-button").disabled = false;
    }
    else {
        document.querySelector("#rezagados-form").innerHTML = "";
        document.querySelector("#rezagados-form").innerHTML = `<p>${obj.error}</p>`;

        document.querySelector("#submit-button").disabled = true;
    }
    
    return obj;
}
