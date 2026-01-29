@echo off
echo ========================================
echo 安装兼容的 Libtool 2.4.6
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加修复的文件...
git add .github/workflows/build-apk.yml

echo.
echo 创建提交...
git commit -m "Fix: Install Libtool 2.4.6 for Buildozer compatibility

- Added 'Install Libtool 2.4.6' step before build
- Downloads and compiles Libtool 2.4.6 from source
- This fixes the ltmain.sh path issue in Libtool 2.4.7
- Ubuntu 22.04 ships with Libtool 2.4.7 which has incompatible paths
- Buildozer/p4a works best with Libtool 2.4.6
- Updated libtool macros fix step to work with 2.4.6
- This should resolve libffi compilation failures"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: install_libtool_246.bat ^<仓库URL^>
    echo.
    echo 示例: install_libtool_246.bat https://github.com/username/repository.git
    echo.
    pause
    exit /b 1
)

set REPO_URL=%1

echo 设置远程仓库...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo 远程仓库已存在，更新 URL...
    git remote set-url origin %REPO_URL%
)

echo.
echo 推送代码到 GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo [错误] 推送失败！
    echo ========================================
    echo.
    echo 如果遇到身份验证问题，请：
    echo 1. 创建 GitHub Personal Access Token
    echo    访问: https://github.com/settings/tokens
    echo 2. 使用以下命令手动推送：
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [成功] Libtool 2.4.6 修复已推送！
echo ========================================
echo.
echo 修复内容：
echo - 从源码编译并安装 Libtool 2.4.6
echo - 解决了 Libtool 2.4.7 的路径兼容性问题
echo - 修复了 ltmain.sh 找不到的错误
echo - 修复了 libffi 编译失败问题
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 查看 "Install Libtool 2.4.6" 步骤
echo    确认安装成功
echo.
echo 3. 查看 "Build APK with Buildozer" 步骤
echo    应该能够成功编译 libffi
echo.
echo 4. 查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 5. 在 Artifacts 部分下载 APK
echo.
pause
