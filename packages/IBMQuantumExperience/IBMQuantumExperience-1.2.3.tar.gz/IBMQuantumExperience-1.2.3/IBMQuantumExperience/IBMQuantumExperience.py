import requests
import time
import datetime
import json

config_base = {
    'url': 'https://quantumexperience.ng.bluemix.net/api'
}


class _Credentials:
    def __init__(self, token, config=None):
        self.token_unique = token
        if config and config.get('url', None):
            self.config = config
        else:
            self.config = config_base

        self.data_credentials = {}
        self.obtain_token()

    def obtain_token(self):
        self.data_credentials = requests.post(self.config.get('url') + "/users/loginWithToken",
                                              data={'apiToken': self.token_unique}).json()

        if not self.get_token():
            print('ERROR: Not token valid')

    def get_token(self):
        return self.data_credentials.get('id', None)

    def get_user_id(self):
        return self.data_credentials.get('userId', None)

    def get_config(self):
        return self.config


class _Request:
    def __init__(self, token, config=None):
        self.credential = _Credentials(token, config)

    def check_token(self, respond):
        if respond.status_code == 401:
            self.credential.obtain_token()
            return False
        return True

    def post(self, path, params='', data=None):
        if data is None:
            data = {}
        headers = {'Content-Type': 'application/json'}
        respond = requests.post(
            self.credential.config['url'] + path + '?access_token=' + str(self.credential.get_token()) + params,
            data=data,
            headers=headers)
        if not self.check_token(respond):
            respond = requests.post(
                self.credential.config['url'] + path + '?access_token=' + str(self.credential.get_token()) + params,
                data=data, headers=headers)
        return respond.json()

    def get(self, path, params='', withToken=True):
        if (withToken):
            access_token = self.credential.get_token()
            if access_token:
                access_token = '?access_token=' + str(access_token)
            else:
                access_token = ''
        else:
            access_token = ''

        respond = requests.get(
            self.credential.config['url'] + path + access_token + params)
        if not self.check_token(respond):
            respond = requests.get(
                self.credential.config['url'] + path + access_token + params)
        return respond.json()


class IBMQuantumExperience:
    def __init__(self, token, config=None):
        self.req = _Request(token, config)

    def _check_credentials(self):
        if not self.req.credential.get_token():
            return False
        return True

    def get_execution(self, id_execution):
        if not self._check_credentials():
            return None
        execution = self.req.get('/Executions/' + id_execution, '')
        if execution["codeId"]:
            execution['code'] = self.get_code(execution["codeId"])
        return execution

    def get_result_from_execution(self, id_execution):
        if not self._check_credentials():
            return None
        execution = self.req.get('/Executions/' + id_execution, '')
        result = {}
        if 'result' in execution:
            if execution["result"]["data"].get('p', None):
                result["measure"] = execution["result"]["data"]["p"]
            if execution["result"]["data"].get('valsxyz', None):
                result["bloch"] = execution["result"]["data"]["valsxyz"]

        return result

    def get_code(self, id_code):
        if not self._check_credentials():
            return None
        code = self.req.get('/Codes/' + id_code, '')
        executions = self.req.get('/Codes/' + id_code + '/executions', 'filter={"limit":3}')
        if isinstance(executions, list):
            code["executions"] = executions
        return code

    def get_image_code(self, id_code):
        if not self._check_credentials():
            return None
        return self.req.get('/Codes/' + id_code + '/export/png/url', '')

    def get_last_codes(self):
        if not self._check_credentials():
            return None
        return self.req.get('/users/' +
                            str(self.req.credential.get_user_id()) +
                            '/codes/lastest', '&includeExecutions=true')['codes']

    def run_experiment(self, qasm, device='simulator', shots=1, name=None, timeout=60):
        if not self._check_credentials():
            return None
        data = {}
        qasm = qasm.replace('IBMQASM 2.0;', '')
        qasm = qasm.replace('OPENQASM 2.0;', '')
        data['qasm'] = qasm
        data['codeType'] = 'QASM2'
        if name is None:
            name = 'Experiment #' + datetime.date.today().strftime("%Y%m%d%H%M%S")
        data['name'] = name

        if device == 'qx5qv2':
            device_type = 'real'
        elif device == 'simulator':
            device_type = 'sim_trivial_2'
        else:
            respond = {}
            respond["error"] = "Device " + device + " not exits in Quantum Experience. Only allow qx5qv2 or simulator"
            return respond

        execution = self.req.post('/codes/execute', '&shots=' + str(shots) + '&deviceRunType=' + device_type,
                                  json.dumps(data))
        respond = {}
        # noinspection PyBroadException
        try:
            status = execution["status"]["id"]
            id_execution = execution["id"]
            result = {}
            respond["status"] = status
            respond["idExecution"] = id_execution
            respond["idCode"] = execution["codeId"]
            if status == "DONE":
                if execution["result"]:
                    if execution["result"]["data"].get('p', None):
                        result["measure"] = execution["result"]["data"]["p"]
                    if execution["result"]["data"].get('valsxyz', None):
                        result["bloch"] = execution["result"]["data"]["valsxyz"]
                    respond["result"] = result
                    return respond
            elif status == "ERROR":
                return respond
            else:
                if timeout:
                    if timeout > 300:
                        timeout = 300
                    for i in range(1, timeout):
                        print("Waiting for results...")
                        result = self.get_result_from_execution(id_execution)
                        if len(result) > 0:
                            respond["status"] = 'DONE'
                            respond["result"] = result
                            return respond
                        else:
                            time.sleep(2)
                    return respond
                else:
                    return respond
        except Exception:
            respond["error"] = execution
            return respond

    def run_job(self, qasms, device='simulator', shots=1, max_credits=3):
        if not self._check_credentials():
            return None
        data = {}
        for qasm in qasms:
            qasm['qasm'] = qasm['qasm'].replace('IBMQASM 2.0;', '')
            qasm['qasm'] = qasm['qasm'].replace('OPENQASM 2.0;', '')
        data['qasms'] = qasms
        data['shots'] = shots
        data['maxCredits'] = max_credits
        data['backend'] = {}
        if device == 'qx5qv2':
            data['backend']['name'] = 'real'
        elif device == 'simulator':
            data['backend']['name'] = 'simulator'
        else:
            respond = {}
            respond["error"] = "Device " + device + " not exits in Quantum Experience. Only allow qx5qv2 or simulator"
            return respond

        job = self.req.post('/Jobs', data=json.dumps(data))
        return job

    def get_job(self, id_job):
        if not self._check_credentials() or not id_job:
            return None
        job = self.req.get('/Jobs/' + id_job)
        return job

    def device_status(self, device='qx5qv2'):
        # TODO: Change the 5Q chip name
        if device == 'qx5qv2':
            device = 'chip_real'
        status = self.req.get('/Status/queue?device=' + device, withToken=False)["state"]
        ret = {}
        ret['available'] = False
        if status:
            ret['available'] = True
        return ret
