
undefined8 valid_char(char param_1)

{
  undefined8 uVar1;
  
  if ((param_1 < '0') || ('9' < param_1)) {
    if ((param_1 < 'a') || ('f' < param_1)) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}

