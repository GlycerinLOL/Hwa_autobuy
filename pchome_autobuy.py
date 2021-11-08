#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import json
import time
import requests

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By



"""
匯入欲搶購的連結、登入帳號、登入密碼及其他個資
"""
from settings import (
    URL, DRIVER_PATH, CHROME_PATH, ACC, PWD,
    BuyerSSN, BirthYear, BirthMonth, BirthDay, multi_CVV2Num    
)

options = webdriver.ChromeOptions()  
options.add_argument(CHROME_PATH)  

driver = webdriver.Chrome(
    executable_path="D:\Coding\Python\PChome-AutoBuy\chromedriver.exe", options=options)
driver.set_page_load_timeout(120)

def login():
    WebDriverWait(driver, 2).until(
        expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/form/div[1]/div/div/input'))
    )
    elem = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/form/div[1]/div/div/input')
    elem.clear()
    elem.send_keys(ACC)
    elem = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/form/div[2]/div/div/input')
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
    driver.get(URL)

    """
    放入購物車
    """
    click_button_id('#btn-variable-buy-now')

    """
    前往購物車
    """
    driver.get("https://www.huahuacomputer.com.tw/cart")

    """
    登入帳戶（若有使用 CHROME_PATH 記住登入資訊，第二次執行時可註解掉）
    """
    try:
        login()
    except:
        print('Already Logged in!')

    """
    前往結帳 (一次付清) (要使用 JS 的方式 execute_script 點擊)
    """
    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div[3]/div[5]/div[2]/section/div[2]/a'))
    )
    driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/div/div[3]/div[5]/div[2]/section/div[2]/a').click()


    """
    勾選同意（注意！若帳號有儲存付款資訊的話，不需要再次勾選，請註解掉！）
    """
    click_button(xpaths['check_agree'])

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


"""
抓取商品開賣資訊，並嘗試搶購
"""

curr_retry = 0
max_retry = 5   # 重試達 5 次就結束程式，可自行調整
wait_sec = 1    # 1 秒後重試，可自行調整秒數


if __name__ == "__main__":
    while curr_retry<max_retry: 
        driver.get(URL)
        if(driver.find_element_by_id('#btn-variable-buy-now').is_enabled()):
            print('商品開賣！')
            main()
            break
        else:
            print('商品尚未開賣！')
            curr_retry+=1
            time.sleep(wait_sec)
            


os.system("pause")