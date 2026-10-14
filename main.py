import sqlite3
from typing import List, Dict, Any

def obtener_conexion() -> sqlite3.Connection:
    conexion = sqlite3.connect("gestion_asistencia.db")
    return conexion

def inicializar_base_datos() -> None:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marcas_asistencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            marca_tiempo TEXT NOT NULL,
            metodo_marcado TEXT NOT NULL,
            coordenadas_gps TEXT NOT NULL,
            etiqueta_modificado TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

class MarcaAsistencia:
    def __init__(self, tipo: str, marca_tiempo: str, metodo_marcado: str, coordenadas_gps: str, etiqueta_modificado: str, id_registro: int = None):
        self.id: int = id_registro
        self.tipo: str = tipo
        self.marca_tiempo: str = marca_tiempo
        self.metodo_marcado: str = metodo_marcado
        self.coordenadas_gps: str = coordenadas_gps
        self.etiqueta_modificado: str = etiqueta_modificado

class RepositorioAsistencia:
    def insertar_marca(self, marca: MarcaAsistencia) -> None:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """INSERT INTO marcas_asistencia 
                 (tipo, marca_tiempo, metodo_marcado, coordenadas_gps, etiqueta_modificado) 
                 VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sql, (marca.tipo, marca.marca_tiempo, marca.metodo_marcado, 
                             marca.coordenadas_gps, marca.etiqueta_modificado))
        conexion.commit()
        conexion.close()
        print(f"[OK] Inserción realizada: Evento de '{marca.tipo}' registrado exitosamente.")

    def consultar_historial_cronologico(self) -> List[Dict[str, Any]]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """SELECT id, tipo, marca_tiempo, metodo_marcado, coordenadas_gps, etiqueta_modificado 
                 FROM marcas_asistencia ORDER BY id DESC"""
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()
        historial = []
        for fila in filas:
            historial.append({
                "id": fila[0],
                "tipo": fila[1],
                "marca_tiempo": fila[2],
                "metodo_marcado": fila[3],
                "coordenadas_gps": fila[4],
                "etiqueta_modificado": fila[5]
            })
        return historial

    def actualizar_marca(self, id_registro: int, nuevo_tipo: str, nueva_hora: str) -> None:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = """UPDATE marcas_asistencia 
                 SET tipo = ?, marca_tiempo = ?, etiqueta_modificado = ? 
                 WHERE id = ?"""
        cursor.execute(sql, (nuevo_tipo, nueva_hora, "Modificado", id_registro))
        conexion.commit()
        conexion.close()
        print(f"[OK] Actualización realizada: Registro #{id_registro} marcado como 'Modificado'.")

    def eliminar_marca(self, id_registro: int) -> None:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "DELETE FROM marcas_asistencia WHERE id = ?"
        cursor.execute(sql, (id_registro,))
        conexion.commit()
        conexion.close()
        print(f"[OK] Eliminación realizada: Registro #{id_registro} borrado de la base de datos.")

if __name__ == "__main__":
    print("--- INICIANDO SIMULACIÓN DEL SISTEMA DE GESTIÓN DE ASISTENCIA ---")
    inicializar_base_datos()
    repositorio = RepositorioAsistencia()

    print("\nEjecutando Inserciones...")
    marca_entrada = MarcaAsistencia(
        tipo="Entrada", 
        marca_tiempo="2026-08-27 06:01:15", 
        metodo_marcado="Reconocimiento facial", 
        coordenadas_gps="6.2442,-75.5812", 
        etiqueta_modificado="Normal"
    )
    marca_almuerzo = MarcaAsistencia(
        tipo="Almuerzo", 
        marca_tiempo="2026-08-27 12:05:00", 
        metodo_marcado="Clave Personal", 
        coordenadas_gps="6.2443,-75.5811", 
        etiqueta_modificado="Normal"
    )
    repositorio.insertar_marca(marca_entrada)
    repositorio.insertar_marca(marca_almuerzo)

    print("\nEjecutando Consulta de Historial...")
    historial_actual = repositorio.consultar_historial_cronologico()
    for registro in historial_actual:
        print(f"ID: {registro['id']} | Evento: {registro['tipo']} | Hora: {registro['marca_tiempo']} | Estado: {registro['etiqueta_modificado']}")

    if historial_actual:
        print("\nEjecutando Actualización Administrativa...")
        id_a_modificar = historial_actual[0]['id']
        repositorio.actualizar_marca(id_registro=id_a_modificar, nuevo_tipo="Almuerzo", nueva_hora="2026-08-27 12:00:00")
        
        print("\nVerificando datos después de actualizar:")
        historial_actualizado = repositorio.consultar_historial_cronologico()
        for registro in historial_actualizado:
            if registro['id'] == id_a_modificar:
                print(f"-> REGISTRO CAMBIADO: ID: {registro['id']} | Evento: {registro['tipo']} | Hora: {registro['marca_tiempo']} | Estado: {registro['etiqueta_modificado']}")

    if historial_actual:
        print("\nEjecutando Eliminación de Registro...")
        id_a_eliminar = historial_actual[-1]['id']
        repositorio.eliminar_marca(id_registro=id_a_eliminar)
        
        print("\nHistorial Final en Base de Datos:")
        historial_final = repositorio.consultar_historial_cronologico()
        if not historial_final:
            print("[Vacío] No quedan registros.")
        else:
            for registro in historial_final:
                print(f"ID: {registro['id']} | Evento: {registro['tipo']} | Hora: {registro['marca_tiempo']}")
