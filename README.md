# CrewCall Backend — Documentación y Seguridad

## Índice
- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos y Relaciones](#modelos-y-relaciones)
- [Serializadores](#serializadores)
- [Vistas y Endpoints](#vistas-y-endpoints)
- [Permisos y Seguridad](#permisos-y-seguridad)
- [Casos de Uso Cubiertos](#casos-de-uso-cubiertos)
- [Ejemplos de Código y Validaciones](#ejemplos-de-código-y-validaciones)

---

## Descripción General
CrewCall es un backend Django para la gestión de embarcaciones, usuarios, tareas, mensajes predefinidos, habitaciones y usuarios invitados (guests). El sistema está diseñado para garantizar la privacidad y seguridad de los datos de cada embarcación, evitando cualquier acceso indebido entre usuarios de diferentes crews.

---

## Estructura del Proyecto

- **api/models/**: Modelos principales (`User`, `Vessel`, `UserVessel`, `Room`, `PredefinedMessage`, `Guest`, `Task`).
- **api/serializers/**: Serializadores para exponer y validar datos de los modelos.
- **api/views/**: Vistas API para cada recurso, con lógica de permisos y filtrado por vessel.
- **api/permissions.py**: Permisos personalizados (`IsAdmin`, `IsAuthenticatedOrGuestWithToken`, etc).
- **api/urls.py**: Rutas de la API.
- **crewcall/settings.py**: Configuración global, seguridad, CORS, JWT, etc.

---

## Modelos y Relaciones

- **User**: Usuario con rol (`admin` o `worker`), email único y especialidad.
- **Vessel**: Embarcación con código único y pin de invitado.
- **UserVessel**: Relación usuario-embarcación, con rol, estado (`active`, `pending`, `revoked`) y flag `is_primary`.
- **Guest**: Invitado asociado a una vessel mediante un token único.
- **Room**: Habitación asociada a una vessel.
- **PredefinedMessage**: Mensaje predefinido asociado a una vessel.
- **Task**: Tarea asociada a una vessel, puede ser creada por admin o guest, asignada a un worker.

---

## Serializadores

- **UserSerializer**: Expone datos del usuario y su primer vessel activo.
- **VesselSerializer**: Expone datos de la vessel, usando `unique_code`.
- **TaskCreateSerializer**: Valida que solo admin o guest puedan crear tareas, y que el worker asignado pertenezca a la misma vessel.
- **PredefinedMessageSerializer**: Expone mensajes predefinidos, usando `unique_code` de la vessel.
- **RoomSerializer**: Expone habitaciones, usando `unique_code` de la vessel.
- **GuestSerializer**: Expone datos del guest y su vessel.

---

## Vistas y Endpoints

- **Autenticación JWT**: `/api/token/`, `/api/token/refresh/`
- **Usuarios**: `/api/users/`, `/api/users/<id>/`, `/api/users/profile/`
- **Workers**: `/api/workers/`, `/api/workers/<id>/`
- **Vessels**: `/api/vessels/`, `/api/vessels/<id>/`, `/api/vessel/register/`, `/api/vessels/join/`, `/api/vessels/my-join-requests/`
- **Rooms**: `/api/rooms/`, `/api/rooms/register/`, `/api/rooms/<id>/`
- **Tareas**: `/api/tasks/`, `/api/tasks/create/`, `/api/tasks/<id>/`
- **Mensajes predefinidos**: `/api/messages/`, `/api/message/register/`, `/api/messages/<id>/`
- **Guests**: `/api/guests/`, `/api/guests/register/`, `/api/guests/<id>/`

Cada endpoint filtra y valida el acceso según la vessel activa del usuario o el token de guest.

---

## Permisos y Seguridad

- **IsAuthenticated**: Solo usuarios autenticados pueden acceder.
- **IsAdmin**: Solo admins pueden acceder o modificar ciertos recursos.
- **IsAuthenticatedOrGuestWithToken**: Permite acceso a usuarios autenticados o invitados con token válido.
- **Validaciones en serializadores**: Se valida que los recursos creados/consultados pertenezcan a la misma vessel que el usuario o guest.
- **No es posible acceder, editar ni eliminar recursos de otras embarcaciones.**
- **Todos los endpoints relevantes devuelven error 403 o 404 si se intenta acceder a recursos ajenos.**

---

## Casos de Uso Cubiertos

1. Un usuario solo puede ver y operar sobre embarcaciones donde tiene relación activa.
2. No es posible acceder, editar ni eliminar recursos de otras embarcaciones.
3. Los workers solo ven y operan sobre sus propias tareas.
4. Los admins pueden ver y gestionar todos los recursos de su vessel.
5. Los guests solo pueden interactuar con la vessel a la que están asociados.
6. No se puede asignar tareas a workers de otra vessel.
7. No se puede crear una relación duplicada entre usuario y vessel.
8. No se puede aprobar o revocar solicitudes de join a vessels ajenas.
9. No se puede acceder a rooms, mensajes o tareas de otra vessel, aunque se conozca el ID.
10. Todos los endpoints relevantes devuelven error 403 o 404 si se intenta acceder a recursos ajenos.

---

## Ejemplos de Código y Validaciones

- **Validación de acceso en vistas:**
  ```python
  if not UserVessel.objects.filter(user=request.user, vessel=vessel, status='active').exists():
      return Response({'error': 'Not allowed to access this vessel.'}, status=status.HTTP_403_FORBIDDEN)
  ```
- **Validación en serializador de tareas:**
  ```python
  if assigned.role != 'worker':
      raise serializers.ValidationError('Tasks can only be assigned to users with role worker.')
  if not UserVessel.objects.filter(user=assigned, status='active', vessel=creator_vessel).exists():
      raise serializers.ValidationError("Assigned user does not have an active vessel in this crew.")
  ```
- **Permiso para guests:**
  ```python
  class IsAuthenticatedOrGuestWithToken(permissions.BasePermission):
      def has_permission(self, request, view):
          if request.user and request.user.is_authenticated:
              return True
          guest_token = request.headers.get('Guest-Token')
          if guest_token:
              # Validar guest_token
              ...
              return True
          return False
  ```

---

## Notas adicionales
- Todos los modelos, serializadores y vistas están diseñados para evitar fugas de datos entre embarcaciones.
- El sistema es extensible y seguro para agregar nuevos recursos siempre que se sigan las mismas reglas de validación y permisos.
- Para producción, asegúrate de tener `DEBUG = False`, usar HTTPS y restringir los orígenes CORS.

---

**CrewCall Backend — Seguridad y privacidad por diseño.** 