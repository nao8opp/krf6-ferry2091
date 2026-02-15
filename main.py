import os
import time
import re
import sys
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage import Chromium
import random
import argparse
import requests
from datetime import datetime

chrome_candidates = [
        "/opt/google/chrome/chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/lib/chromium/chromium",
        "/usr/lib/chromium-browser/chromium-browser",
        "/snap/bin/chromium",
        "/snap/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/local/bin/chromium",
        "/usr/local/bin/chromium-browser",
        "/usr/bin/microsoft-edge-stable",
        "/opt/microsoft/msedge/msedge"
    ]
    
binpath = next((path for path in chrome_candidates if os.path.exists(path)), None)
cwd = os.getcwd()

if binpath:
    print(f"✅ 找到浏览器路径: {binpath}")
else:
    print("⚠️ 警告: 未找到浏览器可执行文件,将使用系统默认路径")
    binpath = None

parser = argparse.ArgumentParser(description="weridhost续期")
parser.add_argument('-k', '--keep', action='store_true', help='启用保留模式')
parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
iargs = parser.parse_args()

# ========== Telegram 通知功能 ==========
def send_telegram_message(message, parse_mode='HTML'):
    """发送 Telegram 消息"""
    bot_token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("⚠️ 未配置 Telegram 通知（缺少 TG_BOT_TOKEN 或 TG_CHAT_ID）")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Telegram 通知发送成功")
            return True
        else:
            print(f"⚠️ Telegram 通知发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ 发送 Telegram 消息时出错: {e}")
        return False

def send_telegram_photo(photo_path, caption=''):
    """发送 Telegram 图片"""
    bot_token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    
    if not bot_token or not chat_id:
        return False
    
    if not os.path.exists(photo_path):
        print(f"⚠️ 截图文件不存在: {photo_path}")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': chat_id,
                'caption': caption
            }
            response = requests.post(url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 截图发送成功: {photo_path}")
            return True
        else:
            print(f"⚠️ 截图发送失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ 发送截图时出错: {e}")
        return False

# ========================================

def safe_ele(obj, selector, timeout=5):
    try:
        return obj.ele(selector, timeout=timeout)
    except:
        return None
def safe_shadow_root(ele):
    try:
        return ele.shadow_root
    except:
        return None

def safe_get_frame(shadow, index):
    try:
        return shadow.get_frame(index)
    except:
        return None

def solve_turnstile(page):
    print('waiting for turnstile')

    div = safe_ele(page, 'xpath://*[@id="app"]/div[2]/div/div[2]/div[2]/section/div[1]/div[3]/div[1]/div/div[3]/div[2]/div/div[1]', 15) 
    if not div:
        div=safe_ele(page, 'xpath://*[@id="app"]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]', 15) 
        print(f'✅ 发现游戏机超过续期时间')
    else:
        print(f'✅ 游戏机在续期时间内')
    div2 = safe_ele(div, 'tag:div', 5) 
    div3 = safe_ele(div2, 'tag:div', 5) 
    shadow = safe_shadow_root(div3) 
    iframe1 = safe_get_frame(shadow, 1)
    body = safe_ele(iframe1, 'tag:body', 5) 
    shadow2=safe_shadow_root(body)
    checkbox = safe_ele(shadow2,'tag:input', 5) 
    

    if iargs.debug:
        check_element('div最外层', div)
        check_element('div2',div2) 
        check_element('div3',div3) 
        check_element('iframe',iframe1) 
        check_element('body',body) 
        check_element('shadow2',body) 
        check_element('checkbox',checkbox)
    else:
        elements = [
            ("div最外层", div),
            ("div2", div2),
            ("div3", div3),
            ("iframe", iframe1),
            ("body", body),
            ("checkbox", checkbox),
        ]
        for name, ele in elements:
            if ele is None:
                check_element(name, ele)
                break
    if 'checkbox' in locals() and checkbox:  
        xof = random.randint(5, 8)
        yof = random.randint(5, 8)
        capture_screenshot("when_cf_turnstile1.png",page=page)
        checkbox.offset(x=xof, y=yof).click(by_js=False)
        print(f'✅ 找到并点击turnstile')
        time.sleep(1)
        capture_screenshot("when_cf_turnstile2.png",page=page)
        return True
    return False

#机器超期时的续期
def solve_turnstile2(page):
    print('waiting for turnstile')

    div = safe_ele(page, 'xpath://*[@id="app"]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]', 15) 
    div2 = safe_ele(div, 'tag:div', 5) 
    div3 = safe_ele(div2, 'tag:div', 5) 
    shadow = safe_shadow_root(div3) 
    iframe1 = safe_get_frame(shadow, 1)
    body = safe_ele(iframe1, 'tag:body', 5) 
    shadow2=safe_shadow_root(body)
    checkbox = safe_ele(shadow2,'tag:input', 5) 
    

    if iargs.debug:
        check_element('div最外层', div)
        check_element('div2',div2) 
        check_element('div3',div3) 
        check_element('iframe',iframe1) 
        check_element('body',body) 
        check_element('shadow2',body) 
        check_element('checkbox',checkbox)
    else:
        elements = [
            ("div最外层", div),
            ("div2", div2),
            ("div3", div3),
            ("iframe", iframe1),
            ("body", body),
            ("checkbox", checkbox),
        ]
        for name, ele in elements:
            if ele is None:
                check_element(name, ele)
                break
    if 'checkbox' in locals() and checkbox:  
        xof = random.randint(5, 8)
        yof = random.randint(5, 8)
        checkbox.offset(x=xof, y=yof).click(by_js=False)
        print(f'✅ 找到并点击turnstile')
        

def check_action_success(page):
    success=page.ele("x://h2[contains(text(), '성공!')]",timeout=10)
    if success:
        print("✅ 续期成功")
        return True
    h2=page.ele("x://h2[contains(., '아직')]",timeout=5)
    error_found=page.ele("x://div[@type='error']",timeout=10)
    if h2 or error_found:
        print("⚠️ 未到续期时间。")
    if not error_found:
        print("⚠️ 按钮已点击,但未检测到明确的成功或错误提示。")

def capture_screenshot( file_name=None,save_dir='screenshots',page=None):
        os.makedirs(save_dir, exist_ok=True)
        if not file_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'screenshot_{timestamp}.png'
        full_path = os.path.join(save_dir, file_name)
        try:
            page.get_screenshot(path=save_dir, name=file_name, full_page=True)
            print(f"📸 截图已保存:{full_path}")
        except Exception as e:
            print(f"⚠️ 截图失败,未能成功保存。${e}")

def check_element(desc, element, exit_on_fail=True):
    if element:
        print(f'✓ {desc}: {element}')
        return True
    else:
        print(f'✗ {desc}: 获取失败')
        return False
def is_port_open(host='127.0.0.1', port=9222, timeout=1):
    import socket
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
def attach_browser(port=9222):
    try:
        if is_port_open():
            browser = Chromium(port)
            if browser.states.is_alive:
                print(f"✅ 成功接管浏览器(端口 {port})")
                return browser
            print("❌ 接管失败,浏览器未响应")
        else:
            print(f"⚠️ 端口 {port} 未开放,跳过接管")
        return None
    except Exception as e:
        print(f"⚠️ 接管浏览器时出错:{e}")
        return None
def search_btn(page):
    add_button_txt = "시간추가"
    print(f"🔍 正在查找 '{add_button_txt}' 按钮...")
    
    # 等待按钮容器出现(确保页面完全加载)
    try:
        page.wait.ele_displayed('//div[contains(@class, "RenewBox2")]', timeout=10)
    except:
        print("⚠️  等待 RenewBox2 容器超时,继续尝试查找...")
    
    # 优先级排序:从最精准 → 最宽松
    selectors = [
        # 1. 【最佳】通过 color="primary" 属性定位(唯一标识)
        '//button[@color="primary"]',
        
        # 2. 通过 class 特征定位
        '//button[contains(@class, "Button__ButtonStyle-sc-1qu1gou-0")]',
        
        # 3. 通过父容器定位(RenewBox2 内的第一个button)
        '//div[contains(@class, "RenewBox2")]//button[1]',
        
        # 4. 通过按钮文本定位(包含 "시간" 或 "추가" 之一)
        f'//button[contains(., "시간") or contains(., "추가")]',
        
        # 5. 最宽松:任意可见的 enabled button(仅作兜底)
        '//button'
    ]
    
    for i, selector in enumerate(selectors, 1):
        print(f"  [{i}/{len(selectors)}] 尝试选择器: {selector[:50]}...")
        btn = safe_ele(page, selector, timeout=3)
        
        if btn:
            # 优先检查文本内容是否匹配
            try:
                btn_text = btn.text.strip()
                if add_button_txt in btn_text:
                    print(f"    ✅ 找到匹配按钮(文本: '{btn_text}')")
                    return btn
                elif btn_text:
                    print(f"    ⚠️ 找到按钮但文本不匹配: '{btn_text}'")
                else:
                    print(f"    ⚠️ 找到按钮但无文本内容")
                
                # 如果是最后一个选择器,即使文本不匹配也返回
                if i == len(selectors):
                    print(f"    ℹ️ 使用兜底选择器返回该按钮")
                    return btn
                    
            except Exception as e:
                print(f"    ⚠️ 检查按钮文本时出错: {e}")
                if i == len(selectors):
                    return btn
        else:
            print(f"    ✗ 未找到匹配元素")
    
    print(f"❌ 所有选择器均未找到 '{add_button_txt}' 按钮")
    return None

def test():
    """
    测试环境检查函数
    """
    print("=" * 60)
    print("🧪 开始环境测试")
    print("=" * 60)
    
    # 检查环境变量
    print("\n【环境变量检查】")
    env_vars = ['SERVER_URL', 'REMEMBER_WEB_COOKIE', 'CHROME_PROXY']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # 敏感信息隐藏部分内容
            display_value = value if var == 'SERVER_URL' else f"{value[:10]}..."
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ⚠️ {var}: 未设置")
    
    # 检查浏览器路径
    print(f"\n【浏览器路径】")
    print(f"  {binpath if binpath else '未指定'}")
    
    # 检查显示模式
    print(f"\n【显示模式】")
    print(f"  {'有头模式 (DISPLAY=' + os.environ.get('DISPLAY', '') + ')' if 'DISPLAY' in os.environ else '无头模式'}")
    
    # 检查临时目录
    print(f"\n【临时目录】")
    tmp_dir = os.environ.get('TMPDIR', '/tmp')
    print(f"  TMPDIR: {tmp_dir}")
    print(f"  工作目录: {cwd}")
    
    print("\n" + "=" * 60)
    print("🧪 环境测试完成")
    print("=" * 60)

def add_server_time():
    """
    主要逻辑函数:启动浏览器并自动点击续期按钮
    """
    start_time = datetime.now()
    print("\n" + "=" * 60)
    print("🚀 开始执行 WeirdHost 服务器续期任务")
    print(f"📅 开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    # 从环境变量获取配置
    server_url = os.environ.get('SERVER_URL')
    remember_web_cookie = os.environ.get('REMEMBER_WEB_COOKIE')
    chrome_proxy = os.environ.get('CHROME_PROXY')
    
    # 检查必需的环境变量
    if not server_url:
        error_msg = "❌ 缺少必需的环境变量: SERVER_URL"
        print(error_msg)
        send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}")
        return False
    
    print(f"🔗 目标服务器: {server_url}")
    # print(f"🍪 使用 Cookie 登录: {'是' if remember_web_cookie else '否'}")
    
    # 设置用户代理
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    
    browser = None
    page = None
    
    # 配置 ChromiumOptions - 参考提供的格式
    options = (
        ChromiumOptions()
        .set_user_agent(user_agent)
        .set_argument('--guest')
        .set_argument('--no-sandbox')
        .set_argument('--disable-gpu')
        .set_argument('--window-size=1280,800')
        .set_argument('--disable-dev-shm-usage') 
        .set_argument(f'--user-data-dir={cwd}/.tmp')
        .set_argument('--disable-software-rasterizer')
        .set_browser_path(binpath)
    )
    
    # 设置代理
    if chrome_proxy:
         options.set_argument(f'--proxy-server={chrome_proxy}')
    
    # 设置无头模式
    if 'DISPLAY' not in os.environ:
        options.headless(True)
        print("✅ DISPLAY环境变量为空,浏览器使用无头模式")
    else:
        options.headless(False)
        print("✅ DISPLAY环境变量存在,浏览器使用正常模式")
    
    try:
        print("正在启动浏览器...")

        browser = Chromium(options)
        print("✅ 浏览器连接/启动成功")
        
        if browser is None:
            # 接管失败,启动新浏览器
            print("启动新的浏览器实例...")
            browser = Chromium(options)
            print("✅ 浏览器启动成功")
        else:
            print("✅ 已连接到现有浏览器")
        
        # 获取当前激活的标签页
        page = browser.latest_tab
        
        # 打印浏览器信息
        print(f"🌐 浏览器已准备就绪")
        print(f"🖥️  显示模式: {'无头模式' if 'DISPLAY' not in os.environ else '正常模式'}")
        
        login_success = False

        # --- 使用 Cookie 登录 ---
        if remember_web_cookie:
            print("检测到 REMEMBER_WEB_COOKIE,尝试使用 Cookie 直接登录...")
            try:
                # 清除并设置新Cookie
                page.set.cookies.clear()
                cookie_data = {
                    'name': 'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d',
                    'value': remember_web_cookie.strip(),
                    'path': '/',
                    'domain':'hub.weirdhost.xyz'
                }
                page.set.cookies(cookie_data)
                
                # 重新加载使Cookie生效
                page.get(server_url)
                page.wait.load_start()
                time.sleep(3)
                
                # 检查登录状态
                if "login" not in page.url and "auth" not in page.url:
                    print("✅ Cookie 登录成功")
                    login_success = True
                else:
                    print("❌ Cookie 登录失败,将尝试邮箱登录")
                    login_success = False
                    
            except Exception as e:
                print(f"Cookie 登录出错: {e}")
                login_success = False
        
        # --- 确保在正确的服务器页面 ---
        if not server_url in page.url:
            print(f"当前不在目标服务器页面,导航至: {server_url}")
            page.get(server_url)
            page.wait.load_start()
            time.sleep(3)
            
            if "login" in page.url.lower():
                error_msg = "❌ 导航失败,会话可能失效。"
                print(error_msg)
                capture_screenshot("server_page_nav_fail.png",page=page)
                send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}\n会话可能已失效,请检查 Cookie")
                send_telegram_photo("screenshots/server_page_nav_fail.png", "导航失败截图")
                return False
        
        print(f"✅ 已成功进入服务器页面: {page.url}")

        # --- 点击 "시간 추가" 按钮 ---
        try:
            # 尝试多种方式查找按钮
            btn=search_btn(page)

            if btn and btn.states.is_enabled:  # <--- 这里修改条件
                print(f"✅ 按钮已找到且可点击(enabled & displayed)")
                # 确保按钮可见
                try:
                    if not btn.states.is_displayed:
                        print("滚动到按钮位置...")
                        page.scroll.to_see(btn)
                        time.sleep(1)
                except:
                    pass
                
                # --- 处理 Turnstile 验证(最多重试 3 次)---
                max_attempts = 3
                res = False

                for attempt in range(1, max_attempts + 1):
                    print(f"\n🔄 [尝试 {attempt}/{max_attempts}]")
                    
                    # 重新点击按钮
                    try:
                        btn.click(by_js=False)
                        print("✅ 点击 '시간 추가' 按钮")
                    except Exception as e:
                        print(f"❌ 点击按钮失败: {type(e).__name__}: {str(e)[:100]}")
                        if attempt < max_attempts:
                            time.sleep(3)
                        continue
                    
                    # 等待页面加载
                    time.sleep(5)
                    
                    # 处理 Turnstile 验证
                    try:
                        res = solve_turnstile(page)
                        if res:
                            break
                        else:
                            print("⚠️ Turnstile 验证未通过(返回 False)")
                    except Exception as e:
                        print(f"❌ Turnstile 验证异常: {type(e).__name__}: {str(e)[:100]}")
                        res = False
                    
                    # 非最后一次尝试时等待后重试
                    if attempt < max_attempts and not res:
                        wait_sec = 3
                        print(f"⏳ 等待 {wait_sec} 秒后重试...")
                        time.sleep(wait_sec)
                    elif attempt == max_attempts:
                        error_msg = "❌ Turnstile 验证失败:已达到最大重试次数(3 次)"
                        print(error_msg)
                        send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}")

                # 检查是否成功
                time.sleep(5)
                success = check_action_success(page)
                
                capture_screenshot("button_click_result.png",page=page)
                
                # 发送通知
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                if success:
                    message = (
                        f"✅ <b>WeirdHost 续期成功</b>\n\n"
                        f"🕐 执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"⏱ 耗时: {duration:.1f} 秒\n"
                        f"🔗 服务器: {server_url}"
                    )
                    send_telegram_message(message)
                    send_telegram_photo("screenshots/button_click_result.png", "续期成功截图")
                else:
                    message = (
                        f"⚠️ <b>WeirdHost 续期完成(状态未确认)</b>\n\n"
                        f"🕐 执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"⏱ 耗时: {duration:.1f} 秒\n"
                        f"ℹ️ 按钮已点击,但未检测到明确的成功提示"
                    )
                    send_telegram_message(message)
                    send_telegram_photo("screenshots/button_click_result.png", "续期完成截图")
                
                return True
            elif btn:
                error_msg = "❌ 续期按钮不可点击,跳过此次操作(可能未到续期时间)"
                print(error_msg)
                send_telegram_message(f"⚠️ <b>WeirdHost 续期跳过</b>\n\n{error_msg}")
            else:
                error_msg = "❌ 未找到续期按钮"
                print(error_msg)
                print("当前页面标题:", page.title)
                print("当前页面URL:", page.url)
                
                # 保存页面截图和HTML帮助调试
                capture_screenshot("add_button_not_found.png",page=page)
                
                try:
                    html_content = page.html
                    # 保存部分HTML内容
                    with open("page_debug.html", "w", encoding="utf-8") as f:
                        f.write(html_content[:10000])
                    print("已保存页面HTML片段到 page_debug.html")
                    
                    # 打印页面上的所有按钮文本
                    print("页面上的按钮文本:")
                    all_buttons = page.eles('button, a.btn, [role="button"]')
                    for i, button in enumerate(all_buttons[:10]):  # 只显示前10个
                        try:
                            btn_text = button.text.strip()
                            if btn_text:
                                print(f"  {i+1}. '{btn_text}'")
                        except:
                            pass
                except Exception as e:
                    print(f"保存调试信息时出错: {e}")
                
                send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}\n当前页面: {page.url}")
                send_telegram_photo("screenshots/add_button_not_found.png", "未找到按钮截图")
                
                return False
                
        except Exception as e:
            error_msg = f"❌ 点击按钮过程中出错: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            capture_screenshot("button_click_error.png",page=page)
            send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}")
            send_telegram_photo("screenshots/button_click_error.png", "错误截图")
            return False

    except Exception as e:
        error_msg = f"❌ 执行过程中发生未知错误: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        if page:
            try:
                capture_screenshot("general_error.png",page=page)
                send_telegram_photo("screenshots/general_error.png", "未知错误截图")
            except:
                pass
        send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n{error_msg}")
        return False
    finally:
        global iargs
        if browser:
            if not iargs.keep:
                try:
                    print("正在关闭浏览器...")
                    browser.quit()
                    time.sleep(2)
                    print("✅ 浏览器已关闭")
                except Exception as e:
                    print(f"⚠️ 关闭浏览器时出错: {e}")

def main():
    global iargs
    """主函数,处理异常退出"""
    try:
        success = add_server_time()
        if success:
            print("✅ 任务执行成功。")
            if not iargs.keep:
                sys.exit(0)
        else:
            print("❌ 任务执行失败。")
            if not iargs.keep:
                sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
        send_telegram_message("⚠️ <b>WeirdHost 续期被中断</b>\n\n用户手动停止了任务")
        if not iargs.keep:
            sys.exit(130)
    except Exception as e:
        print(f"❌ 未捕获的异常: {e}")
        import traceback
        traceback.print_exc()
        send_telegram_message(f"🔴 <b>WeirdHost 续期失败</b>\n\n未捕获的异常: {e}")
        if not iargs.keep:
            sys.exit(1)

if __name__ == "__main__":
    if iargs.debug:
        test()
    else:
        main()
