function muestraModal(url, titulo){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar el videojuego ${titulo}?`;
}

function muestraModalUser(url, titulo){
    document.getElementById('formEliminarU').action = url;
    document.getElementById('modalCuerpo').innerHTML = `¿Deseas eliminar el usuario ${titulo}?`;

}

$("#id_estado").on('change', function(){ 
    var token = $('[name="csrfmiddlewaretoken"]').val();  
    $.ajax({
        type: "post",
        url: `/usuarios/municipios/`,
        data: {'id':this.value, 'csrfmiddlewaretoken': token},
        success: function (response) {
            var html = "";
            if (response[0].hasOwnProperty('error')){
                html+=`<option value="0">${response[0].error}</option>`;
            }
            else{
                $.each(response, function (llave, valor) { 
                    html+=`<option value="${valor.id}">${valor.nombre}</option>`;
                });
            }
            $("#id_municipio").html(html);
        },
        error: function (param) { 
            console.log('Error en la petición');
        }
    });
});


function muestraModalGrupos(url, grupos){
    grps = grupos.split('-')
    grps.length = grps.length - 1
    document.getElementById('formGrupos').action = url;

    $('#formGrupos input[type = checkbox]').each(function(){
        $(this).prop("checked", false);
        if (grps.includes($(this).prop('name'))){
            $(this).prop("checked", true);
        }

    });
}