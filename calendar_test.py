import uiautomator2 as u2
import time
import unittest

import os
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction


class ActionHelpers(webdriver.Remote):

    def scroll(self, origin_el, destination_el, duration=None):
        """Scrolls from one element to another
        :Args:
         - originalEl - the element from which to being scrolling
         - destinationEl - the element to scroll to
         - duration - a duration after pressing originalEl and move the element to destinationEl.
         Default is 600 ms for W3C spec. Zero for MJSONWP.
        :Usage:
            driver.scroll(el1, el2)
        """

        # XCUITest x W3C spec has no duration by default in server side
        if self.w3c and duration is None:
            duration = 600

        action = TouchAction(self)
        if duration is None:
            action.press(origin_el).move_to(destination_el).release().perform()
        else:
            action.press(origin_el).wait(duration).move_to(destination_el).release().perform()
        return self


def setUp(self):
    self.driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723/wd/hub',
        desired_capabilities={
            'platformName': 'Android',
            'platformVersion': '10',
            'deviceName': 'Galaxy S9',
            'automationName': 'Appium',
            'udid': '228822820f017ece'
        })


def test_calendar(self):
    driver = self.driver
    # device ID 정의
    device_id = "228822820f017ece"
    # 핸드폰을 연결한다
    d = u2.connect(device_id)
    # 정상적으로 연결된다
    # assert not device.alive, "디바이스가 정상적으로 연결되지 않았습니다."

    # 캘린더 앱을 실행한다
    app_package = "com.samsung.android.calendar"
    d.app_start(app_package)
    # 프로그램이 정상적으로 수행된다
    pid = d.app_wait(app_package, timeout=20.0)
    if not pid:
        print("com.example.android is not running")
        assert False, f"{app_package}가 정상적으로 수행되지 않았습니다."

    # 할 일 이름값을 정의한다
    task_name = f"{time.time()}_할일"
    # 새로운 일정을 등록한다
    # 일정을 추가할 날짜를 클릭(11월 7일  토요일)
    d.xpath('//*[@text="2020-11-7"]').click()
    # 추가 버튼 클릭
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/floating_action_button"]').click()
    # 일정 내용 입력
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/title"]').set_text(task_name)
    # 저장 버튼 클릭
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/add_app_bar_menu_done"]').click()

    # 일정이 정상적으로 등록되었는지 확인한다

    # 햄버거 메뉴 클릭
    d.xpath('//*[@resource-id="com.samsung.android.calendar:id/open_drawer_container"]').click()
    # 스크롤 다운
    departure = d.xpath(
        '//*[@resource-id="com.samsung.android.calendar:id/drawer_list"]/android.widget.LinearLayout[1]')
    destination = d.xpath(
        '//*[@resource-id="com.samsung.android.calendar:id/drawer_list"]/android.widget.LinearLayout[7]/android.widget.LinearLayout[1]')

    # driver.scroll(d.xpath(departure), d.xpath(destination), duration=None)

    actions = TouchAction(self.driver)
    actions.press(el = departure).move_to(el = destination).release().perform()

    # TouchAction().press(departure).moveTo(destination).release()
    # TouchAction().press(100, 100).moveTo(200, 200).release()

    # driver.execute_script("mobile: scroll", {"direction": "down", element: element.getAttribute("destination")})
    # 검색 버튼 클릭
    d.xpath('//*[@text="검색"]').click()
    # task_name으로 검색
    d(resourceId="com.samsung.android.calendar:id/title", text="검색").set_text(task_name)
    # task_name element 존재 여부 확인
    d(resourceId="com.samsung.android.calendar:id/title", text=task_name).exists()

test_calendar(self)