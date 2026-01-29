@echo off
echo ========================================
echo 添加 Android SDK 许可协议步骤
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
git commit -m "Fix: Add Android SDK license acceptance step

- Added 'Accept Android SDK Licenses' step before build
- Automatically accepts Android SDK licenses by creating license files
- Allows Buildozer to download Build-Tools 36.1 and other components
- Without this step, build appears successful but no APK is generated
- License hashes:
  - android-sdk-license: 89316a2ffe0e01b6d91f2f87be9676f5e584ddc6
  - android-sdk-license: 24333f8a63b6825ea9c5514f83c2829b004d1fee
  - android-sdk-preview-license: d56f5187479451eabf01fb78af6dfcb131a6481e"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: add_sdk_license.bat ^<仓库URL^>
    echo.
    echo 示例: add_sdk_license.bat https://github.com/username/repository.git
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
echo [成功] 许可协议步骤已添加！
echo ========================================
echo.
echo 添加内容：
echo - 在构建前自动接受 Android SDK 许可协议
echo - 允许下载 Build-Tools 36.1 等必要组件
echo - 解决了"伪成功"问题（显示成功但无 APK）
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 这次应该能够成功下载所有必要的工具
echo.
echo 3. 构建完成后，查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 4. 在 Artifacts 部分下载 APK
echo.
pause
