document.addEventListener("DOMContentLoaded", function() {
    
    // Select2 Configuration
    let opciones = {
        placeholder: "----------",
        allowClear: true,
        width: '250px',
    }

    $("#id_sensei").select2(opciones);
    $("#id_curso").select2(opciones);
    $("#id_sede").select2(opciones);
});