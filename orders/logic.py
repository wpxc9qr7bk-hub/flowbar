from users.models import Trabajador
from orders.models import Pedidos
from django.db.models import Count, Q

def assign_bartender_algorithm():
    """
    Algoritmo mejorado: Busca al Bartender con MENOS pedidos ACTIVOS ('PREPARACION').
    Ignora los pedidos que ya están 'LISTO' o 'ENTREGADO'.
    """
    
    trabajadores = Trabajador.objects.all()
    
    if not trabajadores.exists():
        return None
    
    # ANOTACIÓN CON FILTRO:
    # Contamos solo los pedidos donde estado='PREPARACION'
    trabajadores_con_carga = trabajadores.annotate(
        carga_actual=Count('pedidos', filter=Q(pedidos__estado='PREPARACION'))
    ).order_by('carga_actual') 
    
    # .first() nos da el que tiene el número más bajo de carga_actual
    best_bartender = trabajadores_con_carga.first()
    
    # Debug: Imprimimos en la consola quién tiene cuántos pedidos para que verifiques
    print(f"--- ASIGNACIÓN DE CARGA ---")
    for t in trabajadores_con_carga:
        print(f"Bartender: {t.nom_trabajador} | Carga Activa: {t.carga_actual}")
    print(f"--> Asignado a: {best_bartender.nom_trabajador}")
    print("---------------------------")
    
    return best_bartender