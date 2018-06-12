(vl-load-com)
;;;命令定义
(defun c:rbxref()(command "-xref" "R" "*")(command "-xref" "B" "*"))
(defun c:rxref()(command "-xref" "R" "*"))
(defun c:bxref()(command "-xref" "B" "*"))
(defun c:sbxref() (xref-super-bind))
(defun c:afile()(setq file (getstring "请输入需要修复的文件路径：")) (auditfile file))
(defun c:superclean() (superclean))

;;;变量
(setq empty_file "D:\\AcsModule\\Client\\EmptyDwg.dwg")

(defun auditfile (file);修复file的文件错误并保存
  (setq dwgobj (vla-open (vla-get-documents(vlax-get-acad-object)) file))
  (vla-AuditInfo dwgobj T)
  (vlax-invoke-method dwgobj 'Save)
  (vla-close dwgobj)
)
(defun purge_file (file);清理文件
  (setq dwgobj (vla-open (vla-get-documents(vlax-get-acad-object)) file))
  (vla-purgeall dwgobj)
  (vlax-invoke-method dwgobj 'Save)
  (vla-close dwgobj)
)
(defun superclean() ;PURGE和DGN
  (dictremove(namedobjdict)"ACAD_DGNLINESTYLECOMP")(command "-purge" "a" "*" "n")
nil)
(defun get-blocks (/ lst a);列出所有块和外参;list all blocks
  (SETQ LST (LIST  (tblnext "block" t))) (while (setq a (tblnext "block")) (setq lst (cons a lst))) 
lst)

;列出未加载的外参
(defun xref-unload-list ()(setq lst nil)(foreach item (get-blocks) (if (= 4 (cdaddr item)) (setq lst(cons item lst))))lst)

(defun xref-super-bind();绑定清理保存
  (superclean)
  (foreach xref (xref-unload-list) ;修改卸载的到空文件
    (setq block_name (cdadr xref))
    (command "-xref" "p" block_name empty_file)
  );end foreach
  (command "-xref" "r" "*")
  (foreach xref (xref-unload-list);拆离未参照
    (setq xref_name (cdadr xref))
    (command "-xref" "d" xref_name)
  );end foreach
  (command "-xref" "b" "*")
  (superclean)
  (command "qsave")
nil
);end defun