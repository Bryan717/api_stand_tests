# Urban Routes Automation Testing

## Descripción del Proyecto
Este proyecto realiza pruebas automatizadas para la plataforma de taxis **Urban Routes**. Las pruebas verifican el flujo completo de solicitud de un taxi en la aplicación, incluyendo selección de tarifa, ingreso de información del usuario, solicitud de servicios adicionales y confirmación del pedido.

## Tecnologías y Técnicas Utilizadas
- **Lenguaje de Programación:** Python
- **Herramienta de Pruebas:** Pytest
- **Automatización de Navegador:** Selenium WebDriver

## Estructura del Proyecto
- **main.py**: Contiene las clases `UrbanRoutesPage` y `TestUrbanRoutes` con las pruebas definidas.
- **data.py**: Almacena datos de configuración y URL necesarios para las pruebas.
- **README.md**: Instrucciones del proyecto y de configuración de pruebas (este archivo).

## Cómo Ejecutar las Pruebas
1. **Requisitos previos:**
   - Instalar Python 3.x y pip.
   - Instalar ChromeDriver compatible con la versión de Google Chrome instalada.
   
2. **Instalar dependencias:**
   Ejecuta el siguiente comando para instalar Selenium y Pytest:
   ```bash
   pip install -r requirements.txt
