@echo off
echo ========================================
echo 提交构建修复
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加所有修复的文件...
git add .

echo.
echo 创建提交...
git commit -m "Fix: Remove unavailable libtinfo5 package and improve build logging

- Replaced libtinfo5 with libtinfo-dev (available in newer Ubuntu)
- Removed unnecessary packages that may cause conflicts
- Added detailed build logging and error handling
- Added APK verification step after build
- Simplified buildozer.spec configuration
- Improved error messages for troubleshooting"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: submit_fix.bat ^<仓库URL^>
    echo.
    echo 示例: submit_fix.bat https://github.com/username/repository.git
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
echo [成功] 修复已推送！
echo ========================================
echo.
echo 修复内容：
echo - 修复了 libtinfo5 包不存在的问题
echo - 添加了详细的构建日志
echo - 改进了错误处理
echo - 添加了 APK 验证步骤
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 查看构建日志以确认修复是否成功
echo.
echo 3. 如果构建成功，在 Artifacts 部分下载 APK
echo.
pause
