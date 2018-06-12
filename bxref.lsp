(vl-load-com)
;;;�����
(defun c:rbxref()(command "-xref" "R" "*")(command "-xref" "B" "*"))
(defun c:rxref()(command "-xref" "R" "*"))
(defun c:bxref()(command "-xref" "B" "*"))
(defun c:sbxref() (xref-super-bind))
(defun c:afile()(setq file (getstring "��������Ҫ�޸����ļ�·����")) (auditfile file))
(defun c:superclean() (superclean))

;;;����
(setq empty_file "D:\\AcsModule\\Client\\EmptyDwg.dwg")

(defun auditfile (file);�޸�file���ļ����󲢱���
  (setq dwgobj (vla-open (vla-get-documents(vlax-get-acad-object)) file))
  (vla-AuditInfo dwgobj T)
  (vlax-invoke-method dwgobj 'Save)
  (vla-close dwgobj)
)
(defun purge_file (file);�����ļ�
  (setq dwgobj (vla-open (vla-get-documents(vlax-get-acad-object)) file))
  (vla-purgeall dwgobj)
  (vlax-invoke-method dwgobj 'Save)
  (vla-close dwgobj)
)
(defun superclean() ;PURGE��DGN
  (dictremove(namedobjdict)"ACAD_DGNLINESTYLECOMP")(command "-purge" "a" "*" "n")
nil)
(defun get-blocks (/ lst a);�г����п�����;list all blocks
  (SETQ LST (LIST  (tblnext "block" t))) (while (setq a (tblnext "block")) (setq lst (cons a lst))) 
lst)

;�г�δ���ص����
(defun xref-unload-list ()(setq lst nil)(foreach item (get-blocks) (if (= 4 (cdaddr item)) (setq lst(cons item lst))))lst)

(defun xref-super-bind();��������
  (superclean)
  (foreach xref (xref-unload-list) ;�޸�ж�صĵ����ļ�
    (setq block_name (cdadr xref))
    (command "-xref" "p" block_name empty_file)
  );end foreach
  (command "-xref" "r" "*")
  (foreach xref (xref-unload-list);����δ����
    (setq xref_name (cdadr xref))
    (command "-xref" "d" xref_name)
  );end foreach
  (command "-xref" "b" "*")
  (superclean)
  (command "qsave")
nil
);end defun