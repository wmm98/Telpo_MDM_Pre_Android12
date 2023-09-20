import Page as public_pack

sub_shell = public_pack.Shell.Shell()


class interface:
    def __init__(self):
        pass

    def text_is_existed(self, text1, text2):
        sub = self.remove_space(text1)
        string = self.remove_space(text2)
        if sub in string:
            return True
        else:
            return True

    def devices_list(self):
        return sub_shell.invoke("adb devices")

    def connect_ip(self, ip):
        ip_info1 = "connected to %s" % ip
        ip_info2 = "already connected to %s" % ip
        cmd = "adb connect %s" % ip
        print(cmd)
        res = sub_shell.invoke(cmd)
        print(res)
        res = self.remove_space(res)
        if self.remove_space(ip_info1) in res or self.remove_space(ip_info2) in res:
            return True
        else:
            return False

    def disconnect_ip(self, ip):
        res = sub_shell.invoke("adb disconnect %s" % ip)
        print(res)

    def confirm_wifi_adb_connected(self, ip, timeout=90):
        now_time = self.get_current_time()
        while True:
            res = self.connect_ip(ip)
            if res:
                break
            self.time_sleep(2)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                raise Exception("无法连接上WIFI adb")
        self.device_existed(ip)

    def device_existed(self, address):
        now_time = self.get_current_time()
        while True:
            device_online = address + "device"
            res = self.devices_list()
            print(res)
            if device_online in res.replace('\r', '').replace('\t', '').replace(' ', ''):
                break
            if self.get_current_time() > self.return_end_time(now_time, 60):
                self.connect_ip(address)
                assert False, "@@@@无法连接上wifi adb， 请检查！！！！"
            self.time_sleep(1)

    def transfer_version_into_int(self, ver):
        integer_list = ver.split(".")
        integer_version = "".join(integer_list)
        return int(integer_version)

    def load_apk_package(self, path):
        # get apk file
        apk = public_pack.APK(path)
        return apk

    def get_apk_package_name(self, apk_file_path):
        try:
            # get apk package file name
            return self.load_apk_package(apk_file_path).get_package()
        except Exception as e:
            assert False, "@@@@获取包名时出现错误"

    def get_apk_package_version(self, apk_file_path):
        # get package version
        try:
            return self.load_apk_package(apk_file_path).get_androidversion_name()
        except Exception:
            assert False, "@@@@获取包版本时出现错误"

    def get_file_size_in_windows(self, file_path):
        if public_pack.os.path.exists:
            try:
                size = public_pack.os.path.getsize(file_path)
                return size
            except Exception:
                return -1
        else:
            assert False, "@@@@不存在%s, 请检查！！！" % file_path

    def remove_space(self, text):
        return text.replace("\r", "").replace("\n", "").replace(" ", "")

    def upper_transfer(self, text):
        return text.upper()

    def get_current_time(self):
        return public_pack.t_time.time()

    def time_sleep(self, sec):
        public_pack.t_time.sleep(sec)

    def extract_integers(self, text):
        # pattern = r"\d+"
        pattern = r'\d+\.\d+|\d+'
        integers = public_pack.re.findall(pattern, text)
        if len(integers) != 0:
            return [inter for inter in integers]
        else:
            return integers

    def format_string_time(self, time_list):
        if len(time_list) != 0:
            format_time = "%s-%s-%s %s:%s" % (time_list[2], time_list[0], time_list[1], time_list[3], time_list[4])
            return format_time
        else:
            assert False, "@@@@没有显示时间，请检查！！！"

    def format_time(self, time_list):
        if len(time_list) != 0:
            format_time = "%s-%s-%s %s:%s" % (time_list[0], time_list[1], time_list[2], time_list[3], time_list[4])
            return format_time
        else:
            assert False, "@@@@没有显示时间，请检查！！！"

    def compare_time(self, time1, time2):
        dt1 = public_pack.datetime.strptime(time1, "%Y-%m-%d %H:%M")
        dt2 = public_pack.datetime.strptime(time2, "%Y-%m-%d %H:%M")
        if dt1 <= dt2:
            return True
        else:
            return False

    def return_end_time(self, now_time, timeout=180):
        timedelta = 1
        end_time = now_time + timeout
        return end_time


if __name__ == '__main__':
    path = "E:\Mingming\Telpo_Automation\Telpo_MDM\Param\Package\ComAssistant.apk"
    case = interface()
    # name = case.get_apk_package_name(path)
    # print(name)
    # version = case.get_apk_package_version(path)
    # print(version)
    #