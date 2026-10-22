# src/server.py
import socket
import json
import time
import convert

HOST = '127.0.0.1'  
PORT = 50051        

def process_and_stream(conn, request_data: dict):
    """Procesa la petición y envía actualizaciones de progreso en tiempo real."""
    action = request_data.get('action')
    payload = request_data.get('payload', {})
    
    try:
        if action == 'pdf_to_word':
            # Fase 1: Inicio
            send_progress(conn, 10, "Iniciando lectura del PDF...")
            
            # Fase 2: Conversión a Word (Llamada REAL)
            send_progress(conn, 40, "Convirtiendo estructura y corrigiendo LaTeX...")
            
            # ¡AQUÍ ESTÁ LA MAGIA REAL!
            success = convert.pdf_to_word(payload['input_path'], payload['output_path'])
            
            if success:
                # Fase Final
                send_progress(conn, 100, "¡Conversión finalizada!")
                send_final_result(conn, "ok", "Archivo guardado exitosamente.")
            else:
                send_final_result(conn, "error", "Fallo durante la conversión en Python.")
            
        else:
            send_final_result(conn, "error", f"Acción '{action}' desconocida")
            
    except Exception as e:
        send_final_result(conn, "error", str(e))

def send_progress(conn, percent: int, message: str):
    """Envía un paquete JSON de progreso."""
    data = {"type": "progress", "percent": percent, "message": message}
    # Añadimos \n al final para que C++ pueda separar los mensajes
    conn.sendall((json.dumps(data) + "\n").encode('utf-8'))

def send_final_result(conn, status: str, message: str):
    """Envía el paquete JSON final."""
    data = {"type": "result", "status": status, "message": message}
    conn.sendall((json.dumps(data) + "\n").encode('utf-8'))

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Backend asíncrono escuchando en {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue
                
                try:
                    request_str = data.decode('utf-8')
                    request_data = json.loads(request_str)
                    print(f"Iniciando tarea: {request_data['action']}")
                    
                    # Llamamos a la función que emitirá múltiples respuestas
                    process_and_stream(conn, request_data)
                    
                except json.JSONDecodeError:
                    send_final_result(conn, "error", "JSON inválido")

if __name__ == "__main__":
    start_server()