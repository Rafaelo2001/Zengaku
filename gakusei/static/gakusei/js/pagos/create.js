document.addEventListener("DOMContentLoaded", function(){


    // Select2 Configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '300px',
    }

    $("#id_estudiante").select2(opciones);

    let opciones_clase = opciones;
    opciones_clase.placeholder = "Seleccione primero un estudiante.";
    opciones_clase.disabled = true;
    opciones_clase.data = null;

    $("#id_clase").select2(opciones);


    $("#id_estudiante").on("select2:select", () => get_clases( $("#id_estudiante").val() ));

});



async function get_clases(id_estudiante){

    let url = document.querySelector("#pago-form").dataset.get_clases;
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let request = {
        method: "POST",
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({"pk": id_estudiante}),
    }

    let response = await fetch(url, request);
    let obj      = await response.json();
    
    let status = response.ok;
    let clases = obj.results;

    console.log(obj);
    console.log(status);


    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '300px',
        disabled: false,
        data: clases,
    }

    console.log(clases, opciones);
    

    if($("#id_clase").hasClass("select2-hidden-accessible")){
        $("#id_clase").empty().select2("destroy");
    }

    $("#id_clase").select2(opciones).val(null).change();
}
