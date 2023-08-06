from seleniumpm.webelements.clickable import Clickable


class Checkbox(Clickable):
    def __init__(self, driver, locator):
        super(Checkbox, self).__init__(driver, locator)

    def select(self):
        if not self.is_selected():
            self.get_webelement().click()

    def unselect(self):
        if self.is_selected():
            self.get_webelement().click()
