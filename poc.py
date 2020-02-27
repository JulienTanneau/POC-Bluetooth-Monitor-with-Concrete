import bluetooth
import requests
import time


class BluetoothMonitor:

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token

    def get_known_devices(self):
        known_devices = requests.get(
            self.api_url,
            headers={"Authorization": "token {}".format(self.token)}
        ).json().get("results", [])
        return known_devices

    def nearby_devices(self, search_time=15):
        return bluetooth.discover_devices(duration=search_time)

    def set_activity(self, device, active=False):
        requests.patch(
            url=device['url'],
            data={"active": active},
            headers={"Authorization": "token {}".format(self.token)}
        )

    def update_who_is_here(self, known_devices):
        nearby_devices = self.nearby_devices()
        for d in known_devices:
            if d['mac_address'] in nearby_devices:
                self.set_activity(d, True)
            else:
                self.set_activity(d, False)

    def run(self, sleep_time=60):
        while True:
            try:
                self.update_who_is_here(self.get_known_devices())
            except Exception:
                pass
            time.sleep(sleep_time)


if __name__ == '__main__':
    url = ''
    token = ''
    monitor = BluetoothMonitor(api_url=url, token=token)
    monitor.run(sleep_time=30)
