@echo off
echo ========================================
echo 修复 Android NDK 移动错误
echo ========================================
echo.

echo 问题分析：
echo GitHub Actions 构建失败，错误信息：
echo "mv: cannot move 'android-ndk-r25b' to a subdirectory of itself"
echo.
echo 问题原因：
echo 工作流中有一行错误的代码：
echo   mv android-ndk-r25b android-ndk-r25b
echo 这行代码试图将目录移动到自身，这是不可能的。
echo.

echo 正在备份工作流文件...
if exist .github\workflows\build-apk.yml (
    copy .github\workflows\build-apk.yml .github\workflows\build-apk.yml.backup
    echo 已备份到: .github\workflows\build-apk.yml.backup
)

echo.
echo 应用修复：删除错误的 mv 命令...
echo.

echo 修复内容：
echo 1. 删除错误的 "mv android-ndk-r25b android-ndk-r25b" 命令
echo 2. 解压后 NDK 目录已经存在，不需要移动
echo 3. 保持其他配置不变
echo.

echo 提交修复...
git add .github/workflows/build-apk.yml

echo.
set /p COMMIT_MSG="请输入提交信息（默认：修复 Android NDK 移动错误）: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG="修复 Android NDK 移动错误"

git commit -m "%COMMIT_MSG%

- 修复 NDK 解压后的移动错误
- 删除错误的 mv 命令
- 解压后目录已存在，无需移动
- 保持构建流程不变"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_ndk_error.bat ^<仓库URL^>
    echo.
    echo 示例: fix_ndk_error.bat https://github.com/username/repository.git
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
echo 下一步操作：
echo 1. 访问 GitHub Actions 页面：
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 点击 "Build Android APK (Fixed)"
echo 3. 点击 "Run workflow" 手动触发构建
echo.
echo 4. 等待构建完成（约 15-20 分钟）
echo.
echo 5. 下载生成的 APK 文件
echo.
pause
exit /b 0
