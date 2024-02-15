
undefined8 main(int param_1,undefined8 *param_2)
{
  byte bVar1;
  char cVar2;
  int iVar3;
  undefined8 uVar4;
  long in_FS_OFFSET;
  int local_f0;
  int i;
  char user_input [100];
  undefined local_84;
  char encrypt_user_input [104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (param_1 < 2) {
    printf("USAGE: %s [KEY]\n",(char *)*param_2);
    uVar4 = 1;
  }
  else {
    strncpy(user_input,(char *)param_2[1],100);
    local_84 = 0;
    local_f0 = 0;
    while( true ) {
      uVar4 = valid_char(user_input[local_f0]);
      if ((int)uVar4 == 0) break;
      if (local_f0 == 0) {
        cVar2 = jumble(user_input[0]);
        encrypt_user_input[0] = cVar2 % '\x10';
      }
      else {
        cVar2 = jumble(user_input[local_f0]);
        bVar1 = (byte)((int)cVar2 + (int)encrypt_user_input[local_f0 + -1] >> 0x1f);
        encrypt_user_input[local_f0] =
             ((char)((int)cVar2 + (int)encrypt_user_input[local_f0 + -1]) + (bVar1 >> 4) & 0xf) -
             (bVar1 >> 4);
      }
      local_f0 = local_f0 + 1;
    }
    for (i = 0; i < local_f0; i = i + 1) {
      encrypt_user_input[i] = encrypt_user_input[i] + 'a';
    }
    if (local_f0 == 100) {
      iVar3 = strncmp(encrypt_user_input,
                      "mlaebfkoibhoijfidblechbggcgldicegjbkcmolhdjihgmmieabohpdhjnciacbjjcnpcfaopigkpdfnoaknjlnlaohboimombk"
                      ,100);
      if (iVar3 == 0) {
        puts("You got the key, congrats! Now xor it with the flag!");
        uVar4 = 0;
        goto LAB_001009ea;
      }
    }
    puts("Invalid key!");
    uVar4 = 1;
  }
LAB_001009ea:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar4;
}

