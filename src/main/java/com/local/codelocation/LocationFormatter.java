package com.local.codelocation;

import com.intellij.openapi.editor.Document;

/**
 * 生成可直接粘贴到聊天中的代码定位文本。
 */
final class LocationFormatter {

    /**
     * 行号从 1 开始，选区末端位于下一行开头时不包含该行。
     */
    static String format(String filePath, Document document,
                         int selectionStart, int selectionEnd, int caretOffset) {
        int startOffset = selectionStart < selectionEnd ? selectionStart : caretOffset;
        int lastOffset = selectionStart < selectionEnd ? selectionEnd - 1 : caretOffset;
        int firstLine = document.getLineNumber(startOffset) + 1;
        int lastLine = document.getLineNumber(lastOffset) + 1;
        String lineRange = firstLine == lastLine ? String.valueOf(firstLine) : firstLine + "-" + lastLine;

        return filePath + "#" + lineRange;
    }

    private LocationFormatter() {
    }
}
