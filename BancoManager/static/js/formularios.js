$(document).ready(function() {
    // Obtener el token CSRF desde la meta etiqueta
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    // Configurar jQuery para incluir el token CSRF en todas las solicitudes AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });


    // Manejar la carga del formulario
    function handleFormLoad(buttonSelector, url, targetSelector, modalSelector) {
        $(buttonSelector).on('click', function(e) {
            e.preventDefault(); // Prevenir comportamiento por defecto
            console.log('Cargando formulario desde', url);
            $.ajax({
                url: url,  // URL para obtener el formulario
                method: "GET",
                success: function(response) {
                    // Eliminar el header y todo el contenido que contenga 
                    response = response.replace(/<header>[\s\S]*<\/header>/, '');
                    // Eliminar el <footer class="bg-light text-dark text-center py-4"> y todo el contenido que contenga
                    response = response.replace(/<footer class="bg-light text-dark text-center py-4">[\s\S]*<\/footer>/, '');
                    // Insertar el formulario en el HTML
                    $(targetSelector).html(response);
                    console.log('Formulario cargado exitosamente', response);
                    // Mostrar el formulario en un modal
                    $(modalSelector).removeAttr('aria-hidden').modal('show');
                    // Validar si existe un formulario en el modal si es asi se elimina
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al cargar el formulario',
                        text: xhr.responseText
                    });
                }
            });
        });
    }

    // Manejar la carga de datos del formulario
    function handleFormLoadDataincome(url) {
        $.ajax({
            // Tomar la url como ruta unica y no considerar de donde viene
            url: url,  // URL para obtener el formulario
            method: "GET",
            success: function(response) {
                console.log('Formulario cargado exitosamente', response.data[0]);
                // Llenar los campos del formulario
                for (var key in response.data[0]) {
                    if (response.data[0].hasOwnProperty(key)) {
                        var value = response.data[0][key];
                        var inputSelector = `#${key}`;
                        $(inputSelector).val(value);
                    }
                }  
                var nombre_modelo = response.data[0].modelo.replace("_", " ");
                // Actualizar los botones
                $('#boton_agregar').text('Actualizar');
                // Acrtualizar el titulo
                $('#titulo_principal').text('Actualizar '+ nombre_modelo + '');                
            },
            error: function(xhr) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al cargar el formulario',
                    text: xhr.responseText
                });
            }
        });
    }



    // Manejar el envío del formulario
    function handleFormSubmit(formSelector, url, metodo = "POST", modalSelector=null) {
        $(formSelector).on('submit', function(e) {
            e.preventDefault(); // Prevenir comportamiento por defecto
            console.log('Formulario enviado', e);
            // Recolectar datos del formulario
            var formData = $(this).serialize();
            $.ajax({
                url: url,  // URL para agregar ingresos
                method: metodo,
                data: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Ingreso agregado exitosamente',
                        showConfirmButton: false,
                        timer: 1500
                    });
                    // Limpiar el formulario
                    $(formSelector).trigger('reset');
                    // Validar si existe un modal
                    if (modalSelector) {
                        // Ocultar el modal
                        console.log('Cerrando modal', $(modalSelector));
                        $(modalSelector).modal('hide');
                    }
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al agregar',
                        text: xhr.responseText
                    });
                }
            });
        });
    }


    // Funcion principal para la busqueda de registros
    function handleSearchProcess(inputSelector, resultSelector, searchUrl) {
        var debounceTimer;  // Variable para debounce
        $(inputSelector).on('input', function() {
            var query = $(this).val().trim();
            clearTimeout(debounceTimer);  // Limpiar el timer anterior

            if (query.length > 1) {
                debounceTimer = setTimeout(function() {
                    $.ajax({
                        url: searchUrl,  // Ruta que vas a usar para obtener cuentas
                        method: "GET",
                        data: { q: query },  // Envío de la consulta
                        success: function(data) {
                            showResults(data, resultSelector);
                        },
                        error: function(xhr) {
                            console.error("Error al obtener cuentas: ", xhr.responseText);
                        }
                    });
                }, 300);  // Delay de 300ms
            } else {
                $(resultSelector).hide();  // Ocultar la lista si el input está vacío
            }
        });
    }


    // Manejar la búsqueda de cuentas de manera dinámica
    function handleAccountSearch(inputSelector, resultSelector, searchUrl) {
        handleSearchProcess(inputSelector, resultSelector, searchUrl);
    }

    // Manejar la búsqueda de usuarios de manera dinámica
    function handleUserSearch(inputSelector, resultSelector, searchUrl) {
        handleSearchProcess(inputSelector, resultSelector, searchUrl);
    }

    // Manejar la búsqueda de prestamos de manera dinámica
    function handleLoanSearch(inputSelector, resultSelector, searchUrl) {
        handleSearchProcess(inputSelector, resultSelector, searchUrl);
    }

    // Manejar la búsqueda de bancos de manera dinámica
    function handleBankSearch(inputSelector, resultSelector, searchUrl) {
        handleSearchProcess(inputSelector, resultSelector, searchUrl);
    }


    // Mostrar los resultados de la búsqueda
    function showResults(data, resultSelector) {
        var $resultList = $(resultSelector);
        $resultList.empty();  // Limpiar la lista anterior
        if (data.length > 0) {
            data.forEach(function(cuenta) {
                $resultList.append('<li class="list-group-item cuenta-item" data-id="' + cuenta.id + '">' + cuenta.nombre + '</li>');
            });
            $resultList.show();  // Mostrar la lista
        } else {
            $resultList.hide();  // Si no hay resultados oculta la lista
        }
    }

    // Función principal para manejar la selección de registros
    function handleSelectionprocess(resultSelector, inputSelector, hiddenInputSelector) {
        $(document).on('click', '.cuenta-item', function() {
            var cuentaNombre = $(this).text();
            var cuentaId = $(this).data('id');
            var targetInput = $(this).closest(resultSelector).data('target-input');
            var targetHiddenInput = $(this).closest(resultSelector).data('target-hidden-input');

            $(targetInput).val(cuentaNombre);  // Establecer el nombre de la cuenta en el input visible
            $(targetHiddenInput).val(cuentaId);  // Establecer el ID de la cuenta en el input oculto
            $(resultSelector).hide();  // Ocultar la lista
        });

        // Cerrar la lista si se hace clic fuera de ella
        $(document).on('click', function(e) {
            if (!$(e.target).closest(resultSelector).length && !$(e.target).is(inputSelector)) {
                $(resultSelector).hide();
            }
        });
        // Validar si el input es vacio asginar el valor del input a los campos ocultos 
        $(inputSelector).on('input', function() {
            if ($(inputSelector).val() == '') {
                $(hiddenInputSelector).val('');
            }
        });

    }


    // Manejar el clic en una cuenta de la lista
    function handleAccountSelection(resultSelector, inputSelector, hiddenInputSelector) {
        handleSelectionprocess(resultSelector, inputSelector, hiddenInputSelector);
    }
    // Manejar el clic en un usuario de la lista
    function handleUserSelection(resultSelector, inputSelector, hiddenInputSelector) {
        handleSelectionprocess(resultSelector, inputSelector, hiddenInputSelector);
    }
    // Manejar el clic en un prestamo de la lista
    function handleLoanSelection(resultSelector, inputSelector, hiddenInputSelector) {
        handleSelectionprocess(resultSelector, inputSelector, hiddenInputSelector);
    }
    // Manejar el clic en un banco de la lista
    function handleBankSelection(resultSelector, inputSelector, hiddenInputSelector) {
        handleSelectionprocess(resultSelector, inputSelector, hiddenInputSelector);
    }




    // Manejar listar "Ver todas las cuentas"
    function handleViewAllAccounts(buttonSelector, modalSelector, tableSelector, apiUrl) {
        $(buttonSelector).on('click', function() {
            $.ajax({
                url: apiUrl,  // URL para obtener todas las cuentas
                method: "GET",
                success: function(data) {
                    console.log("Informacion cuenta", data);
                    var table = $(tableSelector).DataTable();
                    // Mostrar
                    table.clear();
                    data.cuentas.forEach(function(cuenta) {
                        table.row.add([
                            cuenta.id,
                            cuenta.nombre,
                            cuenta.banco,
                            cuenta.numeroCuenta,
                            cuenta.tipoCuenta
                        ]).draw();
                    });
                    // Mostrar la ventana modal
                    $(modalSelector).modal('show');
                },
                error: function(xhr) {
                    console.error("Error al obtener cuentas: ", xhr.responseText);
                }
            });
        });
    }
    
    // Manejar listar "Ver todos los usuarios"
    function handleViewallUsers(buttonSelector, modalSelector, tableSelector, apiUrl) {
        console.log("Boton ver todos los usuarios");

        $(buttonSelector).on('click', function() {

            $.ajax({
                url: apiUrl,  // URL para obtener todas los usuarios
                method: "GET",
                success: function(data) {
                    console.log("Informacion usuario", data);
                    var table = $(tableSelector).DataTable();
                    // Mostrar
                    table.clear();
                    data.usuarios.forEach(function(usuario) {
                        table.row.add([
                            usuario.id,
                            usuario.nombre_usuario,
                            usuario.nombre,
                            usuario.apellido,
                            usuario.correo,
                        ]).draw();
                    });
                    // Mostrar la ventana modal
                    $(modalSelector).modal('show');
                },
                error: function(xhr) {
                    console.error("Error al obtener usuarios: ", xhr.responseText);
                }
            });
        });
    }
    // Manejar listar "Ver todas las prestamos"
    function handleViewAllloan(buttonSelector, modalSelector, tableSelector, apiUrl) {
        $(buttonSelector).on('click', function() {
            $.ajax({
                url: apiUrl,  // URL para obtener todas las cuentas
                method: "GET",
                success: function(data) {
                    console.log("Informacion prestamo", data);
                    var table = $(tableSelector).DataTable();
                    // Mostrar
                    table.clear();
                    data.prestamos.forEach(function(prestamo) {
                        table.row.add([
                            prestamo.id,
                            prestamo.descripcion,
                            prestamo.monto_total,
                            prestamo.tasa_interes,
                            prestamo.fecha_inicio,
                            prestamo.usuario_prestamista,
                            prestamo.fechaIngreso,
                        ]).draw();
                    });
                    // Mostrar la ventana modal
                    $(modalSelector).modal('show');
                },
                error: function(xhr) {
                    console.error("Error al obtener prestamos: ", xhr.responseText);
                }
            });
        });
    }
    // Manejar listar "Ver todas las bancos"
    function handleViewAllBanks(buttonSelector, modalSelector, tableSelector, apiUrl) {
        $(buttonSelector).on('click', function() {
            $.ajax({
                url: apiUrl,  // URL para obtener todas las cuentas
                method: "GET",
                success: function(data) {
                    console.log("Informacion banco", data);
                    var table = $(tableSelector).DataTable();
                    // Mostrar
                    table.clear();
                    data.bancos.forEach(function(banco) {
                        table.row.add([
                            banco.id,
                            banco.nombre,
                            banco.direccion,
                            banco.telefono,
                        ]).draw();
                    });
                    // Mostrar la ventana modal
                    $(modalSelector).modal('show');
                },
                error: function(xhr) {
                    console.error("Error al obtener bancos: ", xhr.responseText);
                }
            });
        });
    }

    // Validando que funciones se van a a utilizar 
    var modelo_principal = $("#modelo_principal").val();

if (modelo_principal == "Deuda"){
        // Inicializar funciones - Formulario deuda
        // ♠ Manejar el envío del formulario ♠
        handleFormSubmit('#form-agregar-deuda', '/crear_deuda/');
        // ○ Cargar formularios extras (Usuario)
        handleFormLoad('#agregar-usuario', '/crear_usuario/', '#insert-form-agregar-usuario', '#modalAgregarUsuario');
        // ○ Cargar formularios extras (Cuentas)
        handleFormLoad('#agregar-tarjeta', '/crear_tarjeta_credito/', '#insert-form-agregar-tarjeta', '#modalAgregarTarjeta');
        // ○ Cargar formularios extras (Prestamos)
        handleFormLoad('#agregar-prestamo', '/crear_prestamo/', '#insert-form-agregar-prestamo', '#modalAgregarPrestamo');

        // ♣ Manejar la búsqueda de usuarios de manera dinámica ♣
        
        // • Buscar usuarios dinamicamente •
        handleUserSearch('#usuario_deudor', '#lista-usuarios', '/api/buscar_dinamica_usuarios/');
        // • Buscar cuentas dinamicamente •
        handleAccountSearch('#tarjeta', '#lista-tarjetas', '/api/buscar_dinamica_tarjetas_credito/');
        // • Buscar prestamos dinamicamente •
        handleLoanSearch('#prestamo', '#lista-prestamos', '/api/buscar_dinamica_prestamos/');
        

        // ♦ Manejar el clic en las listas ♦
        // • Usuario •
        handleUserSelection('#lista-usuarios', '#usuario_deudor', '#usuario_deudor_id');
        // • Tarjeta •
        handleAccountSelection('#lista-tarjetas', '#tarjeta', '#tarjeta_id');
        // • Prestamo •
        handleLoanSelection('#lista-prestamos', '#prestamo', '#prestamo_id');


        // ○ Manejar el clic en el botón "Ver todos los registros"
        // • Usuarios •
        handleViewallUsers('#ver-todos-usuarios', '#modalUsuarios', '#tabla-usuarios', '/api/usuarios/');
        // • Tarjetas •
        handleViewAllAccounts('#ver-todas-tarjetas', '#modalTarjetas', '#tabla-tarjetas', '/api/cuentas/');
        // • Prestamos •
        handleViewAllloan('#ver-todos-prestamos', '#modalPrestamos', '#tabla-prestamos', '/api/prestamos/');


        


    } else if(modelo_principal == "Préstamo"){
        // Inicializar funciones - Formulario cuenta
        // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-prestamo', '/crear_prestamo/');
        // ○ Cargar formularios extras (Usuario)
        handleFormLoad('#agregar-usuario', '/crear_usuario/', '#insert-form-agregar-usuario', '#modalAgregarUsuario');
        
        // • Buscar usuarios dinamicamente •
        handleUserSearch('#usuario_prestamista', '#lista-usuarios', '/api/buscar_dinamica_usuarios/');
        // ♦ Manejar el clic en las listas ♦
        // • Usuario •
        handleUserSelection('#lista-usuarios', '#usuario_prestamista', '#usuario_prestamista_id');
        // ○ Manejar el clic en el botón "Ver todos los registros"
        // • Usuarios •
        handleViewallUsers('#ver-todos-usuarios', '#modalUsuarios', '#tabla-usuarios', '/api/usuarios/'); 
        
    } else if (modelo_principal == "Tarjeta de Crédito"){
        // Inicializar funciones - Formulario tarjeta
        // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-tarjeta-credito', '/crear_tarjeta_credito/');
    } else if (modelo_principal == "Banco"){
        // Inicializar funciones - Formulario banco
        // Manejar el envío del formulario (Banco)
        handleFormSubmit('#form-agregar-banco', '/crear_banco/');
    } else if (modelo_principal == "Cuenta Bancaria"){
        // Inicializar funciones - Formulario Cuenta Bancaria
        // Manejar el envío del formulario (Cuenta Bancaria)
        handleFormSubmit('#form-agregar-cuenta-bancaria', '/crear_cuenta_bancaria/');
        // ○ Cargar formularios extras (Banco)
        handleFormLoad('#agregar-banco', '/crear_banco/', '#insert-form-agregar-banco', '#modalAgregarBanco');
        // ○ Cargar formularios extras (Usuario)
        handleFormLoad('#agregar-usuario', '/crear_usuario/', '#insert-form-agregar-usuario', '#modalAgregarUsuario');
        
        // • Buscar bancos dinamicamente •
        handleBankSearch('#banco', '#lista-bancos', '/api/buscar_dinamica_bancos/');
        // • Buscar usuarios dinamicamente •
        handleUserSearch('#usuario', '#lista-usuarios', '/api/buscar_dinamica_usuarios/');
        
        // • Banco •
        handleBankSelection('#lista-bancos', '#banco', '#banco_id');
        // • Usuario •
        handleUserSelection('#lista-usuarios', '#usuario', '#usuario_id');

        // ○ Manejar el clic en el botón "Ver todos los registros"
        // • Bancos •
        handleViewAllBanks('#ver-todos-bancos', '#modalBancos', '#tabla-bancos', '/api/bancos/');
        // • Usuarios •
        handleViewallUsers('#ver-todos-usuarios', '#modalUsuarios', '#tabla-usuarios', '/api/usuarios/');

    } else if (modelo_principal == "Usuario"){
        // Inicializar funciones - Formulario Usuario
        // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-usuario', '/crear_usuario/');
        
    } else if (modelo_principal == "Ingreso"){
        // Inicializar funciones - Formulario ingreso
             // Manejar el envío del formulario
             handleFormSubmit('#form-agregar-ingreso', '/crear_ingreso/');
             // Manejar la búsqueda de cuentas de manera dinámica
         handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
             // Manejar el clic en una cuenta de la lista
         handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
             // Manejar el clic en el botón "Ver todas las cuentas"
         handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
         // Cargar formularios extras
         handleFormLoad('#agregar-cuenta', '/crear_cuenta_bancaria/', '#insert-form-agregar-cuenta-bancaria', '#modalAgregarCuenta');

    } else if (modelo_principal == "Egreso"){
        // Inicializar funciones - Formulario egreso
        // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-egreso', '/crear_egreso/');
        // Manejar la búsqueda de cuentas de manera dinámica
        handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
        // Manejar el clic en una cuenta de la lista
        handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
        // Manejar el clic en el botón "Ver todas las cuentas"
        handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
        // Cargar formularios extras
        handleFormLoad('#agregar-cuenta', '/crear_cuenta_bancaria/', '#insert-form-agregar-cuenta-bancaria', '#modalAgregarCuenta');
    }

    if (modelo_principal == "Ingreso_Actualizado"){
        // Extraer el id de la url
        id = $("#id_formulario").val();
        // Cargar los datos del formulario
        handleFormLoadDataincome(`../../../api/cargar_registros_ingresos/${id}/`);
             // Manejar el actualizacion del formulario
        handleFormSubmit('#form-agregar-ingreso', `../../../api/editar_ingreso/${id}/`, metodo="POST", modalSelector="modalEditarIngreso");
             // Manejar la búsqueda de cuentas de manera dinámica
         handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
             // Manejar el clic en una cuenta de la lista
         handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
             // Manejar el clic en el botón "Ver todas las cuentas"
         handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
         // Cargar formularios extras
         handleFormLoad('#agregar-cuenta', '/crear_cuenta_bancaria/', '#insert-form-agregar-cuenta-bancaria', '#modalAgregarCuenta');

         
    } else if (modelo_principal == "Egreso_Actualizado"){
        // Extraer el id de la url
        id = $("#id_formulario").val();
        // Cargar los datos del formulario
        handleFormLoadDataincome(`../../../api/cargar_registros_egresos/${id}/`);
        // Manejar el actualizacion del formulario
        handleFormSubmit('#form-agregar-egreso', `../../../api/editar_egreso/${id}/`, metodo="POST", modalSelector="modalEditarEgreso");
        // Manejar la búsqueda de cuentas de manera dinámica
        handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
        // Manejar el clic en una cuenta de la lista
        handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
        // Manejar el clic en el botón "Ver todas las cuentas"
        handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
        // Cargar formularios extras
        handleFormLoad('#agregar-cuenta', '/crear_cuenta_bancaria/', '#insert-form-agregar-cuenta-bancaria', '#modalAgregarCuenta');
        } else if (modelo_principal == "Cuenta_bancaria"){
        // Extraer el id de la url
        id = $("#id_formulario").val();
        // Cargar los datos del formulario
        handleFormLoadDataincome(`../../../api/cargar_registros_cuenta_bancaria/${id}/`);
        // Manejar el actualizacion del formulario
        handleFormSubmit('#form-agregar-cuenta-bancaria', `../../../api/editar_cuenta_bancaria/${id}/`, metodo="POST", modalSelector="modalEditarCuenta");
        // Manejar la búsqueda de bancos de manera dinámica
        handleBankSearch('#banco', '#lista-bancos', '/api/buscar_dinamica_bancos/');
        // Manejar la búsqueda de usuarios de manera dinámica
        handleUserSearch('#usuario', '#lista-usuarios', '/api/buscar_dinamica_usuarios/');
        // Manejar el clic en un banco de la lista
        handleBankSelection('#lista-bancos', '#banco', '#banco_id');
        // Manejar el clic en un usuario de la lista
        handleUserSelection('#lista-usuarios', '#usuario', '#usuario_id');
        // Cargar formularios extras
        handleFormLoad('#agregar-banco', '/crear_banco/', '#insert-form-agregar-banco', '#modalAgregarBanco');
        handleFormLoad('#agregar-usuario', '/crear_usuario/', '#insert-form-agregar-usuario', '#modalAgregarUsuario');
}

});