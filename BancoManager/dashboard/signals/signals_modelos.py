from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
#  _____                                                                 _____ 
# ( ___ )                                                               ( ___ )
#  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
#  |   |  __  __  ___  ____  _____ _     ___  ____                       |   | 
#  |   | |  \/  |/ _ \|  _ \| ____| |   / _ \/ ___|                      |   | 
#  |   | | |\/| | | | | | | |  _| | |  | | | \___ \                      |   | 
#  |   | | |  | | |_| | |_| | |___| |__| |_| |___) |                     |   | 
#  |   | |_|__|_|\___/|____/|_____|_____\___/|____/   _     _____ ____   |   | 
#  |   | |  _ \|  _ \|_ _| \ | |/ ___|_ _|  _ \ / \  | |   | ____/ ___|  |   | 
#  |   | | |_) | |_) || ||  \| | |    | || |_) / _ \ | |   |  _| \___ \  |   | 
#  |   | |  __/|  _ < | || |\  | |___ | ||  __/ ___ \| |___| |___ ___) | |   | 
#  |   | |_|   |_| \_\___|_| \_|\____|___|_| /_/   \_\_____|_____|____/  |   | 
from ..modelo_deudas.models_deudas import *
from ..modelo_banco.models_banco import *
from ..modelo_auditlog.modelo_auditlog import *
from ..modelo_dinero.models_dinero import *
from ..utils.generales import *
#  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
# (_____)                                                               (_____)

# /==================================================================================\
# || _____ ______   ________  ________  _______   ___       ________  ________      ||
# |||\   _ \  _   \|\   __  \|\   ___ \|\  ___ \ |\  \     |\   __  \|\   ____\     ||
# ||\ \  \\\__\ \  \ \  \|\  \ \  \_|\ \ \   __/|\ \  \    \ \  \|\  \ \  \___|_    ||
# || \ \  \\|__| \  \ \  \\\  \ \  \ \\ \ \  \_|/_\ \  \    \ \  \\\  \ \_____  \   ||
# ||  \ \  \    \ \  \ \  \\\  \ \  \_\\ \ \  \_|\ \ \  \____\ \  \\\  \|____|\  \  ||
# ||   \ \__\    \ \__\ \_______\ \_______\ \_______\ \_______\ \_______\____\_\  \ ||
# ||    \|__|     \|__|\|_______|\|_______|\|_______|\|_______|\|_______|\_________\||
# ||                                                                    \|_________|||
# ||                                                                                ||
# ||                                                                                ||
# || ___  ___  _________  ___  ___       ________                                   ||
# |||\  \|\  \|\___   ___\\  \|\  \     |\   ____\                                  ||
# ||\ \  \\\  \|___ \  \_\ \  \ \  \    \ \  \___|_                                 ||
# || \ \  \\\  \   \ \  \ \ \  \ \  \    \ \_____  \                                ||
# ||  \ \  \\\  \   \ \  \ \ \  \ \  \____\|____|\  \                               ||
# ||   \ \_______\   \ \__\ \ \__\ \_______\____\_\  \                              ||
# ||    \|_______|    \|__|  \|__|\|_______|\_________\                             ||
# ||                                       \|_________|                             ||
# \==================================================================================/
from ..modelo_utils.modelo_inter import *
# /==================================================================================\
@receiver(post_save, sender=CuentaBancaria)
def crear_tarjeta_credito(sender, instance, created, **kwargs):
    """
    Signal para crear una Tarjeta de Crédito automáticamente
    al crear una nueva CuentaBancaria si el tipo es credito.
    """
    if created and instance.tipoCuenta == 'Credito':
        try:
            # Crear una Tarjeta de Crédito asociada a la cuenta
            TarjetaCredito.objects.create(
                cuenta=instance,
                numero_tarjeta=f"0000{instance.numeroCuenta[-4:]}",
                nombre_titular=instance.usuario.get_full_name(),
                fecha_inicio=instance.fechaIngreso,
                fecha_corte=instance.fechaIngreso + timedelta(days=15),
                fecha_limite_pago=instance.fechaIngreso + timedelta(days=30),
                fecha_vencimiento=instance.fechaIngreso + timedelta(days=365),
                colorIdentificacion='#38daf7',
                limite=0,
                usuario=instance.usuario
            )
        except ValidationError as e:
            # Manejo de errores para validaciones específicas del modelo
            print(f"Error al crear Tarjeta de Crédito: {e}")
        except Exception as e:
            # Manejo de errores genéricos
            print(f"Ocurrió un error no esperado funcion crear tarjeta de credito: {e}")


# /==================================================================================\
@receiver(post_save, sender=Ingreso)
def crear_registro_ingreso(sender, instance, created, **kwargs):
    """
    Signal para crear un RegistroIngreso automáticamente
    al agregar un nuevo Ingreso, y actualizar el saldo de
    la cuenta bancaria asociada.
    """
    if created:
        try:
            # Crear el RegistroIngreso
            registro_ingreso = RegistroIngreso.objects.create(
                cuenta=instance.cuenta,  # Cuenta asociada desde Ingreso
                monto=instance.cantidad,  # Cantidad del Ingreso
                fecha=instance.fecha,     # Fecha del Ingreso
                descripcion=instance.descripcion or "Ingreso registrado automáticamente"
            )
            registro_ingreso.aplicar_ingreso()  # Aplicar ingreso al saldo de la cuenta

        except ValidationError as e:
            # Manejo de errores para validaciones específicas del modelo
            print(f"Error al crear RegistroIngreso: {e}")
        except Exception as e:
            # Manejo de errores genéricos
            print(f"Ocurrió un error no esperado crear registro ingreso: {e}")

@receiver(post_save, sender=Egreso)
def crear_registro_egreso(sender, instance, created, **kwargs):
    """
    Signal para crear un RegistroEgreso automáticamente
    en caso de que el flujo del negocio necesite registrar un egreso
    de un ingreso para, por ejemplo, registrar movimientos netos.
    """
    if created:
        try:
            # Crear el RegistroEgreso a partir del Ingreso
            registro_egreso = RegistroEgreso.objects.create(
                cuenta=instance.cuenta,  # Cuenta asociada desde Ingreso
                monto=instance.cantidad,  # Monto que refleja el 'egreso' que podría estar asimilando un retorno
                fecha=instance.fecha,     # Fecha del registro
                descripcion=f"Transacción automática basada en el Egreso: {instance.descripcion} - {instance.proposito}",
                usuario=instance.usuario  # Usuario asociado
            )
            
            # Intentamos aplicar el egreso (lo mismo que saldo negativo en cuenta)
            registro_egreso.aplicar_egreso()

        except ValidationError as e:
            # Manejo de errores para validaciones específicas del modelo
            print(f"Error al crear RegistroEgreso: {e}")
        except Exception as e:
            # Manejo de errores genéricos
            print(f"Ocurrió un error no esperado crear registro egreso: {e}")

@receiver(post_save, sender=Ingreso)
def actualizar_saldo_cuenta_ingreso(sender, instance, created, **kwargs):
    """
    Signal para actualizar el saldo de la cuenta asociada a un Ingreso
    cuando se crea o actualiza un ingreso.
    """
    try:
        with transaction.atomic():
            cuenta = instance.cuenta
            if created:
                # Si es un nuevo ingreso, simplemente suma la cantidad
                cuenta.saldoInicial += instance.cantidad
            else:
                # Obtener ingreso anterior y actualizar saldo
                ingreso_anterior = Ingreso.objects.get(pk=instance.pk)
                actualizar_saldo(cuenta, ingreso_anterior.cantidad, instance.cantidad)
            cuenta.save()
    except Exception as e:
        # Manejo de errores genéricos
        print(f"Ocurrió un error al actualizar el saldo de ingreso: {e}")

@receiver(post_save, sender=Egreso)
def actualizar_saldo_cuenta_egreso(sender, instance, created, **kwargs):
    """
    Signal para actualizar el saldo de la cuenta asociada a un Egreso
    cuando se crea o actualiza un egreso.
    """
    try:
        with transaction.atomic():
            cuenta = instance.cuenta
            if created:
                # Si es un nuevo egreso, simplemente resta la cantidad
                cuenta.saldoInicial -= instance.cantidad
            else:
                # Obtener egreso anterior y actualizar saldo
                egreso_anterior = Egreso.objects.get(pk=instance.pk)
                actualizar_saldo(cuenta, egreso_anterior.cantidad, instance.cantidad)
            cuenta.save()
    except Exception as e:
        # Manejo de errores genéricos
        print(f"Ocurrió un error al actualizar el saldo de egreso: {e}")

# /==================================================================================\
@receiver(post_save, sender=Prestamo)
def crear_deuda_al_prestamo(sender, instance, created, **kwargs):
    """
    Signal para crear una Deuda automáticamente al crear un nuevo Prestamo.
    """
    if created:
        try:
            # Calcular una fecha de vencimiento predeterminada a 30 días después de la fecha de inicio del préstamo
            fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)
            # Crear la Deuda asociada al préstamo
            Deuda.objects.create(
                usuario_deudor=instance.usuario_prestamista,  # Se considera usuario prestamista como deudor aquí
                monto=instance.monto_total,
                tipo_deuda='prestamo',
                descripcion=f'Deuda generada por el préstamo {instance.id}',
                prestamo=instance,
                fecha_vencimiento=fecha_vencimiento
            )
        except ValidationError as e:
            # Manejo de errores específicos de validación
            print(f"Error al crear Deuda: {e}")
        except Exception as e:
            # Manejo de errores genéricos
            print(f"Ocurrió un error no esperado crear deuda al prestamo: {e}")


@receiver(post_save, sender=Prestamo)
def actualizar_prestamo_estado(sender, instance, created, **kwargs):
    """
    Signal que se activa al crear o actualizar un Prestamo.
    Actualiza el estado de la deuda asociada cuando el préstamo
    es marcado como saldado.
    """
    try:
        if not created and instance.estado:  # Solo si el préstamo es actualizado y está saldado
            actualizar_estado_deuda(instance)

    except Exception as e:
        print(f"Ocurrió un error al intentar actualizar el estado del préstamo: {e}")

@receiver(post_save, sender=TarjetaCredito)
def crear_deuda_por_tarjeta(sender, instance, **kwargs):
    """
    Signal para crear una Deuda automáticamente al eliminar una Tarjeta de Crédito.
    """
    try:
        # Calcular una fecha de vencimiento predeterminada a 30 días después de la fecha de inicio del préstamo
        fecha_vencimiento = calcular_fecha_vencimiento(instance.fecha_inicio)
        # Crear una Deuda por el saldo pendiente de la tarjeta
        Deuda.objects.create(
            usuario_deudor=instance.usuario,
            monto=instance.saldo,
            tipo_deuda='tarjeta',
            descripcion=f'Deuda generada por la tarjeta {instance.numero_tarjeta}',
            tarjeta=instance,
            fecha_vencimiento=fecha_vencimiento
        )
    except ValidationError as e:
        # Manejo de errores específicos de validación
        print(f"Error al crear Deuda por tarjeta: {e}")
    except Exception as e:
        # Manejo de errores genéricos
        print(f"Ocurrió un error no esperado crear deuda a una tarjeta: {e}")

# /==================================================================================\
@receiver(post_save, sender=Deuda)
def alertar_deuda_alta(sender, instance, created, **kwargs):
    """
    Signal que se activa al crear o actualizar una Deuda.
    Verifica si el monto de la deuda supera un límite preestablecido
    y envía una alerta si es el caso.
    """
    try:
        # Definir el límite para la alerta de deuda
        LIMITE_DEUDA = 20000  # Este valor puede definirse en la configuración o en un archivo de constantes

        # Si la deuda es recién creada o actualizada y supera el límite
        if instance.monto > LIMITE_DEUDA:
            enviar_alerta_deuda_alta(instance.usuario_deudor, instance.monto)

    except Exception as e:
        # Manejo de errores genéricos
        print(f"Ocurrió un error al enviar la alerta de deuda alta: {e}")