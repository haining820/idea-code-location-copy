# idea-code-location-copy

在 IDEA 代码编辑器中右键选择 **复制代码定位**，复制单行纯文本到系统剪贴板，格式为 `代码绝对路径#行号`：

```text
/Users/example/IdeaProjects/demo/src/main/java/Foo.java#91-94
```

选中单行或未选中代码时，行号为单个数字。未选中代码时使用光标所在行。行号从 1 开始；选区结束在下一行开头时不会把下一行算进去。多光标或列选区使用主光标的选区。

代码绝对路径来自当前编辑器对应的本地文件。临时编辑器和 JAR 内的虚拟文件不显示该操作。未保存的修改按编辑器中的当前行号计算。

右键菜单使用 📝 图标，提供普通和 Retina 分辨率。

## 安装

1. 打开 IDEA 的 **Settings → Plugins**。
2. 点击齿轮，选择 **Install Plugin from Disk…**。
3. 选择 `idea-code-location-copy-1.0.5.zip`，不用解压。
4. 按 IDEA 提示重启或启用插件。
5. 在编辑器选中代码，右键点击 **复制代码定位**，再去聊天输入框粘贴。

插件名称是 **idea-code-location-copy**。“复制代码定位”显示在编辑器右键菜单最上方，macOS 快捷键为 **Option + Command + O（⌥⌘O）**。

IDEA 默认 macOS 键位中的“跳转到符号”（Go to Symbol）也使用 ⌥⌘O。使用默认键位时，请在 **Settings → Keymap** 解除该操作的同键绑定，并确认“复制代码定位”使用该快捷键。

插件 ID 已随名称更新，安装新版前请先卸载旧插件，避免出现重复菜单。

## 编译

仅使用本机 IDEA SDK 和 JDK，不需要下载 Gradle、Maven 或其他依赖。

```bash
python3 build.py \
  --idea-home '/Applications/IntelliJ IDEA 2026.app/Contents' \
  --jdk-home '/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home'
```

安装包默认生成到 `dist/idea-code-location-copy-1.0.5.zip`。可用 `--output` 和 `--build-dir` 指定输出位置。

最低平台版本为 261（IDEA 2026.1），字节码目标为 Java 21。使用本机 IDEA 2026.1（IU-261.22158.277）SDK 编译。其他 IDEA 版本未验证。

## 验证

已通过 SDK 编译、安装包 ZIP/JAR 结构及 Action 注册描述校验，并使用 IDEA 的真实 `DocumentImpl` 验证 9 个行号边界用例，包括单行、跨行、选区末端换行、空文件、文件末尾和中文内容。Action 类实例化及索引期间可用性检查通过。未进行 IDEA 界面中的安装与点击验证。

📝 图标的 16px 和 32px PNG 资源已校验，并通过 IDEA `IconLoader` 加载检查。
