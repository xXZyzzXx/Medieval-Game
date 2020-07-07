import gui_advanced as ga
import themes


class BarracksButton(ga.AdvancedButton):
    def __init__(self, dialoguebox_list, dialog, x=0, y=0, width=225, height=200, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_barracks)
        self.dialoguebox_list = dialoguebox_list
        self.dialog = dialog
        self.current_place = None
        # ====
        self.name = 'Казармы'
        self.image_icon = r"/images/barracks.png"
        self.building_type = 'Военные'
        self.technologies_for_unlock = ['Военное дело']
        self.time_building = 100
        self.cost_wood = 20
        self.cost_food = 30
        self.cost_iron = 400
        self.cost_clay = 50
        self.b_lvl = 1

    def on_press(self):
        if not self.dialoguebox_list[0].active and not self.dialoguebox_list[1].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox_list[2].current_place = self.current_place
            self.dialog.delete_dialoguebox_content()
            self.dialoguebox_list[0].create_house_content(self.name, self.image_icon, self.time_building,
                                                          self.cost_wood, self.cost_food,
                                                          self.cost_iron, self.cost_clay, self.b_lvl)
            self.dialoguebox_list[0].active = True

    def update(self):
        pass


class HouseButton(ga.AdvancedButton):
    def __init__(self, dialoguebox_list, dialog, x=0, y=0, width=225, height=200, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_house)
        self.dialoguebox_list = dialoguebox_list
        self.dialog = dialog
        self.current_place = None
        # ====
        self.name = 'Хижина'
        self.image_icon = r"/images/house.png"
        self.building_type = 'Социальные'
        self.technologies_for_unlock = [None]
        self.time_building = 100
        self.cost_wood = 60
        self.cost_food = 0
        self.cost_iron = 40
        self.cost_clay = 5
        self.b_lvl = 1

    def on_press(self):
        if not self.dialoguebox_list[0].active and not self.dialoguebox_list[1].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox_list[2].current_place = self.current_place
            self.dialog.delete_dialoguebox_content()
            self.dialoguebox_list[0].create_house_content(self.name, self.image_icon, self.time_building,
                                                          self.cost_wood, self.cost_food,
                                                          self.cost_iron, self.cost_clay, self.b_lvl)
            self.dialoguebox_list[0].active = True

    def update(self):
        pass


class Building_House:
    def __init__(self):
        self.name = 'Хижина'
        self.image_icon = r"/images/house.png"
        self.building_type = 'Социальные'
        self.technologies_for_unlock = [None]
        self.time_building = 100
        self.cost_wood = 60
        self.cost_food = 0
        self.cost_iron = 40
        self.cost_clay = 5
        self.b_lvl = 1


class Building_Barracks:
    def __init__(self):
        self.name = 'Казармы'
        self.image_icon = r"/images/barracks.png"
        self.building_type = 'Военные'
        self.technologies_for_unlock = ['Военное дело']
        self.time_building = 100
        self.cost_wood = 20
        self.cost_food = 30
        self.cost_iron = 400
        self.cost_clay = 50
        self.b_lvl = 1


class Building_Granary:
    def __init__(self):
        self.name = 'Землянка'
        self.image_icon = r"/images/building_found.png"
        self.building_type = 'Социальные'
        self.technologies_for_unlock = ['Колесо', 'Дома']
        self.time_building = 100
        self.cost_wood = 30
        self.cost_food = 0
        self.cost_iron = 5
        self.cost_clay = 0
        self.b_lvl = 1


class Building_Masterskaya:
    def __init__(self):
        self.name = 'Мастерская'
        self.image_icon = r"/images/building_found.png"
        self.building_type = 'Производственные'
        self.technologies_for_unlock = ['Обработка дерева']
        self.time_building = 175
        self.cost_wood = 7400
        self.cost_iron = 500
        self.cost_food = 2800
        self.cost_clay = 388
        self.b_lvl = 1
