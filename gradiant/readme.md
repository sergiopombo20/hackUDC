# Application integrated with Denodo AI SDK

Documentation at [Denodo AI SDK - User Manual](#).

## Creación de la base de datos de ejemplo

Hemos creado una base de datos de ejemplo en formato CSV, basándonos en los departamentos de la página web  
[Gradiant Careers - Áreas](https://careers.gradiant.org/jobs)  
Generamos personas ficticias con conocimientos en ciertas áreas de la tecnología.  

También hemos probado con modelos **PostgreSQL** y **MongoDB**, pero **Denodo** parece no clasificar bien las relaciones por el momento.

## Carga en Denodo AI SDK

Después, hemos cargado el CSV en el **Denodo AI SDK**. Este kit simplifica la preparación de datos al combinar el acceso, la transformación y la seguridad en una única interfaz, agilizando el ciclo de desarrollo de aplicaciones de IA.

Desde **Denodo**, podemos hacer peticiones a un **LLM** que responde a las preguntas según el contexto.  
Usando **ChatGPT-4o** como modelo, hemos conseguido compilar un modelo que responde preguntas sobre el conocimiento que tienen ciertas personas en ciertos departamentos sobre algunos frameworks.

## Implementación de un frontal en Telegram

Hemos implementado un **frontal en Telegram** que permite:
- Subir **CSVs**  
- Hacer preguntas sobre el contexto del dataset  

## Consultas de ejemplo

```plaintext
/query Dime quien tiene conocimientos de Java  
/query Cual es la libreria más conocida entre los empleados de Gradiant  
/query dime el correo de alguien que tenga conocimiento de Dark Web  
