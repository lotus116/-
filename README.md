# 校园网自动登录重连脚本

这个脚本用于解决校园网定时掉线问题，通过一个后台脚本实现全自动静默登录。

## 完整操作流程

### 步骤一：环境准备

1.  **安装 Python**：确保你的电脑已安装 Python (例如 3.10+)。
2.  **安装依赖库**：打开“命令提示符 (CMD)”，运行以下两条命令来安装必需的库：
    ```bash
    pip install requests
    pip install selenium
    ```
3.  **（重要）禁用 Windows 应用别名**：
      * 在 Windows 开始菜单搜索“**管理应用执行别名**”。
      * 打开它，在列表里找到 `python.exe` 和 `python3.exe`。
      * **把这两个开关都拨到“关”**。

### 步骤二：准备文件

1.  **创建文件夹**：在你的电脑上创建一个**纯英文路径**的文件夹，例如：`C:\AutoLogin`
2.  **下载驱动**：
      * 打开 Edge 浏览器，在地址栏输入 `edge://version` 查看你的版本号。
      * 访问 [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
      * 下载与你 Edge 版本**完全匹配**的 `win64` 驱动。
3.  **放置文件**：
      * 将 `auto_login.py` (主脚本) 和 `start_login.bat` (启动器) 放入 `C:\AutoLogin` 文件夹。
      * 解压你刚下载的驱动，把 `msedgedriver.exe` 文件也放入 `C:\AutoLogin` 文件夹。
      * **此时，你的 `C:\AutoLogin` 文件夹内应有 3 个文件。**

### 步骤三：修改配置

1.  **（重要）修改密码**：

      * 用记事本或代码编辑器打开 `auto_login.py`。
      * 找到 `USER_ACCOUNT` 和 `USER_PASSWORD` 变量，**填入你自己的校园网账号和密码**。

2.  **修改启动器 (`start_login.bat`)**：

      * 右键 `start_login.bat` -\> **编辑**。
      * 这个脚本里有**两个**需要你检查并修改的**绝对路径**：

    <!-- end list -->

    ```batch
    START "AutoLogin" /B "C:\Path\To\Your\python.exe" -u "C:\AutoLogin\auto_login.py" >> login_log.txt 2>>&1
    ```

      * **路径 1 (`python.exe`)**：
          * 在 CMD 中运行 `where python` 找到你的 `python.exe` 绝对路径 (例如 `C:\Users\cclear116\AppData\Local\Programs\Python\Python310\python.exe`)。
          * 用这个路径替换掉 `.bat` 文件中的 `"C:\Path\To\Your\python.exe"`。
      * **路径 2 (`auto_login.py`)**：
          * 确保这个路径指向你步骤二中创建的 `.py` 文件 (例如 `"C:\AutoLogin\auto_login.py"`)。

### 步骤四：设置开机自启（隐藏后台运行）

这是让脚本“精简自动”的最后一步。

1.  按 `Win + R` 键，输入 `taskschd.msc`，打开“**任务计划程序**”。

2.  在右侧点击“**创建任务...**”。

3.  **【常规】选项卡**：

      * 名称：`AutoCampusLogin` (可以随便起名)
      * 勾选 "**无论用户是否登录都运行**" (**实现后台静默运行的关键**)
      * 勾选 "**使用最高权限运行**"

4.  **【触发器】选项卡**：

      * 点击 "新建..." -\> "开始任务：" 选择 "**登录时**"。
      * (推荐) 勾选“延迟任务” 1 分钟。

5.  **【操作】选项卡**：

      * 点击 "新建..." -\> "程序/脚本："
      * 点击“浏览...”，选择你的 `start_login.bat` 启动文件 (例如 `C:\AutoLogin\start_login.bat`)。

6.  **【条件】选项卡**：

      * **取消勾选** “仅在计算机使用交流电源时才启动” (如果是笔记本)。

7.  **保存**：

      * 点击“确定”保存任务。
      * 系统会提示你**输入你当前电脑的开机密码**以授权后台运行。

### 步骤五：验证

1.  **重启电脑**。
2.  登录 Windows 一分钟后，脚本会自动在后台运行（**不会有任何弹窗**）。
3.  你可以打开 `C:\AutoLogin\login_log.txt` 文件，查看 `登录成功！网络已连接。` 等日志来确认脚本是否在正常工作。

**如何停止**：打开“任务计划程序”，找到你的 `AutoCampusLogin` 任务，右键 -\> **禁用** 或 **结束**。
