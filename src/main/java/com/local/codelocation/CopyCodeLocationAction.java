package com.local.codelocation;

import com.intellij.codeInsight.hint.HintManager;
import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Caret;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.ide.CopyPasteManager;
import com.intellij.openapi.project.DumbAwareAction;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

import java.awt.datatransfer.StringSelection;

/**
 * 将代码文件绝对路径和选区行号复制到系统剪贴板。
 */
public final class CopyCodeLocationAction extends DumbAwareAction {

    @Override
    public @NotNull ActionUpdateThread getActionUpdateThread() {
        return ActionUpdateThread.BGT;
    }

    @Override
    public void update(@NotNull AnActionEvent event) {
        Project project = event.getProject();
        Editor editor = getHostEditor(event);
        VirtualFile file = getLocalFile(editor);
        event.getPresentation().setEnabledAndVisible(
                project != null && !project.isDisposed() && file != null);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent event) {
        Project project = event.getProject();
        Editor editor = getHostEditor(event);
        VirtualFile file = getLocalFile(editor);
        if (project == null || project.isDisposed() || editor == null || file == null) {
            return;
        }
        Caret caret = editor.getCaretModel().getPrimaryCaret();
        String content = LocationFormatter.format(
                file.getPath(), editor.getDocument(),
                caret.getSelectionStart(), caret.getSelectionEnd(), caret.getOffset());
        CopyPasteManager.getInstance().setContents(new StringSelection(content));
        HintManager.getInstance().showInformationHint(editor, "已复制代码绝对路径和行号");
    }

    /**
     * 注入语言编辑器使用宿主文件，确保路径与行号对应同一份源文件。
     */
    private static Editor getHostEditor(AnActionEvent event) {
        Editor editor = event.getData(CommonDataKeys.HOST_EDITOR);
        return editor != null ? editor : event.getData(CommonDataKeys.EDITOR);
    }

    /**
     * 仅处理有本地绝对路径的代码文件。
     */
    private static VirtualFile getLocalFile(Editor editor) {
        if (editor == null || editor.isDisposed()) {
            return null;
        }
        VirtualFile file = FileDocumentManager.getInstance().getFile(editor.getDocument());
        return file != null && file.isValid() && !file.isDirectory() && file.isInLocalFileSystem()
                ? file : null;
    }
}
