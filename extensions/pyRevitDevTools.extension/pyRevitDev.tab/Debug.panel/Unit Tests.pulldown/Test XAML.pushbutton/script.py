"""Test loading XAML in IronPython."""
#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens
import urllib2
import json

from pyrevit import framework
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script


logger = script.get_logger()
output = script.get_output()


class NestedObject(forms.Reactive):
    def __init__(self, text):
        self._text = text

    @forms.reactive
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value


class ButtonData(forms.Reactive):
    def __init__(self, title, nested):
        self._title = title
        self.nested = nested

    @forms.reactive
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value


class EmployeeInfo(forms.Reactive):
    def __init__(self, name, job, supports):
        self._name = name
        self.job = job
        self.supports = supports

    @forms.reactive
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class ServerStatus(forms.Reactive):
    def __init__(self):
        self._status = False

    @forms.reactive
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


# code-behind for the window
class UI(forms.WPFWindow):
    def __init__(self):
        self.nested_data = NestedObject(text="<nested text>")
        self.data = \
            ButtonData(
                title="<bound title>",
                nested=self.nested_data
                )
        self.status = ServerStatus()

    def setup(self):
        self.textbox.DataContext = self.nested_data
        self.empinfo.DataContext = [
            EmployeeInfo(
                name="Ehsan",
                job="Architect",
                supports=[
                    "UX",
                    "CLI",
                    "Core"
                ]),
            EmployeeInfo(
                name="Gui",
                job="Programmer",
                supports=[
                    "CLI",
                ]),
            EmployeeInfo(
                name="Alex",
                job="Designer",
                supports=[
                    "Core"
                ]),
        ]
        self.textblock.DataContext = self.data
        self.button.DataContext = self.data
        self.statuslight.DataContext = self.status

    def set_status(self, status):
        print(status)
        self.status.status = status is not None

    def check_status(self):
        status_uri = r'https://status.epicgames.com/api/v2/status.json'
        status = json.loads(urllib2.urlopen(status_uri).read())
        self.dispatch(self.set_status, status)

    def check_fortnite_status(self, sender, args):
        self.dispatch(self.check_status)

    def update_text(self, sender, args):
        pass

    def button_click(self, sender, args):
        self.data.title = "<updated bound title>"
        self.nested_data.text = "<updated nested text>"

    def read_data(self, sender, args):
        forms.alert(self.nested_data.text)


# init ui
ui = script.load_ui(UI(), 'ui.xaml')
# show modal or nonmodal
ui.show_dialog()