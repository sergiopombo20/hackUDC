Application integrated with Denodo AI SDK, documentation at  
[Denodo AI SDK - User Manual](https://community.denodo.com/docs/html/document/denodoconnects/latest/en/Denodo%20AI%20SDK%20-%20User%20Manual).

Hemos creado una base de datos de ejemplo en formato CSV, basándonos en los departamentos de la página web  
[https://careers.gradiant.org/jobs](https://careers.gradiant.org/jobs) en la sección "Áreas", creando personas ficticias con conocimientos en ciertas áreas de la tecnología.  
También hemos probado con modelos posgreSQL y mongoDB, pero denodo parece no clasificar bien las relaciones por el momento.


Después, hemos cargado el CSV en el Denodo AI SDK. Este kit simplifica la preparación de datos al combinar el acceso, la transformación y la seguridad en una única interfaz, agilizando el ciclo de desarrollo de aplicaciones de IA.  

Desde Denodo, podemos hacer peticiones a un LLM que responde a las preguntas según el contexto. Usando ChatGPT-4o como modelo, hemos conseguido compilar un modelo que responde preguntas sobre el conocimiento que tienen ciertas personas en ciertos departamentos sobre algunos frameworks.
Además, hemos implementado un frontal en telegram que permite subir CSVs y permite hacer preguntas del contexto del dataset.

querys de ejemplo: 

/query Dime quien tiene conocimientos de Java
/query Cual es la libreria más conocida entre los empleados de gradient
/query dime el correo de alguien que tenga conocimiento de Dark Web

