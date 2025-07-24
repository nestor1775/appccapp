from firebase_admin import messaging, credentials, initialize_app, get_app
from decouple import config
import json

"""  local  def get_firebase_app():
    try:
        # Intenta obtener la aplicación existente
        return get_app()
    except ValueError as e:
        if "The default Firebase app does not exist" in str(e):
            # Si no existe, la creamos
            cred_path = config('FIREBASE_CREDENTIALS_PATH')
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"No se encontró el archivo de credenciales en: {cred_path}")
            
            try:
                cred = credentials.Certificate(cred_path)
                return initialize_app(cred)
            except Exception as e:
                print(f"Error al inicializar Firebase: {e}")
                raise
        else:
            raise

"""
def get_firebase_app():
    try:
        return get_app()
    except ValueError as e:
        if "The default Firebase app does not exist" in str(e):
            # Leer el JSON desde la variable de entorno
            cred_json = config('FIREBASE_CREDENTIALS_JSON', default=None)
            
            if not cred_json:
                raise ValueError("FIREBASE_CREDENTIALS_JSON environment variable is not set or is empty")
                
            if isinstance(cred_json, bool):
                raise ValueError("FIREBASE_CREDENTIALS_JSON is a boolean, expected a JSON string")
                
            try:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
                return initialize_app(cred)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in FIREBASE_CREDENTIALS_JSON: {e}")
            except Exception as e:
                raise ValueError(f"Error initializing Firebase: {e}")
        else:
            raise

def enviar_notificacion(usuario, mensaje):
    """
    Envía una notificación push a un usuario específico.
    
    Args:
        usuario: Instancia del modelo User al que se le enviará la notificación
        mensaje (str): El mensaje de la notificación
    """
    try:
        # Asegurarse de que Firebase esté inicializado
        get_firebase_app()
        # Obtener los tokens de dispositivo del usuario
        from api.models import Device
        dispositivos = Device.objects.filter(user=usuario)
        
        if not dispositivos.exists():
            print(f"El usuario {usuario.username} no tiene dispositivos registrados")
            return False
        
        for dispositivo in dispositivos:
            message = messaging.Message(
                notification=messaging.Notification(
                    title='Nueva tarea asignada',
                    body=mensaje,
                ),
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        sound='mi_sonido_personalizado.mp3', 
                    ),
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound='alert.caf',  
                        ),
                    ),
                ),
                token=dispositivo.token,
            )
            response = messaging.send(message)
            print(f"Notificación enviada a {usuario.username}: {response}")

        
        return True
    except Exception as e:
        print(f"Error al enviar notificación: {e}")
        return False
