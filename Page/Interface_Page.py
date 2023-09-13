import Page as public_pack


class interface:
    def __init__(self):
        pass

    def get_apk_package_name(self, apk_file_path):
        try:
            # 加载 APK 文件
            apk = public_pack.APK(apk_file_path)
            # 获取包名
            package_name = apk.get_package()
            print("APK 文件的包名为:", package_name)
        except Exception as e:
            print("获取包名时出现错误:", e)

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
