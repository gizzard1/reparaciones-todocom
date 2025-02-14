# Chatbot que atiende clientes para un negocio de reparación de laptops v0.0

Este proyecto es un prototipo inicial de chatbot, que atiende clientes de manera automática. La interfaz ofrece un ambiente amigable.
El algoritmo actúa sobre ramificaciones, cambiando el contexto dependiendo los patrones que se perciban por parte del input del usuario.

## Características

- **Interfaz intuitiva**: Diseñada para que los usuarios perciban una experiencia de chat habitual.
- **Algoritmo de búsqueda**: Que es alimentado de un archivo intents.json con casos reales y puede ser mejorable para entrenamiento.

## Tecnologías Utilizadas

- **Frontend y Backend**: Implementado con el framework Streamlit, usando lenguaje python
- **Unidecode**: Para reducir errores por acentos.
- **Random**: Produce una respuesta del arreglo que contiene para los diversos casos presentados.

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/gizzard1/reparaciones-todocom
cd reparaciones-todocom
```

### 2. Instalar dependencias

#### Streamlit
```cmd
pip install streamlit
```

#### Unidecode:
```cmd
pip install Unidecode
```

### 3. Configuración
- Alimenta al archivo intents.json para expandir el número de casos. Por razones de confidencialidad sólo mantendré algunos en este repositorio a modo de prueba y estudio.

### 4. Levanta la aplicación
Navega hasta el directorio de la aplicación y usa el comando:
```cmd
streamlit run .\main.py
```

## Aplicaciones Prácticas

- **Soporte IT**: Para atender casos especiales y cotidianos.
- **Asistente para generar citas**: Conectado a una aplicación integrada o desarrollando una base de datos.
- **Asistente que genera cotizaciones**: De manera automática y al instante.
