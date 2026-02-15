import os
import time
import re
import sys
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage import Chromium
import random
import argparse

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
    print("⚠️ 警告: 未找到浏览器可执行文件，将使用系统默认路径")
    binpath = None

parser = argparse.ArgumentParser(description="weridhost续期")
parser.add_argument('-k', '--keep', action='store_true', help='启用保留模式')
parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
iargs = parser.parse_args()

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
        print("⚠️ 按钮已点击，但未检测到明确的成功或错误提示。")

def capture_screenshot( file_name=None,save_dir='screenshots',page=None):
        os.makedirs(save_dir, exist_ok=True)
        if not file_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'screenshot_{timestamp}.png'
        full_path = os.path.join(save_dir, file_name)
        try:
            page.get_screenshot(path=save_dir, name=file_name, full_page=True)
            print(f"📸 截图已保存：{full_path}")
        except Exception as e:
            print(f"⚠️ 截图失败，未能成功保存。${e}")

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
    # global binpath
    # options = (
    #     ChromiumOptions()
    #     # .set_user_agent(user_agent)
    #     .set_argument('--guest')
    #     .set_argument('--no-sandbox')
    #     .set_argument('--disable-gpu')
    #     .set_argument('--window-size=1280,800')
    #     .set_argument('--disable-dev-shm-usage') 
    #     .set_argument(f'--user-data-dir={cwd}/.tmp')
    #     .set_argument('--disable-software-rasterizer')
    #     .set_browser_path(binpath)
    # )
    
    # # 设置代理
    # # if chrome_proxy:
    # #      options.set_argument(f'--proxy-server={chrome_proxy}')
    
    # # 设置无头模式
    # if 'DISPLAY' not in os.environ:
    #     options.headless(True)
    #     print("✅ DISPLAY环境变量为空，浏览器使用无头模式")
    # else:
    #     options.headless(False)
    #     print("✅ DISPLAY环境变量存在，浏览器使用正常模式")
    # browser = Chromium(options)
    # return browser
    try:
        if is_port_open():
            browser = Chromium(port)
            if browser.states.is_alive:
                print(f"✅ 成功接管浏览器（端口 {port}）")
                return browser
            print("❌ 接管失败，浏览器未响应")
        else:
            print(f"⚠️ 端口 {port} 未开放，跳过接管")
        return None
    except Exception as e:
        print(f"⚠️ 接管浏览器时出错：{e}")
        return None
def search_btn(page):
    add_button_txt = "시간추가"
    print(f"🔍 正在查找 '{add_button_txt}' 按钮...")
    
    # 等待按钮容器出现（确保页面完全加载）
    try:
        page.wait.ele_displayed('//div[contains(@class, "RenewBox2")]', timeout=10)
    except:
        print("⚠️  等待 RenewBox2 容器超时，继续尝试查找...")
    
    # 优先级排序：从最精准 → 最宽松
    selectors = [
        # 1. 【最佳】通过 color="primary" 属性定位（唯一标识）
        '//button[@color="primary"]',
        
        # 2. 通过 class 特征定位
        '//button[contains(@class, "Button__ButtonStyle-sc-1qu1gou-0")]',
        
        # 3. 通过父容器定位（RenewBox2 内的第一个button）
        '//div[contains(@class, "RenewBox2___StyledDiv")]/button[1]',
        
        # 4. 通过文本包含匹配（不依赖精确文本）
        f'//button[contains(@class, "Button__ButtonStyle") and contains(., "{add_button_txt}")]',
        
        # 5. 通过 span 的 class 定位
        '//span[contains(@class, "Button___StyledSpan-sc-1qu1gou-2")]/ancestor::button[1]',
        
        # 6. 通过索引定位（第5个button，根据调试信息）
        '(//button)[5]'
    ]
    
    for i, selector in enumerate(selectors, 1):
        try:
            btn = page.ele(selector, timeout=3)
            if btn and btn.tag == 'button':
                btn_text = btn.text.strip()
                btn_class = btn.attr('class') or ''
                btn_color = btn.attr('color') or ''
                
                # 验证：检查是否包含目标文本或正确的class/color
                if (add_button_txt in btn_text or 
                    'Button__ButtonStyle-sc-1qu1gou-0' in btn_class or 
                    btn_color == 'primary'):
                    print(f"✅ 找到按钮 (选择器#{i}): {selector[:60]}...")
                    print(f"   📌 class: {btn_class[:50]}")
                    print(f"   📌 color: {btn_color}")
                    print(f"   📌 文本: '{btn_text}'")
                    return btn
        except Exception as e:
            continue
    
    # 如果以上都失败，尝试遍历所有button手动查找
    print("\n🔄 尝试遍历所有按钮手动匹配...")
    try:
        all_btns = page.eles('tag:button')
        for idx, btn in enumerate(all_btns, 1):
            try:
                btn_text = btn.text.strip()
                btn_class = btn.attr('class') or ''
                btn_color = btn.attr('color') or ''
                
                # 匹配条件：包含目标文本 或 正确的class 或 color="primary"
                if (add_button_txt in btn_text or 
                    'Button__ButtonStyle-sc-1qu1gou-0' in btn_class or 
                    btn_color == 'primary'):
                    print(f"✅ 找到按钮 (遍历#{idx})")
                    print(f"   📌 class: {btn_class[:50]}")
                    print(f"   📌 color: {btn_color}")
                    print(f"   📌 text: '{btn_text}'")
                    return btn
            except:
                continue
    except Exception as e:
        print(f"❌ 遍历按钮失败: {e}")
    
    # 最终诊断
    print(f"\n❌ 未找到按钮 '{add_button_txt}'")
    return None

def test():
    browser = attach_browser()
    page = browser.latest_tab
    btn=search_btn(page)
    if not btn:
        print("查找失败")
    elif btn and btn.states.is_enabled: 
         print("查找成功，按钮可点击")
    else:
        print("查找成功")
    # capture_screenshot("test1111.png",page=page)
    # solve_turnstile2(page)
    # solve_turnstile(page)
    # check_action_success(page)
    
def is_valid_proxy(proxy: str) -> bool:
    """
    校验代理格式是否合法
    """
    if not proxy:
        return False
    pattern = re.compile(
        r'^(http|https|socks4|socks5)://'
        r'([a-zA-Z0-9.-]+|\d{1,3}(\.\d{1,3}){3})'
        r':(\d+)$'
    )
    return bool(pattern.match(proxy))

def add_server_time() -> bool:
    global binpath
    """
    使用 DrissionPage 登录 hub.weirdhost.xyz 并点击 "시간 추가" 按钮。
    """
    # 查找可用的 Chrome/Chromium 路径
    remember_web_cookie = os.environ.get('REMEMBER_WEB_COOKIE')
    pterodactyl_email = os.environ.get('PTERODACTYL_EMAIL')
    pterodactyl_password = os.environ.get('PTERODACTYL_PASSWORD')
    server_url = os.environ.get('WEIRDHOST_SERVER_URLS')
    chrome_proxy = os.environ.get("CHROME_PROXY")
    browser=None
    page=None
    if not (remember_web_cookie or (pterodactyl_email and pterodactyl_password)):
        print("❌ 错误: 缺少登录凭据。请设置 REMEMBER_WEB_COOKIE 或 PTERODACTYL_EMAIL 和 PTERODACTYL_PASSWORD 环境变量。")
        return False

    if chrome_proxy and not is_valid_proxy(chrome_proxy):
        print(f"❌ 错误: 代理格式不合法: {chrome_proxy}")
        return False

    if not server_url:
        print("❌ 错误: 未设置 WEIRDHOST_SERVER_URLS 环境变量")
        return False
    
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.7499.169 Safari/537.36"
    )

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
        print("✅ DISPLAY环境变量为空，浏览器使用无头模式")
    else:
        options.headless(False)
        print("✅ DISPLAY环境变量存在，浏览器使用正常模式")
    
    try:
        print("正在启动浏览器...")

        browser = Chromium(options)
        print("✅ 浏览器连接/启动成功")
        
        if browser is None:
            # 接管失败，启动新浏览器
            print("启动新的浏览器实例...")
            browser = Chromium(options)
            print("✅ 浏览器启动成功")
        else:
            print("✅ 已连接到现有浏览器")
        
        # 获取当前激活的标签页
        page = browser.latest_tab
        
        # 打印浏览器信息
        print(f"🌐 浏览器已准备就绪")
        # print(f"📡 代理设置: {chrome_proxy if chrome_proxy else '无'}")
        print(f"🖥️  显示模式: {'无头模式' if 'DISPLAY' not in os.environ else '正常模式'}")
        
        login_success = False

        # --- 使用 Cookie 登录 ---
        if remember_web_cookie:
            print("检测到 REMEMBER_WEB_COOKIE，尝试使用 Cookie 直接登录...")
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
                    print("❌ Cookie 登录失败，将尝试邮箱登录")
                    login_success = False
                    
            except Exception as e:
                print(f"Cookie 登录出错: {e}")
                login_success = False
        
        # --- 确保在正确的服务器页面 ---
        if not server_url in page.url:
            print(f"当前不在目标服务器页面，导航至: {server_url}")
            page.get(server_url)
            page.wait.load_start()
            time.sleep(3)
            
            if "login" in page.url.lower():
                print("❌ 导航失败，会话可能失效。")
                capture_screenshot("server_page_nav_fail.png",page=page)
                return False
        
        print(f"✅ 已成功进入服务器页面: {page.url}")

        # --- 点击 "시간 추가" 按钮 ---
        try:
            # 尝试多种方式查找按钮
            btn=search_btn(page)

            if btn and btn.states.is_enabled:  # <--- 这里修改条件
                print(f"✅ 按钮已找到且可点击（enabled & displayed）")
                # 确保按钮可见
                try:
                    if not btn.states.is_displayed:
                        print("滚动到按钮位置...")
                        page.scroll.to_see(btn)
                        time.sleep(1)
                except:
                    pass
                
                # --- 处理 Turnstile 验证（最多重试 3 次）---
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
                            print("⚠️ Turnstile 验证未通过（返回 False）")
                    except Exception as e:
                        print(f"❌ Turnstile 验证异常: {type(e).__name__}: {str(e)[:100]}")
                        res = False
                    
                    # 非最后一次尝试时等待后重试
                    if attempt < max_attempts and not res:
                        wait_sec = 3
                        print(f"⏳ 等待 {wait_sec} 秒后重试...")
                        time.sleep(wait_sec)
                    elif attempt == max_attempts:
                        print("❌ Turnstile 验证失败：已达到最大重试次数（3 次）")

                # 检查是否成功
                time.sleep(5)
                check_action_success(page)
                
                capture_screenshot("button_click_result.png",page=page)
                return True
            elif btn:
                print(f"❌ '{add_button_txt}' 按钮不可点击跳过此次操作")
            else:
                print(f"❌ 未找到 '{add_button_txt}' 按钮")
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
                
                return False
                
        except Exception as e:
            print(f"❌ 点击按钮过程中出错: {e}")
            import traceback
            traceback.print_exc()
            capture_screenshot("button_click_error.png",page=page)
            return False

    except Exception as e:
        print(f"❌ 执行过程中发生未知错误: {e}")
        import traceback
        traceback.print_exc()
        if page:
            try:
                capture_screenshot("general_error.png",page=page)
            except:
                pass
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
    """主函数，处理异常退出"""
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
        if not iargs.keep:
            sys.exit(130)
    except Exception as e:
        print(f"❌ 未捕获的异常: {e}")
        import traceback
        traceback.print_exc()
        if not iargs.keep:
            sys.exit(1)

if __name__ == "__main__":
    if iargs.debug:
        test()
    else:
        main()