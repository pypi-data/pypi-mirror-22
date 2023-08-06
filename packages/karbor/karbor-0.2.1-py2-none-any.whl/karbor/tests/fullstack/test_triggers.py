# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from karbor.tests.fullstack import karbor_base
from karbor.tests.fullstack import karbor_objects as objects


class TriggersTest(karbor_base.KarborBaseTest):
    """Test Triggers operation"""

    def test_triggers_list(self):
        trigger1 = self.store(objects.Trigger())
        trigger1.create('time', {'pattern': '0 20 * * 2', 'format': 'crontab'})
        trigger2 = self.store(objects.Trigger())
        trigger2.create('time', {'pattern': '0 10 * * *', 'format': 'crontab'})

        items = self.karbor_client.triggers.list()
        ids = [item.id for item in items]
        self.assertTrue(trigger1.id in ids)
        self.assertTrue(trigger2.id in ids)

    def test_triggers_get(self):
        trigger_name = "FullStack Trigger Test Get"
        trigger = self.store(objects.Trigger())
        trigger.create('time', {'pattern': '0 15 * * 2', 'format': 'crontab'},
                       name=trigger_name)
        trigger = self.karbor_client.triggers.get(trigger.id)
        self.assertEqual(trigger_name, trigger.name)

    def test_triggers_delete(self):
        trigger = objects.Trigger()
        trigger.create('time', {'pattern': '0 12 * * 2', 'format': 'crontab'})
        self.karbor_client.triggers.delete(trigger.id)
        items = self.karbor_client.triggers.list()
        ids = [item.id for item in items]
        self.assertTrue(trigger.id not in ids)
