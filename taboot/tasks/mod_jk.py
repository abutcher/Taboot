# -*- coding: utf-8 -*-
# Taboot - Client utility for performing deployments with Func.
# Copyright © 2009-2011, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from taboot.tasks import BaseTask, FuncTask, TaskResult

JK_ENABLE = 0
JK_DISABLE = 1
JK_STOP = 2
JK_QUERY_STATE = 3
JK_QUERY_WAIT_STATE = 4

class ToggleHost(FuncTask):
    def __init__(self, action, proxyhost, **kwargs):
        super(ToggleHost, self).__init__(proxyhost, **kwargs)
        self._action = action
        if action == JK_ENABLE:
            self._command = 'taboot.modjk.enable_host'
        elif action == JK_DISABLE:
            self._command = 'taboot.modjk.disable_host'
        elif action == JK_STOP:
            self._command = 'taboot.modjk.stop_host'
        else:
            raise Exception("Undefined toggle action")

    def _process_result(self, result):
        t = TaskResult(self)
        if len(result) > 0:
            t.success = True
            if self._action == JK_ENABLE:
                verb = 'Enabled'
            elif self._action == JK_DISABLE:
                verb = 'Disabled'
            elif self._action == JK_STOP:
                verb = 'Stopped'

            t.output = "%s AJP on the following balancer/worker " \
                "pairs:\n" % verb
            for balancer, worker in result:
                t.output += "%s:  %s\n" % (balancer, worker)
        else:
            t.success = False
            t.output = "Failed to find worker host"
        return t

class JKBaseTask(BaseTask):
    def __init__(self, proxies, action, **kwargs):
        super(JKBaseTask, self).__init__(**kwargs)
        from sys import modules
        self.proxies = proxies
        self.jkaction = getattr(modules[self.__module__], "JK_%s" %
                                action.upper())

    def run(self, runner):
        output = ""
        success = True
        for proxy in self.proxies:
            toggler = ToggleHost(self.jkaction, self._host, host=proxy)
            result = toggler.run(runner)
            output += "%s:\n" % proxy
            output += "%s\n" % result.output
            if result.success == False:
                success = False
                break
        return TaskResult(self, success=success, output=output)

class QueryHost(FuncTask):
    def __init__(self, query, proxyhost, **kwargs):
        super(QueryHost, self).__init__(proxyhost, **kwargs)
        self._query = query
        if query == JK_QUERY_STATE:
            self._command = 'taboot.modjk.query_host_state'
        elif query == JK_QUERY_WAIT_STATE:
            self._command = 'taboot.modjk.query_host_wait_state_ok'
        else:
            raise Exception("Undefined toggle action")

    def _process_result(self, result):
        t = TaskResult(self)
        if len(result) > 0:
            t.success = True
            if self._query == JK_QUERY_STATE:
                noun = 'state'
            if self._query == JK_QUERY_STATE:
                noun = 'state'

            t.output = "Queried %s AJP on the following balancer/worker " \
                "pairs:\n" % noun
            for balancer, worker, state in result:
                t.output += "%s:  %s  %s\n" % (balancer, worker, state)
        else:
            t.success = False
            t.output = "Failed to find worker host"
        return t

class JKQueryBaseTask(BaseTask):
    def __init__(self, proxies, query, **kwargs):
        super(JKQueryBaseTask, self).__init__(**kwargs)
        from sys import modules
        self.proxies = proxies
        self.jkaction = getattr(modules[self.__module__], "JK_QUERY_%s" %
                                query.upper())

    def run(self, runner):
        output = ""
        success = True
        for proxy in self.proxies:
            queryer = QueryHost(self.jkaction, self._host, host=proxy)
            result = queryer.run(runner)
            output += "%s:\n" % proxy
            output += "%s\n" % result.output
            if result.success == False:
                success = False
                break
        return TaskResult(self, success=success, output=output)

class OutOfRotation(JKBaseTask):
    """
    Remove an AJP node from rotation on a proxy via modjkapi access on
    the proxy with func.

    :Parameters:
      - `proxies`: A list of URLs to AJP jkmanage interfaces
    """
    def __init__(self, proxies, action="stop", **kwargs):
        super(OutOfRotation, self).__init__(proxies, action, **kwargs)

class InRotation(JKBaseTask):
    """
    Put an AJP node in rotation on a proxy via modjkapi access on
    the proxy with func.

    :Parameters:
      - `proxies`: A list of URLs to AJP jkmanage interfaces
    """
    def __init__(self, proxies, action="enable", **kwargs):
        super(InRotation, self).__init__(proxies, action, **kwargs)

class QueryState(JKQueryBaseTask):
    """
    Query the state of an AJP node on a proxy via modjkapi access on
    the proxy with func.

    :Parameters:
      - `proxies`: A list of URLs to AJP jkmanage interfaces
    """
    def __init__(self, proxies, query="state", **kwargs):
        super(QueryState, self).__init__(proxies, query, **kwargs)

def WaitOnStateOK(JKQueryBaseTask):
    """
    Wait until all workers associated with the AJP node on a proxy
    have a state of OK through use of modjkapi on the proxy node with
    func.

    :Parameters:
      - `proxies`: A list of URLs to AJP jkmanage interfaces
    """
    def _init__(self, proxies, query="wait_state", **kwargs):
        super(WaitOnStateOK, self).__init__(proxies, query, **kwargs)
