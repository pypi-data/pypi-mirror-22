; NOTE: Assertions have been autogenerated by utils/update_llc_test_checks.py
; RUN: llc < %s -mtriple=i386-apple-darwin8 -mattr=+sse2 | FileCheck %s --check-prefix=X32
; RUN: llc < %s -mtriple=x86_64-apple-darwin8 -mattr=+sse2 | FileCheck %s --check-prefix=X64
; rdar://6034396

define void @test(i32 %x, float* %y) nounwind {
; X32-LABEL: test:
; X32:       ## BB#0: ## %entry
; X32-NEXT:    movl {{[0-9]+}}(%esp), %eax
; X32-NEXT:    movl {{[0-9]+}}(%esp), %ecx
; X32-NEXT:    shrl $23, %ecx
; X32-NEXT:    cvtsi2ssl %ecx, %xmm0
; X32-NEXT:    movss %xmm0, (%eax)
; X32-NEXT:    retl
;
; X64-LABEL: test:
; X64:       ## BB#0: ## %entry
; X64-NEXT:    shrl $23, %edi
; X64-NEXT:    cvtsi2ssl %edi, %xmm0
; X64-NEXT:    movss %xmm0, (%rsi)
; X64-NEXT:    retq
entry:
  lshr i32 %x, 23
  uitofp i32 %0 to float
  store float %1, float* %y
  ret void
}
