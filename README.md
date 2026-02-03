# 错题整理软件 - Android应用

这是一个使用Kivy框架开发的错题整理Android应用。

## 项目结构

```
.
├── main.py                    # 主程序入口
├── database.py                # 数据库管理
├── main_screen.py            # 主界面
├── photo_screen.py           # 拍照界面
├── draft_screen.py           # 草稿界面
├── question_library_screen.py # 错题库界面
├── question_edit_screen.py   # 错题编辑界面
├── paper_edit_screen.py      # 试卷编辑界面
├── paper_library_screen.py   # 试卷库界面
├── import_export.py          # 导入导出功能
├── print_service.py          # 打印服务
├── utils.py                  # 工具函数
├── requirements.txt          # Python依赖
├── buildozer.spec            # Buildozer配置文件
├── buildozer-simple.spec     # 简化版Buildozer配置
├── .github/workflows/        # GitHub Actions配置
│   ├── build-apk.yml         # 完整构建配置
│   └── build-apk-simple.yml  # 简化构建配置
```

## 依赖说明

### Python依赖
- `kivy==2.3.0` - GUI框架
- `pillow==10.3.0` - 图像处理
- `fpdf2==2.7.6` - PDF生成
- `pyjnius==1.6.1` - Java Native Interface
- `plyer==2.1.0` - 平台特定功能
- `cython==0.29.33` - C扩展编译器
- `pyopenssl==23.2.0` - SSL支持

## 构建APK

### 方法1：使用简化配置（推荐）
1. 重命名文件：
   ```bash
   mv buildozer-simple.spec buildozer.spec
   mv .github/workflows/build-apk-simple.yml .github/workflows/build-apk.yml
   ```

2. 提交到GitHub，GitHub Actions会自动构建

### 方法2：本地构建
1. 安装Buildozer：
   ```bash
   pip install buildozer==1.5.0 python-for-android==2024.1.21 Cython==0.29.33
   ```

2. 安装系统依赖：
   ```bash
   sudo apt-get install -y build-essential git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good autoconf libtool pkg-config libncurses5-dev libncursesw5-dev libtinfo-dev cmake libffi-dev libssl-dev automake zip unzip openjdk-17-jdk python3-dev libjpeg-dev libpng-dev libfreetype6-dev libsqlite3-dev libbz2-dev libxml2-dev liblzma-dev m4 bison flex gperf lld clang libc++-dev libc++abi-dev libtool-bin
   ```

3. 构建APK：
   ```bash
   buildozer android debug
   ```

## GitHub Actions配置

### 完整配置 (`build-apk.yml`)
- 使用Python 3.12
- 最新版本的依赖
- 包含libffi修复

### 简化配置 (`build-apk-simple.yml`)
- 使用Python 3.10（更稳定）
- 固定版本的依赖
- 预下载Android SDK
- 自动接受许可协议

## 常见问题

### 1. libffi构建失败
错误信息：
```
configure.ac:418: You should run autoupdate.
LT_SYS_SYMBOL_USCORE is expanded from...
autoreconf: error: /usr/bin/autoconf failed
```

**解决方案**：
- 使用简化配置（`buildozer-simple.spec`）
- 使用固定版本的依赖
- 预下载Android SDK

### 2. 构建时间过长
**解决方案**：
- 只构建arm64-v8a架构
- 使用GitHub Actions缓存
- 预下载Android SDK

### 3. 权限问题
确保在`buildozer.spec`中正确配置权限：
```ini
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.features = android.hardware.camera
```

## 应用功能

1. **拍照录入** - 拍摄错题照片
2. **错题管理** - 分类整理错题
3. **试卷生成** - 创建错题试卷
4. **导出功能** - 导出为PDF格式
5. **数据备份** - 导入导出数据

## 技术支持

如果遇到构建问题，请：
1. 查看GitHub Actions日志
2. 使用简化配置
3. 检查依赖版本兼容性
