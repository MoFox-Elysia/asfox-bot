@echo off
echo ========================================
echo 测试构建配置
echo ========================================
echo.

echo 1. 检查关键文件...
if exist main.py (
    echo ✅ main.py 存在
) else (
    echo ❌ main.py 不存在
)

if exist buildozer.spec (
    echo ✅ buildozer.spec 存在
) else (
    echo ❌ buildozer.spec 不存在
)

if exist requirements.txt (
    echo ✅ requirements.txt 存在
) else (
    echo ❌ requirements.txt 不存在
)

if exist .github\workflows\build-apk.yml (
    echo ✅ GitHub Actions 工作流存在
) else (
    echo ❌ GitHub Actions 工作流不存在
)

echo.
echo 2. 检查 Python 依赖...
python -c "import kivy; print('✅ Kivy 版本:', kivy.__version__)" 2>nul
if errorlevel 1 echo ❌ Kivy 未安装

python -c "import Cython; print('✅ Cython 版本:', Cython.__version__)" 2>nul
if errorlevel 1 echo ❌ Cython 未安装

echo.
echo 3. 检查构建配置...
findstr /i "title=" buildozer.spec
findstr /i "package.name=" buildozer.spec
findstr /i "requirements=" buildozer.spec

echo.
echo 4. 检查 GitHub Actions 配置...
type .github\workflows\build-apk.yml | findstr /i "cython" >nul
if errorlevel 1 (
    echo ❌ GitHub Actions 中未找到 Cython 安装
) else (
    echo ✅ GitHub Actions 包含 Cython 安装
)

echo.
echo ========================================
echo 测试完成
echo ========================================
echo.
echo 建议：
echo 1. 如果所有检查都通过，可以尝试构建
echo 2. 如果有 ❌ 标记的问题，请先修复
echo 3. 使用 fix_cython_issue.bat 修复常见问题
echo.
pause
