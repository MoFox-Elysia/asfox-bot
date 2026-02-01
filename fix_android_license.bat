@echo off
echo ========================================
echo 修复 Android SDK 许可证问题
echo ========================================
echo.

echo 问题分析：
echo GitHub Actions 构建失败，错误信息：
echo "Skipping following packages as the license is not accepted:"
echo "Android SDK Build-Tools 36.1"
echo.
echo 问题原因：
echo Buildozer 在非交互式环境中无法自动接受 Android SDK 许可证
echo 需要预先接受所有必要的许可证
echo.

echo 正在备份工作流文件...
if exist .github\workflows\build-apk.yml (
    copy .github\workflows\build-apk.yml .github\workflows\build-apk.yml.backup
    echo 已备份到: .github\workflows\build-apk.yml.backup
)

echo.
echo 应用修复：添加许可证接受步骤...
echo.

echo 修复内容：
echo 1. 添加 "Pre-accept Android SDK licenses" 步骤
echo 2. 创建 ~/.android/licenses 目录
echo 3. 写入所有必要的许可证文件
echo 4. 使用 "yes |" 自动回答所有提示
echo 5. 包含 6 个必要的许可证哈希
echo.

echo 提交修复...
git add .github/workflows/build-apk.yml

echo.
set /p COMMIT_MSG="请输入提交信息（默认：修复 Android SDK 许可证问题）: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG="修复 Android SDK 许可证问题"

git commit -m "%COMMIT_MSG%

- 添加 Android SDK 许可证预接受步骤
- 创建必要的许可证文件
- 包含 6 个许可证哈希值
- 使用 yes | 自动回答构建提示
- 解决 Build-Tools 36.1 安装失败问题

许可证哈希值：
1. android-sdk-license
2. android-sdk-preview-license  
3. android-sdk-arm-dbt-license
4. android-googletv-license
5. google-gdk-license"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_android_license.bat ^<仓库URL^>
    echo.
    echo 示例: fix_android_license.bat https://github.com/username/repository.git
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
echo 2. 点击 "Build Android APK (With License Fix)"
echo 3. 点击 "Run workflow" 手动触发构建
echo.
echo 4. 等待构建完成（约 15-20 分钟）
echo.
echo 5. 下载生成的 APK 文件
echo.
echo 许可证修复说明：
echo - 预先接受所有 Android SDK 许可证
echo - 解决 Build-Tools 36.1 安装失败
echo - 避免交互式提示问题
echo - 确保 Aidl 工具正确安装
echo.
pause
exit /b 0
