import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from django.conf import settings
from django.core.cache import cache  


logger = logging.getLogger(__name__)

class IikoService:
    def __init__(self):
        self.base_url = "https://api-ru.iiko.services/api/1"
        self.api_login = settings.IIKO_API_LOGIN
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def ensure_token_in_redis(self) -> str:
        token_key = getattr(settings, 'IIKO_TOKEN_CACHE_KEY', 'iiko_token')
        token_timeout = getattr(settings, 'IIKO_TOKEN_CACHE_TIMEOUT', 3600)
        token_in_redis = cache.get(token_key)

        if token_in_redis:
            print(f"Токен уже существует в Redis: {token_in_redis}")
        else:
            print("Токен в Redis не найден. Генерируем новый токен при открытии main.html...")
            token_in_redis = self._get_new_token()
            cache.set(token_key, token_in_redis, token_timeout)
            print(f"Сгенерирован и сохранён новый IIKO Token: {token_in_redis}")

        return token_in_redis

    def get_token_and_order_by_table(self, organization_id: str, table_uuid: str) -> Dict[str, Any]:
        if not organization_id or not table_uuid:
            raise ValueError("organization_id и table_uuid обязательны для получения заказа")

        token_key = getattr(settings, 'IIKO_TOKEN_CACHE_KEY', 'iiko_token')
        token_timeout = getattr(settings, 'IIKO_TOKEN_CACHE_TIMEOUT', 3600)
        token_in_redis = cache.get(token_key)

        if token_in_redis:
            print(f"Токен найден в Redis: {token_in_redis}")
        else:
            print("Токен в Redis отсутствует, генерируем новый перед запросом заказа...")
            token_in_redis = self._get_new_token()
            cache.set(token_key, token_in_redis, token_timeout)

        try:
            headers = {"Authorization": f"Bearer {token_in_redis}"}
            url = f"{self.base_url}/order/by_table"
            payload = {
                "organizationIds": [organization_id],
                "tableIds": [table_uuid]
            }
            print("Пробуем запросить текущий счёт (by_table) с токеном из Redis...")
            response = self._session.post(url, json=payload, headers=headers, timeout=15)

            if response.status_code == 401:
                logger.warning("Получен 401. Пробуем обновить токен и повторить запрос.")
                token_in_redis = self._get_new_token()
                cache.set(token_key, token_in_redis, token_timeout)
                print(f"Обновлённый токен: {token_in_redis}")
                headers["Authorization"] = f"Bearer {token_in_redis}"
                response = self._session.post(url, json=payload, headers=headers, timeout=15)
                if response.status_code == 401:
                    logger.error("Получен 401 после обновления токена. Ошибка авторизации.")
                    raise ValueError("Ошибка авторизации")

            response.raise_for_status()
            order_data = response.json()
            print("Запрос текущего счёта (by_table) выполнен успешно.")
            return order_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе текущего счёта в iiko: {e}")
            if getattr(e, 'response', None):
                logger.error(f"Ответ сервера: {e.response.text}")
            raise

    def _get_new_token(self) -> str:
        try:
            response = self._session.post(
                f"{self.base_url}/access_token",
                json={"apiLogin": self.api_login},
                timeout=getattr(settings, 'IIKO_API_TIMEOUT', 15)
            )
            response.raise_for_status()
            data = response.json()
            token = data.get('token')
            if not token:
                logger.error(f"Нет поля 'token' в ответе от iiko: {data}")
                raise ValueError("Отсутствует токен в ответе iiko")

            print(f"Новый IIKO Token: {token}")
            return token

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении токена iiko: {e}")
            if getattr(e, 'response', None):
                logger.error(f"Ответ сервера: {e.response.text}")
            raise
    
    def call_waiter(self, department_id, table_number, waiter_id=None):
        url = f"{self.base_url}/notifications/waiter-call"
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
            
        payload = {
                "userId": waiter_id or settings.IIKO_DEFAULT_WAITER_ID,
                "departmentId": department_id,
                "table": table_number
        }

        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
                raise Exception(f"Ошибка вызова официанта: {str(e)}")
        
    def get_waiter_info(self, organization_id: str, table_uuid: str) -> dict:

        if not organization_id or not table_uuid:
            raise ValueError("organization_id и table_uuid обязательны")

        try:
            token = self.ensure_token_in_redis()
            headers = {"Authorization": f"Bearer {token}"}
            
            url = f"{self.base_url}/employees/info"
            payload = {
                "organizationId": organization_id,
                "tableId": table_uuid
            }

            response = self._session.post(
                url,
                json=payload,
                headers=headers,
                timeout=getattr(settings, 'IIKO_API_TIMEOUT', 15)
            )

            if response.status_code == 401:
                token = self._get_new_token()
                headers["Authorization"] = f"Bearer {token}"
                response = self._session.post(url, json=payload, headers=headers)
                response.raise_for_status()

            data = response.json()
            
            return {
                'name': data.get('name', 'Неизвестный официант'),
                'photo': data.get('photoUrl'),
                'position': data.get('position', 'Официант'),
                'id': data.get('id')
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении информации об официанте: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Ответ сервера: {e.response.text}")
            raise Exception("Не удалось получить информацию об официанте")
        


logger = logging.getLogger(__name__)

class IikoWaiterService:
    def __init__(self):
        self.base_url = settings.IIKO_WAITER_API_URL
        self.api_key = settings.IIKO_WAITER_API_KEY
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        })

    def _make_request(self, endpoint: str, payload: dict) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/notifications/mobile/{endpoint}"
            response = self._session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при вызове {endpoint}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Ответ сервера: {e.response.text}")
            raise Exception(f"Ошибка при вызове {endpoint}")

    def call_waiter(self, 
                   department_id: str,
                   table_number: str,
                   user_id: Optional[str] = None,
                   comment: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "departmentId": department_id,
            "table": table_number,
            "userId": user_id or settings.IIKO_DEFAULT_WAITER_ID,
            "comment": comment
        }
        return self._make_request("waiter-call", payload)

    def request_cash_payment(self, 
                           order_id: str,
                           table_number: str,
                           user_id: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "orderId": order_id,
            "table": table_number,
            "userId": user_id or settings.IIKO_DEFAULT_WAITER_ID
        }
        return self._make_request("waiter-call/cash-payment", payload)

    def request_card_payment(self, 
                           order_id: str,
                           table_number: str,
                           user_id: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "orderId": order_id,
            "table": table_number,
            "userId": user_id or settings.IIKO_DEFAULT_WAITER_ID
        }
        return self._make_request("waiter-call/card-payment", payload)
        

    def notify_order_paid(self, 
                         order_id: str,
                         payment_type: str,
                         amount: float) -> Dict[str, Any]:
        payload = {
            "orderId": order_id,
            "paymentType": payment_type,
            "amount": amount
            
        }
        return self._make_request("order-paid", payload)

    def notify_new_order(self, 
                        order_id: str,
                        table_number: str,
                        items: list,
                        user_id: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "orderId": order_id,
            "table": table_number,
            "userId": user_id or settings.IIKO_DEFAULT_WAITER_ID,
        }

        return self._make_request("new-order", payload)

    def broadcast_new_order(self, 
                          order_id: str,
                          table_number: str) -> Dict[str, Any]:
        payload = {
            "orderId": order_id,
            "table": table_number,
        }
        return self._make_request("new-order-broadcast", payload)