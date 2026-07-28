*** Begin Patch
*** Update File: jarvis-terminal/virtual_mouse/main.py
@@
-if __name__ == "__main__":
-    main()
+if __name__ == "__main__":
+    try:
+        main()
+    except Exception as e:
+        # Provide a helpful message; the run_vm wrapper will write full traceback
+        print("Virtual Mouse failed to start:", e)
+        raise
*** End Patch
