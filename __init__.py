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


from os import path, makedirs
from os.path import expanduser
from datetime import date

import pyautogui

from adapt.intent import IntentBuilder
from mycroft.skills import skill_api_method
from mycroft.skills.core import MycroftSkill, intent_handler


class HelpersMixin:
    @staticmethod
    def create_if_not_exists(directory):
        """
        Create dir if not exist
        :param directory:
        :return:
        """
        if not path.isdir(directory):
            makedirs(directory)


class ErrorsMixin(MycroftSkill):
    def handle_error(self):
        self.speak("I am shit myself")


class CameraShootMixin(MycroftSkill):
    @skill_api_method
    def take_single_photo(self):
        """Take a single photo using the attached camera."""
        self.handle_camera_activity()

    def handle_camera_activity(self):
        """Perform camera action.

        Arguments:
            activity (str): the type of action to take, one of:
                "generic" - open the camera app
        """
        self.gui["save_path"] = self.save_folder
        self.gui["singleshot_mode"] = True
        self.gui.show_page("Camera.qml", override_idle=60)


class JokerSkill(MycroftSkill, HelpersMixin, CameraShootMixin):

    def __init__(self):
        self.screenshot_dir = expanduser("~/Pictures")
        self.videos_dir = expanduser("~/Videos")
        self.create_if_not_exists(self.screenshot_dir)
        self.create_if_not_exists(self.videos_dir)
        super(JokerSkill, self).__init__(name="JokerSkill")

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
            self.take_single_photo()  # Take a smile!
            self.speak("Shoot!")
        except NotImplementedError as e:
            print(e)
            self.handle_error()

    def stop(self):
        # self.handle_camera_completed()
        pass

def create_skill():
    return JokerSkill()
