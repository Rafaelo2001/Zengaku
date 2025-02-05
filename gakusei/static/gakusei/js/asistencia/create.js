// // // Numero
// // var precio_clase = false;

// // // Objecto JS
// // var beca  = false;

// // // Numero
// // var descuento  = false;


// // $(document).ready(function() {

// //     // Select2 configuration
// //     let opciones = {
// //         placeholder: "----------",
// //         allowClear: true,
// //         width: '250px',
// //     }
    
// //     $("#id_clase").select2(opciones);
// //     $("#id_estudiante").select2(opciones);
    

// //     // Al limpiar Clase
// //     $("#id_clase").on("select2:clear", () => {
// //         precio_clase = false;
// //         document.querySelector("#clase-data").innerText = "";

// //         calculo_precio();
// //     });

// //     // Al limpiar el Estudiante
// //     $("#id_estudiante").on("select2:clear", () => {
// //         beca = false;
// //         descuento = false;
// //         document.querySelector("#estudiante-beca").innerText = "";
// //         document.querySelector("#estudiante-descuento").innerText = "";

// //         calculo_precio();
// //     });

// //     // Obtenemos los precios y becas a partir de las funciones asincronas
// //     $("#id_clase").on("select2:select", (e) => get_price_clase(e));
// //     $("#id_estudiante").on("select2:select", (e) => get_price_estudiante(e));


// //     // Recuperamos datos anteriores y reactivamos las funciones de obtenion de precios
// //     if( $("#id_clase").val() ) {
// //         val = $("#id_clase").val();

// //         $("#id_clase").val(null).trigger("change");
// //         $("#id_clase").val(val).trigger("change");

// //         // Objeto que simula ser un evento
// //         let e = {"params": { "data": {"id": val} }}
// //         get_price_clase(e);   
// //     }

// //     if( $("#id_estudiante").val() ) {
// //         val = $("#id_estudiante").val();

// //         $("#id_estudiante").val(null).trigger("change");
// //         $("#id_estudiante").val(val).trigger("change");

// //         let e = {"params": { "data": {"id": val} }}
// //         get_price_estudiante(e);   
// //     }
// // });

// // async function get_price_clase(e) {
// //     let url = document.querySelector("#inscripciones-form").dataset.clase_url;
// //     let clase = await get_api_data(e, url);
    
// //     precio_clase = clase.precio;

// //     document.querySelector("#clase-data").innerText = `Precio de la clase: ${clase.precio}$`;

// //     calculo_precio();
// // }

// // async function get_price_estudiante(e) {
// //     let url = document.querySelector("#inscripciones-form").dataset.estudiante_url;
// //     let estudiante = await get_api_data(e, url);

// //     let beca_data, descuento_data;

// //     if (estudiante.beca) {
// //         // Estudiante -> Beca.
// //         beca_data = estudiante.beca;
        
// //         // Declaramos variable global
// //         beca = {"descuento": beca_data.descuento, "tipo": beca_data.tipo_descuento[0]};

// //         document.querySelector("#estudiante-beca").innerText = `Beca: ${beca_data.nombre}`;
// //     } else {
// //         beca = false;
// //         document.querySelector("#estudiante-beca").innerText = "";
// //     }

// //     if (estudiante.descuento) {
// //         // Estudiante -> Descuento Especial -> Cuanto es el descuento.
// //         descuento_data = estudiante.descuento.descuento;

// //         descuento = descuento_data;

// //         document.querySelector("#estudiante-descuento").innerText = `Descuento: ${descuento_data}$`;

// //     } else {
// //         descuento = false;

// //         document.querySelector("#estudiante-descuento").innerText = "";
// //     }

// //     calculo_precio();
// // }

// // function calculo_precio() {
// //     if (precio_clase) {
        
// //         let precio_final = precio_clase;        

// //         if (descuento) {
// //             precio_final -= descuento;

// //             if (precio_final<0) {precio_final=0}            
// //         }

// //         if (beca) {
// //             if (beca.tipo == "P") {
// //                 precio_final = precio_final - (precio_final * beca.descuento) / 100;
// //             }

// //             if (beca.tipo == "C"){
// //                 precio_final -= beca.descuento;
// //                 if (precio_final<0) {precio_final=0}
// //             }
// //         }

// //         // Redondeo al entero mas cercano.
// //         precio_final = Math.round(precio_final);
        
// //         document.querySelector("#id_precio_a_pagar").value = precio_final;
// //         document.querySelector("#precio-final").innerText = `Precio Final = ${precio_final}$`;

// //     } else {
// //         document.querySelector("#id_precio_a_pagar").value = "";
// //         document.querySelector("#precio-final").innerText = "";
// //     }
// // }


// // async function get_api_data(event, url) {

// //     let id = event.params.data.id;
    
// //     let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;
    
// //     let request = {
// //         method: "POST",
// //         headers: {'X-CSRFToken': csrf_token},
// //         mode: 'same-origin',
// //         body: JSON.stringify({"pk": id}),
// //     }
    
    
// //     try {
// //         let response = await fetch(url, request);
// //         let obj      = await response.json()
        
// //         return obj;    

// //     } catch (error) {
// //         console.error("Error al obtener los datos:", error);
// //         return {};
// //     }
// // }


document.addEventListener("DOMContentLoaded", function(){
    
    // Select2 Configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '250px',
    }
    
    $("#id_clase").select2(opciones);
    // $("#id_estudiante").select2(opciones);


    // Buscamos Dias de Clase
    $("#id_clase").on("select2:select", () => get_dias_clase( $("#id_clase").val() ));

    // Buscamos Estudiantes Inscritos
    $("#id_dias_de_clase").on("select2:select", () => get_estudiantes( $("#id_clase").val(), $("#id_dias_de_clase").val() ));



    // Reactivacion con valores anteriores
    if( $("#id_clase").val() ) {
        val = $("#id_clase").val();

        $("#id_clase").val(null).trigger("change");
        $("#id_clase").val(val).trigger("change");

        get_dias_clase(val);   
    }



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
                url_redirect = "loqdevuelvaelobjcxd";
            }
            else {
                error_form = r.error_form;
            }
        })
        .finally(() => {
            if(status){

            }
            else {
                document.querySelector("#estudiante-presentes").innerHTML = "";
                document.querySelector("#estudiante-presentes").innerHTML = error_form;
            }
        });
        

    });

});

async function get_dias_clase(clase_id) {

    let url = document.querySelector("#asistencia-form").dataset.dias;
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let request = {
        method: "POST",
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({"pk": clase_id}),
    }
    
    let response = await fetch(url, request);
    let obj      = await response.json()
    
    render_dias_select2(obj.results);
    
    return obj;
}

/**
 * 
 * @param {Array} dias_data - Datos en formato Select2
 */
function render_dias_select2(dias_data) {

    document.querySelector("#dias-select").innerHTML = "";
    document.querySelector("#estudiante-presentes").innerHTML = "";

    if (!dias_data){
        document.querySelector("#dias-select").innerHTML = "No ha habiado dias de clases para esta Clase.";
        return;
    }
    else {
        $('#id_dias_de_clase').select2('destroy');

        let select = document.createElement("select");
        select.id = "id_dias_de_clase";
        
        let label = document.createElement("label");
        label.innerText = "Dia de Clase: ";
        label.htmlFor = "id_dias_de_clase";
    
        document.querySelector("#dias-select").append(label);
        document.querySelector("#dias-select").append(select);
    }

    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '250px',
        data: dias_data,
    }

    // Que renderizar el Select2 que sea nulo
    $("#id_dias_de_clase").select2(opciones).val(null).trigger("change");

    $("#id_dias_de_clase").on("select2:select", () => get_estudiantes( $("#id_clase").val(), $("#id_dias_de_clase").val() ));


}


async function get_estudiantes(clase_id, dia_id) {

    let url = document.querySelector("#asistencia-form").dataset.estudiantes;
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let request = {
        method: "POST",
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({"clase_id": clase_id, "dia_id": dia_id}),
    }
    
    let response = await fetch(url, request);
    let obj      = await response.json()
    
    
    document.querySelector("#estudiante-presentes").innerHTML = "";
    document.querySelector("#estudiante-presentes").innerHTML = obj.form;
    
    
    
    return obj;
}





