#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import json
import time
import requests
import datetime

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import date



"""
匯入欲搶購的連結、登入帳號、登入密碼及其他個資
"""
from settings import (
    URL, DRIVER_PATH, CHROME_PATH, ACC, PWD,    
)

options = webdriver.ChromeOptions()  
options.add_argument(CHROME_PATH)  

driver = webdriver.Chrome(
    executable_path=DRIVER_PATH, options=options)
driver.set_page_load_timeout(120)

def login():
    WebDriverWait(driver, 2).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'form.simple_form:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)'))
    )
    elem = driver.find_element_by_css_selector('form.simple_form:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)')
    elem.clear()
    elem.send_keys(ACC)
    elem = driver.find_element_by_css_selector('form.simple_form:nth-child(7) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)')
    elem.clear()
    elem.send_keys(PWD)
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((By.ID, "sign-in-btn"))
    )
    driver.find_element_by_id('sign-in-btn').click()
    print('成功登入')


def click_button(xpath):
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, xpath))
    )
    driver.find_element_by_xpath(xpath).click()

def click_button_id(Btnid):
    WebDriverWait(driver,20).until(
        expected_conditions.element_to_be_clickable(
            (By.ID,Btnid)
        )
    )
    driver.find_element_by_id(Btnid).click()

def click_button_css(Btncss):
    WebDriverWait(driver,20).until(
        expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR,Btncss)
        )
    )
    driver.find_element_by_css_selector(Btncss).click()



"""
集中管理需要的 xpath
"""
xpaths = {
    'add_to_cart': r"/html/body/div[6]/div[1]/div/div/div/div[2]/div[3]/div[2]/div[4]/div[7]/button[2]/div",
    'check_agree': r"/html/body/div[6]/div/div/div/div/div[5]/div[1]/form/div/label/input",
    'Pay_btn': r"/html/body/div[6]/div[1]/div/div/div/div[3]/div[5]/div[2]/section/div[2]/a",
    # 'pay_once': "//li[@class=CC]/a[@class='ui-btn']",
    # 'pay_line': "//li[@class=LIP]/a[@class='ui-btn line_pay']", 
    # 'submit': "//a[@id='btnSubmit']",
    # 'warning_msg': "//a[@id='warning-timelimit_btn_confirm']",  # 之後可能會有變動
}

def main():

    """
    放入購物車
    """
    click_button_id('#btn-variable-buy-now')

    """
    前往結帳 (一次付清) (要使用 JS 的方式 execute_script 點擊)
    """
    
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a.btn:nth-child(2)"))
    )
    driver.find_element_by_css_selector("a.btn:nth-child(2)").click()
    

    """
    勾選同意（注意！若帳號有儲存付款資訊的話，不需要再次勾選，請註解掉！）
    """
    click_button_css(".checkbox > label:nth-child(1) > input:nth-child(1)")

    """
    送出訂單 (要使用 JS 的方式 execute_script 點擊)
    """
    '''
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "place-order-btn"))
    )
    button = driver.find_element_by_id("place-order-btn")
    driver.execute_script("arguments[0].click();", button)
    '''

    os.system("pause")

def main2():
    
    """
    放入購物車
    """
    click_button_id('btn-main-checkout')

    driver.get("https://www.huahuacomputer.com.tw/cart")
    driver.refresh()

    """
    前往結帳 (一次付清) (要使用 JS 的方式 execute_script 點擊)
    """
    
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a.btn:nth-child(2)"))
    )
    driver.find_element_by_css_selector("a.btn:nth-child(2)").click()
    

    """
    勾選同意（注意！若帳號有儲存付款資訊的話，不需要再次勾選，請註解掉！）
    """
    click_button_css(".checkbox > label:nth-child(1) > input:nth-child(1)")

    """
    送出訂單 (要使用 JS 的方式 execute_script 點擊)
    """
    '''
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "place-order-btn"))
    )
    button = driver.find_element_by_id("place-order-btn")
    driver.execute_script("arguments[0].click();", button)
    '''

    os.system("pause")
    


"""
抓取商品開賣資訊，並嘗試搶購
"""

target_time=datetime.datetime(2021,11,11,23,15,00)

curr_time=datetime.datetime.now()
wait_sec = 0.3    # 1 秒後重試，可自行調整秒數


if __name__ == "__main__":
    while curr_time<target_time: 
        driver.get(URL)
        if(driver.find_element_by_id("#btn-variable-buy-now").is_displayed()):
            print('商品開賣！')
            driver.get("https://www.huahuacomputer.com.tw/users/sign_in")
            if(driver.find_elements_by_css_selector("form.simple_form:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)")):
                login()
            main()
            break
        elif(driver.find_element_by_id("btn-main-checkout").is_enabled()):
            driver.get("https://www.huahuacomputer.com.tw/users/sign_in")
            print('商品開賣！')
            if(driver.find_elements_by_css_selector("form.simple_form:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)")):
                login()
            main2()
            break
        else:
            print('商品尚未開賣！')
            time.sleep(wait_sec)
            


