import allure
from utils.base_web_driver import BaseWebDriver
import pytest
from Common import Log
from Page.Devices_Page import DevicesPage
from Page.Message_Page import MessagePage
from Page.Telpo_MDM_Page import TelpoMDMPage
from Page.OTA_Page import OTAPage
import time
from Common.excel_data import ExcelData
from Conf.Config import Config
from Common.simply_case import Optimize_Case
from Common.DealAlert import AlertData
from Page.Release_Device_Page import ReleaseDevicePage

conf = Config()
excel = ExcelData()
opt_case = Optimize_Case()
alert = AlertData()

log = Log.MyLog()


class TestOTAPage:

    def setup_class(self):
        self.driver = BaseWebDriver().get_web_driver()
        self.page = OTAPage(self.driver, 40)

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_test02')
    @allure.title("OTA-Upgrade Packages Page")
    def test_upgrade_package_page(self):
        self.page.click_OTA_btn()
        self.page.click_upgrade_packages()

    @allure.feature('MDM_test01')
    @allure.title("OTA-Add OTA package")
    def test_add_OTA_package(self):
        exp_existed_text = "ota already existed"
        exp_success_text = "success"
        package_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "file_category": "test", "plat_form": "Android"}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        ota_info = {"file_name": file_path,  "file_category": package_info["file_category"], "plat_form": package_info["plat_form"]}
        self.page.click_add_btn()
        self.page.input_ota_package_info(ota_info)
        self.page.click_save_add_ota_pack()
        text = self.page.get_alert_text()
        print(text)
        if exp_existed_text in text:
            self.page.refresh_page()
        elif exp_success_text in text:
            # search package
            self.page.search_device_by_pack_name(package_info["package_name"])
        time.sleep(3)

        # "loading-title txt-textOneRow"

    @allure.feature('MDM_test02')
    @allure.title("OTA-release OTA package")
    def test_release_OTA_package(self):
        exp_success_text = "success"
        exp_existed_text = "ota release already existed"
        release_info = {"package_name": "TPS900_msm8937_sv10_fv1.1.16_pv1.1.16-1.1.18.zip", "sn": "A250900P03100019",
                        "silent": 0, "category": "NO Limit", "network": "NO Limit", }

        self.page.click_upgrade_packages()
        # search package
        self.page.search_device_by_pack_name(release_info["package_name"])
        # ele = self.page.get_package_ele(release_info["package_name"])
        self.page.click_release_btn()
        self.page.input_release_OTA_package(release_info)

        text = self.page.click_alert_release_btn()
        # text = self.page.get_alert_text()
        if exp_success_text in text:
            self.page.click_package_release_page()
        elif exp_existed_text in text:
            self.page.refresh_page()











