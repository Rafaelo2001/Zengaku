document.addEventListener("DOMContentLoaded", function() {
    
    // Select2 Configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '250px',
    }

    $("#id_clase").select2(opciones);

    document.querySelector("#horario-form").addEventListener("submit", () => {

        document.querySelector("#id_clase").disabled  = false;
    });
});