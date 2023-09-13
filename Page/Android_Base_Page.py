import Page as public_pack
from Page.Interface_Page import interface

sub_shell = public_pack.Shell.Shell()


class AndroidBasePage(interface):
    def __init__(self, client, times, name):
        self.client = client
        self.times = times
        self.device_name = name

    def get_device_name(self):
        return self.device_name

    def get_internal_storage_directory(self):
        if "aimdm" in self.u2_send_command("ls sdcard/"):
            return "sdcard"
        elif "aimdm" in self.u2_send_command("ls data/"):
            return "data"

    def ping_network(self, times):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, "www.baidu.com")
        exp = self.remove_space("ping: unknown host %s" % "www.baidu.com")
        now_time = self.get_current_time()
        while True:
            res = self.remove_space(self.send_shell_command(cmd))
            print(res)
            if exp not in res:
                break
            public_pack.t_time.sleep(1)
            if self.get_current_time() > self.return_end_time(now_time, 120):
                if exp in self.remove_space(self.send_shell_command(cmd)):
                    assert False, "超过2分钟无法上网,请检查网络"

    def device_unlock(self):
        self.client.screen_off()
        self.client.unlock()

    def u2_send_command(self, cmd):
        try:
            return self.client.shell(cmd, timeout=120).output
        except TypeError:
            raise Exception("@@@@传入的指令无效！！！")
        except RuntimeError:
            raise Exception("@@@@设备无响应， 查看设备的连接情况！！！")

    def send_shell_command(self, cmd):
        try:
            command = "adb -s %s shell %s" % (self.device_name, cmd)
            return sub_shell.invoke(command, runtime=30)
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def send_adb_command(self, cmd):
        try:
            command = "adb -s %s %s" % (self.device_name, cmd)
            res = sub_shell.invoke(command, runtime=30)
            return res
        except Exception:
            print("@@@@发送指令有异常， 请检查！！！")

    def device_boot_complete(self):
        time_out = self.get_current_time() + 120
        try:
            while True:
                boot_res = self.send_shell_command("getprop sys.boot_completed")
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
                boot_res = self.send_shell_command("getprop sys.boot_completed")
                print(boot_res)
                if str(1) in boot_res:
                    break
                self.time_sleep(2)
        except Exception as e:
            assert False, "@@@@启动出问题，请检查设备启动情况！！！"

    def devices_list(self):
        return sub_shell.invoke("adb devices")

    def device_exist(self):
        while True:
            res = sub_shell.invoke("adb devices")
            print(res)
            if self.device_name in res.replace('\r', '').replace('\t', '').replace(' ', ''):
                break
            self.time_sleep(2)

    def click_element(self, ele):
        ele.click()

    def get_element_text(self, ele):
        text = ele.get_text()
        return text

    def input_element_text(self, ele, text):
        ele.clear_text()
        ele.send_keys(text)

    def get_element_by_id(self, id_no, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        if self.wait_ele_presence_by_id(id_no, time_to_wait):
            return self.client(resourceId=id_no)

    def get_element_by_id_no_wait(self, id_no):
        return self.client(resourceId=id_no)

    def get_element_by_class_name(self, class_name, timeout=0):
        if timeout == 0:
            time_to_wait = self.times
        else:
            time_to_wait = timeout
        self.wait_ele_presence_by_class_name(class_name, time_to_wait)
        return self.client(className=class_name)

    def wait_ele_presence_by_id(self, id_no, time_to_wait):
        flag = self.client(resourceId=id_no).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_presence_by_class_name(self, class_name, time_to_wait):
        flag = self.client(className=class_name).exists(timeout=time_to_wait)
        if flag:
            return True
        else:
            assert False, "@@@@查找元素超时！！！"

    def wait_ele_gone_by_id(self, id_no, wait):
        if wait == 0:
            time_to_wait = 5
        else:
            time_to_wait = wait
        return self.client(resourceId=id_no).wait_gone(timeout=time_to_wait)

    def wait_ele_gone_by_class_name(self, class_name, time_to_wait):
        return self.client(className=class_name).exists(timeout=time_to_wait)

    def alert_show(self, id_no, time_to_wait):
        try:
            self.wait_ele_presence_by_id(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def alert_fade(self, id_no, time_to_wait):
        try:
            self.wait_ele_gone_by_id(id_no, time_to_wait)
            return True
        except AssertionError:
            return False

    def wait_alert_fade(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_fade(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)

    def wait_alert_appear(self, id_no, time_to_wait):
        now_time = self.get_current_time()
        while True:
            if self.alert_show(id_no, time_to_wait):
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False
            self.time_sleep(1)


if __name__ == '__main__':
    from utils.client_connect import ClientConnect

    conn = ClientConnect()
    conn.connect_device("d")
    d = conn.get_device()
    page = AndroidBasePage(d, 10, d.serial)
    res = page.u2_send_command("getprop ro.serialno")
    print(res)
    element = page.get_element_by_id("com.tpos.aimdm:id/tip")
    print(page.get_element_text(element))
    # if ele:
    #     print(page.get_element_text(ele))
