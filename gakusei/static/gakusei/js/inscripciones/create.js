// Numero
var precio_clase = false;

// Objecto JS
var beca  = false;

// Numero
var descuento  = false;


$(document).ready(function() {

    // Select2 configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '250px',
    }
    
    $("#id_clase").select2(opciones);
    $("#id_estudiante").select2(opciones);
    

    // Al limpiar Clase
    $("#id_clase").on("select2:clear", () => {
        precio_clase = false;
        document.querySelector("#clase-data").innerText = "";

        calculo_precio();
    });

    // Al limpiar el Estudiante
    $("#id_estudiante").on("select2:clear", () => {
        beca = false;
        descuento = false;
        document.querySelector("#estudiante-beca").innerText = "";
        document.querySelector("#estudiante-descuento").innerText = "";

        calculo_precio();
    });

    // Obtenemos los precios y becas a partir de las funciones asincronas
    $("#id_clase").on("select2:select", (e) => get_price_clase(e));
    $("#id_estudiante").on("select2:select", (e) => get_price_estudiante(e));


    // Recuperamos datos anteriores y reactivamos las funciones de obtenion de precios
    if( $("#id_clase").val() ) {
        val = $("#id_clase").val();

        $("#id_clase").val(null).trigger("change");
        $("#id_clase").val(val).trigger("change");

        // Objeto que simula ser un evento
        let e = {"params": { "data": {"id": val} }}
        get_price_clase(e);   
    }

    if( $("#id_estudiante").val() ) {
        val = $("#id_estudiante").val();

        $("#id_estudiante").val(null).trigger("change");
        $("#id_estudiante").val(val).trigger("change");

        let e = {"params": { "data": {"id": val} }}
        get_price_estudiante(e);   
    }
});

async function get_price_clase(e) {
    let url = document.querySelector("#inscripciones-form").dataset.clase_url;
    let clase = await get_api_data(e, url);
    
    precio_clase = clase.precio;

    document.querySelector("#clase-data").innerText = `Precio de la clase: ${clase.precio}$`;

    calculo_precio();
}

async function get_price_estudiante(e) {
    let url = document.querySelector("#inscripciones-form").dataset.estudiante_url;
    let estudiante = await get_api_data(e, url);

    let beca_data, descuento_data;

    if (estudiante.beca) {
        // Estudiante -> Beca.
        beca_data = estudiante.beca;
        
        // Declaramos variable global
        beca = {"descuento": beca_data.descuento, "tipo": beca_data.tipo_descuento[0]};

        document.querySelector("#estudiante-beca").innerText = `Beca: ${beca_data.nombre}`;
    } else {
        beca = false;
        document.querySelector("#estudiante-beca").innerText = "";
    }

    if (estudiante.descuento) {
        // Estudiante -> Descuento Especial -> Cuanto es el descuento.
        descuento_data = estudiante.descuento.descuento;

        descuento = descuento_data;

        document.querySelector("#estudiante-descuento").innerText = `Descuento: ${descuento_data}$`;

    } else {
        descuento = false;

        document.querySelector("#estudiante-descuento").innerText = "";
    }

    calculo_precio();
}

function calculo_precio() {
    if (precio_clase) {
        
        let precio_final = precio_clase;        

        if (descuento) {
            precio_final -= descuento;

            if (precio_final<0) {precio_final=0}            
        }

        if (beca) {
            if (beca.tipo == "P") {
                precio_final = precio_final - (precio_final * beca.descuento) / 100;
            }

            if (beca.tipo == "C"){
                precio_final -= beca.descuento;
                if (precio_final<0) {precio_final=0}
            }
        }

        // Redondeo al entero mas cercano.
        precio_final = Math.round(precio_final);
        
        document.querySelector("#id_precio_a_pagar").value = precio_final;
        document.querySelector("#precio-final").innerText = `Precio Final = ${precio_final}$`;

    } else {
        document.querySelector("#id_precio_a_pagar").value = "";
        document.querySelector("#precio-final").innerText = "";
    }
}


async function get_api_data(event, url) {

    let id = event.params.data.id;
    
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;
    
    let request = {
        method: "POST",
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        body: JSON.stringify({"pk": id}),
    }
    
    
    try {
        let response = await fetch(url, request);
        let obj      = await response.json()
        
        return obj;    

    } catch (error) {
        console.error("Error al obtener los datos:", error);
        return {};
    }
}