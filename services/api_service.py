import requests
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple

class ApiService:
    def __init__(self, power_bi_api_url: str, **connection_args):
        self.power_bi_api_url: str = power_bi_api_url
        self.headers: dict = None

        self.access_token = connection_args.pop('access_token', None)

        for key, value in connection_args.items():
            setattr(self, key, value)
    
    def get_endpoint(self, endpoint: str) -> List[Dict]:
        try:
            response = requests.get(
                self.power_bi_api_url + endpoint,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()['value']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get endpoint: {endpoint} - {e}")
    
    def get_headers(self) -> dict:
        try:
            return {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
        except Exception as e:
            raise Exception(f"Failed to get headers: {e}")

    def get_groups_admin(self, access_token: str) -> List[Tuple[str, str]]:
        endpoint_url = f'{self.power_bi_api_url}/v1.0/myorg/admin/groups?%24top=5000'
        try:
            data = self.get_endpoint(endpoint_url)
            new_record_list = [(record.get('capacityid'), record.get('id')) for record in data]
            return new_record_list
        except Exception as e:
            raise Exception(f"Failed to get groups: {e}")
        
    def get_activityevents_admin(self, access_token: str) -> List[Tuple[str, str]]:
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        curr_day = datetime.combine(date.today(), datetime.min.time())
        back30day = curr_day - timedelta(days=30)

        new_record_list = []
        while curr_day > back30day:
            startDateTime: str = curr_day.strftime(date_format)
            endDateTime: str = ((curr_day + timedelta(days=1)) - timedelta(seconds=1)).strftime(date_format)

            endpoint_url = f'{self.power_bi_api_url}/v1.0/myorg/admin/activityevents?%24filter=activityDateTime%20ge%20{startDateTime}%20and%20activityDateTime%20le%20{endDateTime}&%24top=5000'
            endpoint_url = endpoint_url.replace('000000Z', '000Z')

            while endpoint_url:
                try:
                    api_response = requests.get(endpoint_url, headers=self.headers)
                    api_response.raise_for_status()
                    data = api_response.json()['value']
                    new_record_list += [(record.get('activityDateTime'), record.get('activityType')) for record in data]

                    endpoint_url = api_response.json().get('@odata.nextLink')
                except requests.exceptions.RequestException as e:
                    raise Exception(f"Failed to get activity events: {e}")
                except KeyError as e:
                    raise Exception(f"Failed to parse activity events response: {e}")

            curr_day -= timedelta(days=1)

        return new_record_list
