from selenium.common import TimeoutException
from Conf.Config import Config
from Page.Telpo_MDM_Page import TelpoMDMPage
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time

conf = Config()


class APPSPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # private app related
    loc_private_app_btn = (By.LINK_TEXT, "Private Apps")
    private_app_main_title = "Private Apps"

    # new apk btn
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square']")
    loc_choose_file = (By.ID, "file")
    loc_choose_category = (By.ID, "Category")
    loc_developer_box = (By.ID, "developer")
    loc_des_box = (By.ID, "desc")
    loc_apk_save_btn = (By.CSS_SELECTOR, "btn btn-primary comfirm_create_app_button")

    # alert show
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    def click_private_app_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_private_app_btn))
        self.click(self.loc_private_app_btn)
        while True:
            if self.private_app_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_private_app_btn)
            if time.time() > self.return_end_time():
                assert False, "@@@@打开private app page 出错！！！"

    def click_add_btn(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_new_btn))
        self.click(self.loc_new_btn)
        self.confirm_alert_existed(self.loc_new_btn)

    def input_app_info(self, info):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_choose_file))
        self.input_text(self.loc_choose_file, info["file_name"])
        self.select_by_text(self.loc_choose_category, info["file_category"])
        self.input_text(self.loc_developer_box, info["developer"])
        self.input_text(self.loc_des_box, info["description"])
        time.sleep(1)
        self.click(self.loc_apk_save_btn)
        self.confirm_alert_not_existed(self.loc_apk_save_btn)

    def click_save_add_ota_pack(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_apk_save_btn))
        self.click(self.loc_apk_save_btn)
        self.confirm_alert_not_existed(self.loc_apk_save_btn)

    def alert_fade(self):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 6)
            return True
        except TimeoutException:
            return False

        # check if alert would appear

    def alert_show(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 6)
            return True
        except TimeoutException:
            return False

    def get_alert_text(self):
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text

    def confirm_alert_not_existed(self, loc, ex_js=0):
        while True:
            if self.alert_fade():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
