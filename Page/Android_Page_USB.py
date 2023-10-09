import Page as public_pack
from Page.Interface_Page import interface

sub_shell = public_pack.Shell.Shell()


class AndroidBasePageUSB(interface):
    def __init__(self, client, times, name):
        self.USB_client = client
        self.times = times
        self.device_name = name

    def start_app_USB(self, package_name):
        self.USB_client.app_start(package_name)
        self.time_sleep(3)
        self.confirm_app_start(package_name)

    def get_current_app_USB(self):
        return self.USB_client.app_current()['package']

    def confirm_app_start(self, package_name):
        now_time = self.get_current_time()
        while True:
            if package_name in self.get_current_app_USB():
                break
            else:
                self.start_app_USB(package_name)
        if self.get_current_time() > self.return_end_time(now_time):
            assert False, "@@@@app无法启动， 请检查！！！！"
        self.time_sleep(2)

    def get_app_info_USB(self, package):
        """
        Return example:
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }
            """
        try:
            app_information = self.USB_client.app_info(package)
            return app_information
        except public_pack.UiaError as e:
            print("获取app信息发生异常：", e)
            assert False, e

    def get_app_installed_list_USB(self):
        return self.USB_client.app_list()

    def app_is_installed_USB(self, package):
        if package in self.get_app_installed_list_USB():
            return True
        else:
            return False

    def uninstall_app_USB(self, package):
        status = self.USB_client.app_uninstall(package)
        return status

    def get_device_name_USB(self):
        return self.device_name

    def download_file_is_existed_USB(self, file_name):
        res = self.u2_send_command_USB(
            "ls /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory_USB(), file_name))
        if self.remove_space(file_name) in self.remove_space(res):
            return True
        else:
            return False

    def get_file_size_in_device_USB(self, file_name):
        "-rw-rw---- 1 root sdcard_rw   73015 2023-09-05 16:51 com.bjw.ComAssistant_1.1.apk"
        res = self.u2_send_command_USB(
            "ls -l /%s/aimdm/download/ |grep %s" % (self.get_internal_storage_directory_USB(), file_name))
        # get integer list in res
        integer_list = self.extract_integers(res)
        size = int(integer_list[1])
        return size

    def get_internal_storage_directory_USB(self):
        if "aimdm" in self.u2_send_command_USB("ls sdcard/"):
            return "sdcard"
        elif "aimdm" in self.u2_send_command_USB("ls data/"):
            return "data"
        else:
            assert False, "@@@@ 内部sdcard和data下均不存在aimdm文件夹， 请检查设备内核版本！！！！"

    def get_cur_wifi_status(self):
        return self.u2_send_command_USB("settings get global wifi_on")

    def wifi_open_status(self):
        return self.text_is_existed("1", self.get_cur_wifi_status())

    def wifi_close_status(self):
        return self.text_is_existed("0", self.get_cur_wifi_status())

    def open_wifi_btn(self):
        if "0" in self.get_cur_wifi_status():
            self.u2_send_command_USB("svc wifi enable")
            return self.wifi_open_status()
        return True

    def close_wifi_btn(self):
        if "1" in self.get_cur_wifi_status():
            self.u2_send_command_USB("svc wifi disable")
            return self.wifi_close_status()
        return True

    def confirm_wifi_status_open(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.wifi_open_status():
                break
            else:
                self.time_sleep(3)
                self.open_wifi_btn()
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@超过2分钟打开wifi按钮， 请检查！！！"

    def confirm_wifi_status_close(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.wifi_close_status():
                break
            else:
                self.time_sleep(3)
                self.close_wifi_btn()
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert False, "@@@@超过2分钟关闭wifi按钮， 请检查！！！"

    def ping_network(self, times=5, timeout=120):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            res = self.remove_space(self.send_shell_command_USB(cmd))
            print(res)
            if exp not in res:
                break
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                if exp in self.remove_space(self.send_shell_command_USB(cmd)):
                    assert False, "@@@@超过2分钟无法上网,请检查网络"
            public_pack.t_time.sleep(2)

    def device_unlock_USB(self):
        self.USB_client.screen_off()
        self.USB_client.unlock()

    def u2_send_command_USB(self, cmd):
        try:
            return self.USB_client.shell(cmd, timeout=120).output
        except Exception as e:
            print(e)
        # except TypeError:
        #     raise Exception("@@@@传入的指令无效！！！")
        # except RuntimeError:
        #     raise Exception("@@@@设备无响应， 查看设备的连接情况！！！")

    def send_shell_command_USB(self, cmd):
        try:
            command = "adb -s %s shell %s" % (self.device_name, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def send_adb_command_USB(self, cmd):
        try:
            command = "adb -s %s %s" % (self.device_name, cmd)
            print("command:", command)
            res = sub_shell.invoke(command, runtime=30)
            return res
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def device_boot_complete_USB(self):
        time_out = self.get_current_time() + 120
        try:
            while True:
                boot_res = self.send_shell_command_USB("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                if self.get_current_time() > time_out:
                    print("完全启动超时")
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def device_boot_complete_debug_off(self):
        try:
            while True:
                boot_res = self.send_shell_command_USB("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def click_element_USB(self, ele):
        ele.click()

    def get_element_text_USB(self, ele):
        text = ele.get_text()
        return text

    def input_element_text_USB(self, ele, text):
        ele.clear_text()
        ele.send_keys(text)

    def get_element_by_id_USB(self, id_no, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        if self.wait_ele_presence_by_id_USB(id_no, time_to_wait):
            return self.USB_client(resourceId=id_no)

    def get_element_by_id_no_wait_USB(self, id_no):
        return self.USB_client(resourceId=id_no)

    def get_element_by_class_name_USB(self, class_name, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        self.wait_ele_presence_by_class_name_USB(class_name, time_to_wait)
        return self.USB_client(className=class_name)

    def wait_ele_presence_by_id_USB(self, id_no, time_to_wait):
        flag = self.USB_client(resourceId=id_no).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_presence_by_class_name_USB(self, class_name, time_to_wait):
        flag = self.USB_client(className=class_name).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_gone_by_id_USB(self, id_no, wait):
        if wait == 0:
            time_to_wait = 5
        else:
            time_to_wait = wait
        return self.USB_client(resourceId=id_no).wait_gone(timeout=time_to_wait)

    def wait_ele_gone_by_class_name_USB(self, class_name, time_to_wait):
        return self.USB_client(className=class_name).exists(timeout=time_to_wait)

    def alert_show(self, id_no, time_to_wait):
        try:
            self.wait_ele_presence_by_id_USB(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def alert_fade(self, id_no, time_to_wait):
        try:
            self.wait_ele_gone_by_id_USB(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def wait_alert_fade_USB(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_fade(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def wait_alert_appear_USB(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_show(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def open_mobile_data(self):
        cmd = "svc data enable"
        self.u2_send_command_USB(cmd)
        self.time_sleep(5)

    def close_mobile_data(self):
        cmd = "svc data disable"
        self.u2_send_command_USB(cmd)
        self.open_wifi_btn()


if __name__ == '__main__':
    from utils.client_connect import ClientConnect

    conn = ClientConnect()
    conn.connect_device("d")
    d = conn.get_device()
    page = AndroidBasePageUSB(d, 10, d.serial)
    res = page.u2_send_command_USB("getprop ro.serialno")
    print(res)
    element = page.get_element_by_id_USB("com.tpos.aimdm:id/tip")
    print(page.get_element_text_USB(element))
    # if ele:
    #     print(page.get_element_text(ele))