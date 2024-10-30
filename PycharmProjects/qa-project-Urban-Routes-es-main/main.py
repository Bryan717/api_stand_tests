import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (By.ID, 'comfort-tariff')
    phone_field = (By.ID, 'phone')
    add_card_button = (By.ID, 'add-card')
    card_cvv_field = (By.ID, 'code')
    link_card_button = (By.ID, 'link')
    message_field = (By.ID, 'message')
    blanket_option = (By.ID, 'blanket')
    tissues_option = (By.ID, 'tissues')
    ice_cream_option = (By.ID, 'ice-cream')
    confirm_taxi_button = (By.ID, 'confirm-taxi')
    driver_info_modal = (By.ID, 'driver-info-modal')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def add_credit_card(self, cvv):
        self.driver.find_element(*self.add_card_button).click()
        cvv_field = self.driver.find_element(*self.card_cvv_field)
        cvv_field.send_keys(cvv)
        cvv_field.send_keys(Keys.TAB)  # Simula perder el enfoque del campo CVV
        self.driver.find_element(*self.link_card_button).click()

    def enter_message_to_driver(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_option).click()
        self.driver.find_element(*self.tissues_option).click()

    def order_ice_cream(self, quantity=2):
        ice_cream_option = self.driver.find_element(*self.ice_cream_option)
        for _ in range(quantity):
            ice_cream_option.click()

    def confirm_taxi_order(self):
        self.driver.find_element(*self.confirm_taxi_button).click()

    def wait_for_driver_info_modal(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.driver_info_modal))




class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # Rellenar el número de teléfono
        routes_page.enter_phone_number(data.phone_number)

        # Agregar una tarjeta de crédito
        routes_page.add_credit_card(data.card_cvv)
        confirmation_code = retrieve_phone_code(self.driver)
        routes_page.enter_phone_number(confirmation_code)

        # Escribir un mensaje para el conductor
        routes_page.enter_message_to_driver(data.driver_message)

        # Pedir una manta y pañuelos
        routes_page.request_blanket_and_tissues()

        # Pedir 2 helados
        routes_page.order_ice_cream()

        # Confirmar el pedido de taxi
        routes_page.confirm_taxi_order()

        # Esperar a que aparezca la información del conductor (opcional)
        routes_page.wait_for_driver_info_modal()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
