# Otro RPG más

El juego se basa en una plantilla base de un juego rpg, en este caso particular desarrollado en Python 3.7. El juego no tiene ningún objetivo en concreto, sino más bien se fundamenta con diferentes funcionalidades como explorar diferentes mapas, programar npc por medio de scripts, agregar objetos como pociones de salud o libros acumulables, y activar comportamientos dentro de cualquier personaje, ya sea NPC o jugador.
*Aun en progreso, version alpha aún no completada*

## Cómo utilizar

### Para poder correr el juego no hace falta más que:

Correr el archivo server.py. 
Correr el archivo client.py.

### Para crear y añadir un script debe seguir los siguiente pasos:

1. Diríjase a la carpeta /scripts/characters/.
1. Cree un archivo nuevo con el nombre del personaje que desea crear y con extensión .py.
1. Importe dentro del mismo script y cree una clase que herede del mismo.
	*Por temas de facilidad se recomienda también importar characterWrapper de game.scripts.CharacterWrapper y Vector2D de game.core.v2D*
	*Todas las posiciones y velocidades se manejan con esos vectores*
1. Cree un onInit y al character, por medio de la función character.onInit(), asígnele un nombre con el pasando de parámetro el nombre.
1. Cree un onUpdate y onMessage con base a la estructura de scripts.
1. Utilice las funciones facilitadas por el wrapper para controlar el npc.

  *Aún se trabaja en un esquema facilitado para la creación de mapas con diferentes posibilidades*

## Requerimientos

1. Python 3.7 o mayor, de 64 bits.
1. Pygame, versión >= 1.9.6.
1. Pyqueue, version >= 2.0.0.
1. Zmq, última versión

## Contacto
  * Carlos Arturo Cruz Useche
  * email: ccruzu@unal.edu.co
