import sys
import random
import time

import websockets
import asyncio
import json
import string

from webactions_lm.parser.widget import Screen

class WebUIHeiHei:
    def _run_async(_f):
        def wrapper(*args, **kwargs):
            return asyncio.get_event_loop().run_until_complete(_f(*args, **kwargs))
        return wrapper

    async def _send_and_wait_for_response(self, _cmd, _reqid, _debug=False):
        if _debug:
            print(_cmd)
        await self.ws.send(_cmd)

        while True:
            response = await self.ws.recv()
            data = json.loads(response)
            if _debug:
                print(data)
            payload = data['payload']
            if _reqid != payload.get('reqid', None):
                continue
            return payload
        return None

    def __init__(self):
        self.url = None
        self.automatedTabId = None
        self.chatdeskTabId = None
        self.chatdeskUrl = None
        self.issue_id = None
        self.lastUi = None

    @_run_async
    async def init(self, _server=None):
        url = 'ws://localhost:8125/ts'
        conn = websockets.connect(url, max_size=2**30)
        self.ws = await conn

    @_run_async
    async def go_to_page(self, _url):
        self.url = _url
        reqid = ''.join(random.choices(string.ascii_lowercase, k=10))
        cmd = f'{{"action":"createTab","url":"{_url}", "reqid":"{reqid}", "background":false}}'
        
        response = await self._send_and_wait_for_response(cmd, reqid)
        if False == response['succeeded']:
            return False
        self.automatedTabId = response['tabId']
        
        while True:
            response = await self.ws.recv()
            data = json.loads(response)
            if 'load' == data.get('payload', {}).get('event_type', None):
                time.sleep(1)
                break
        
        return True

    @_run_async
    async def close(self):
        reqid = ''.join(random.choices(string.ascii_lowercase, k=10))
        cmd = f'{{"action":"removeTab","tabId":{self.automatedTabId}, "reqid":"{reqid}"}}'
        response = await self._send_and_wait_for_response(cmd, reqid)
        return response['succeeded']

    @_run_async
    async def observe(self, _tabId, _compress=True):
        reqid = ''.join(random.choices(string.ascii_lowercase, k=10))
        cmd = f'{{"action":"watch", "tabId":{_tabId}, "reqid":"{reqid}"}}'
        response = await self._send_and_wait_for_response(cmd, reqid)

        assert response['succeeded']

        content = response
        if ('htree' not in content) and ('content' in content):
            content = content['content']
        if 'htree' in content:
            self.lastUi = Screen(content['htree'])
            return self.lastUi
        return None

    @_run_async
    async def click(self, _id):
        print(f'-- click ({_id})')
        if self.lastUi is None:
            return
        widget = self.lastUi.find_by_id(int(_id))

        reqid = ''.join(random.choices(string.ascii_lowercase, k=10))
        cmd = f'{{"action":"click", "tabId":{self.automatedTabId}, "reqid":"{reqid}", ' +\
            f'"xpath":"{widget.xpath}", "buttonClicked":0}}'
        response = await self._send_and_wait_for_response(cmd, reqid)
        return response['succeeded']

    @_run_async
    async def _type(self, _id, _text, _enter=False):
        if self.lastUi is None:
            return
        widget = self.lastUi.find_by_id(int(_id))

        reqid = ''.join(random.choices(string.ascii_lowercase, k=10))
        cmd = f'{{"action":"text", "tabId":{self.automatedTabId}, "reqid":"{reqid}", ' +\
            f'"xpath":"{widget.xpath}", "text":"{_text}", "simulateKeystrokes":true}}'
        response = await self._send_and_wait_for_response(cmd, reqid, True)
        if False == response['succeeded']:
            return False
        if _enter:
            cmd = f'{{"action":"key", "tabId":{self.automatedTabId}, "reqid":"{reqid}", ' +\
                f'"xpath":"{widget.xpath}", "key":"Enter"}}'
            response = await self._send_and_wait_for_response(cmd, reqid, True)
       
        return response['succeeded']

    @_run_async
    async def clear(self, _id):
        pass

    def type(self, _id, _text):
        if False == self.click(_id):
            return False
        # time.sleep (0.5)
        return self._type(_id, _text)

    def parse_page(self):
        ui = self.observe(self.automatedTabId)
        return ui.parseForLLM()

    def find_widget_by_val(self, _val, _type=None):
        for id, widget in self.lastUi.internalId2Widget.items():
            if (widget.value != _val):
                continue
            if (_type is not None):
                if ("type" not in widget.attributes):
                    continue
                if (widget.attributes['type'] != _type):
                    continue
            return widget

        return None

    def get_widget_vals_list(self):
        widget_vals = []
        for id, widget in self.lastUi.internalId2Widget.items():
            if (widget.value != ''):
                widget_vals.append(widget.value)
        return widget_vals
    
    @_run_async
    async def get_active_tab(self):
        await self.ws.send(f'{{"action":"listTabs"}}')
        response = await self.ws.recv()
        data = json.loads(response)

        for window in data['payload']:
            if not window['focused']:
                continue
            for tab in window['tabs']:
                if tab['active']:
                    return (tab['id'], tab['url'])
        return (None, None)

    @_run_async
    async def get_tab_from_url(self, url):
        await self.ws.send(f'{{"action":"listTabs"}}')
        response = await self.ws.recv()
        data = json.loads(response)

        for window in data['payload']:
            for tab in window['tabs']:
                if url in tab['url']:
                    return (tab['id'], tab['url'])
        return (None, None)

    def get_issue_id(self):
        self.chatdeskTabId, self.chatdeskUrl = self.get_active_tab()
        if self.chatdeskTabId is None:
            return None

        ui = self.observe(self.chatdeskTabId, False)

        issue_id_label_candidates = ui.find_by_value('External ID:')
        # print (issue_id_label_candidates)
        if 1 != len(issue_id_label_candidates):
            print(
                f"[ERROR] Multiple 'External ID' labels found? {issue_id_label_candidates}")
            return None

        issue_id_label = issue_id_label_candidates[0]
        issue_id_text = issue_id_label.parent.get_text()
        # print (issue_id_text)
        issue_id_candidates = [
            t for t in issue_id_text if t not in ['', 'External ID:']]
        if 1 != len(issue_id_candidates):
            print(
                f'[ERROR] Multiple possible issue id texts? {issue_id_candidates}')
            return None

        self.issue_id = issue_id_candidates[0]
        # print (self.issue_id)
        return self.issue_id