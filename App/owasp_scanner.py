import zapv2
import time
import subprocess
import os


class OWASPScanner:
    def __init__(self, target):
        self.target = target
        zapApiKey = os.environ.get('API_KEY_ZAP')
        print(zapApiKey)
        self.zap = zapv2.ZAPv2(
            apikey=zapApiKey,
            proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    # This scan returns the list of all urls within the target
    def spider(self):
        self.zap.spider.scan(self.target)
        while int(self.zap.spider.status) < 100:
            print('Spider progress %: {}'.format(self.zap.spider.status))
            time.sleep(10)

        print('Spider complete')
        return self.zap.spider.results()

    # This scan returns the list of all alerts generated by the active scan
    def active_scan(self):
        self.zap.ascan.scan(self.target)
        while int(self.zap.ascan.status) < 100:
            print('Active Scan progress %: {}'.format(self.zap.ascan.status))
            time.sleep(10)

        print('Active Scan complete')
        return self.zap.core.alerts()

    # This scan returns the list of all open ports
    def port_scan(self):
        self.zap.portscan.scan(self.target, '0-65535')
        while int(self.zap.portscan.status) < 100:
            print('Port Scan progress %: {}'.format(self.zap.portscan.status))
            time.sleep(10)

        print('Port Scan complete')
        return self.zap.portscan.port_list(self.target)


class NiktoScanner:
    def __init__(self, target):
        self.target = target

    def ssl_scan(self):
        # Run Nikto scanner command and get output
        output = subprocess.check_output(
            ['nikto', '-h', self.target, '-ssl'])
        output = output.decode('utf-8')

        # Return the output
        return output

    def scan(self):
        # Run Nikto scanner command and get output
        output = subprocess.check_output(['nikto', '-h', self.target])
        output = output.decode('utf-8')

        # Return the output
        return output
