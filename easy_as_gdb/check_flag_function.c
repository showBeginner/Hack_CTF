
/* WARNING: Function: __i686.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

undefined4 FUN_000108c4(char *param_1,uint param_2)

{
  char *__dest;
  char *__dest_00;
  uint local_18;
  
  __dest = (char *)calloc(param_2 + 1,1);
  strncpy(__dest,param_1,param_2);
  FUN_000107c2(__dest,param_2,0xffffffff);
  __dest_00 = (char *)calloc(param_2 + 1,1);
  strncpy(__dest_00,&DAT_00012008,param_2);
  FUN_000107c2(__dest_00,param_2,0xffffffff);
  puts("checking solution...");
  local_18 = 0;
  while( true ) {
    if (param_2 <= local_18) {
      return 1;
    }
    if (__dest[local_18] != __dest_00[local_18]) break;
    local_18 = local_18 + 1;
  }
  return 0xffffffff;
}

