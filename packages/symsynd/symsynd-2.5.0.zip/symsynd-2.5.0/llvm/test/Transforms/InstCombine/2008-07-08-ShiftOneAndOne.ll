; NOTE: Assertions have been autogenerated by utils/update_test_checks.py
; RUN: opt < %s -instcombine -S | FileCheck %s

define i1 @PR2330(i32 %a) {
; CHECK-LABEL: @PR2330(
; CHECK-NEXT:    [[TOBOOL:%.*]] = icmp ne i32 %a, 0
; CHECK-NEXT:    ret i1 [[TOBOOL]]
;
  %tmp15 = shl i32 1, %a
  %tmp237 = and i32 %tmp15, 1
  %toBool = icmp eq i32 %tmp237, 0
  ret i1 %toBool
}

