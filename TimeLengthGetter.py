import re


class TimeLengthGetter:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.fileLines: list = []

        self.reMinute = re.compile(r".*（(\d+)分")
        self.reSecond = re.compile(r".*分(\d+)秒）.*")
        self.minute: int = 0
        self.second: int = 0

    def open_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            self.fileLines = file.readlines()

    def re_match(self):
        for line in self.fileLines:
            minute: int = 0
            second: int = 0
            minuteMatchResult = self.reMinute.match(line)
            if minuteMatchResult is not None:
                minute = int(minuteMatchResult.groups()[0])
            secondMatchResult = self.reSecond.match(line)
            if secondMatchResult is not None:
                second = int(secondMatchResult.groups()[0])
            self.minute += minute
            self.second += second

    def calculate_total_time(self):
        print("minute:", self.minute)
        print("second:", self.second)
        self.minute += self.second // 60
        self.second = self.second % 60
        print("总时间：{}:{}:{}".format(self.minute // 60, self.minute % 60, self.second))


if __name__ == "__main__":
    timeLengthGet = TimeLengthGetter(r"resources/TimeLengthSourceData.txt")
    timeLengthGet.open_file()
    timeLengthGet.re_match()
    timeLengthGet.calculate_total_time()
