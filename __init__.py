# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path, mkdir
from os.path import expanduser
from datetime import date

import pyautogui

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
import pyclip


class JokerSkill(MycroftSkill):
    def __init__(self):
        self.screenshot_dir = expanduser("~/Pictures")
        if not path.exists(self.screenshot_dir):
            mkdir(self.screenshot_dir)
        super(JokerSkill, self).__init__(name="JokerSkill")

    def bad_boy(self):
        self.speak("I am shit myself, check my shit")

    @intent_handler(IntentBuilder("ScreenshotIntent").require("Screenshot"))
    def handle_screenshot(self):
        try:
            today = date.today().strftime("%d-%m-%Y_%H:%M:%S")
            filename = f"{today} JarvisScreen.png"
            filepath = f"{self.screenshot_dir}/{filename}"

            my_screenshot = pyautogui.screenshot()
            my_screenshot.save(filepath)
            # TODO: Better don't kill after CTRL+v EVERYTHING
            # pyclip.copy(open(filepath, 'rb').read())
            self.speak("Saved")
        except NotImplementedError as e:
            print(e)
            self.bad_boy()

    def stop(self):
        pass


def create_skill():
    return JokerSkill()
