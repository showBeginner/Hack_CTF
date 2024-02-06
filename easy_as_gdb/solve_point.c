
/* WARNING: Function: __i686.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_000109af(void)

{
  char *__s;
  size_t sVar1;
  undefined4 uVar2;
  int iVar3;
  
  __s = (char *)calloc(0x200,1);
  printf("input the flag: ");
  fgets(__s,0x200,_stdin);
  sVar1 = strnlen(&DAT_00012008,0x200);
  uVar2 = FUN_0001082b(__s,sVar1);
  FUN_000107c2(uVar2,sVar1,1);
  iVar3 = FUN_000108c4(uVar2,sVar1);
  if (iVar3 == 1) {
    puts("Correct!");
  }
  else {
    puts("Incorrect.");
  }
  return 0;
}

