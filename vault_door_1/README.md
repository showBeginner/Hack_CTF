# vault-door-1
**Tag:** picoCTF 2019, Reverse Engineer
## Question:
_Author: Mark E. Haase_
### Description
This vault uses some complicated arrays! I hope you can make sense of it, special agent. The source code for this vault is here: `VaultDoor1.java`
## Analysis
Found the the function `checkPassword()` to check password.\
It tell us that `password.length() == 32` and `password.charAt(0)  == 'd'`..... etc so we can write the function to given a correct password to new string.
## Resolve
```java
public static  String hackPassword() {
	char[] password = new char[32];
	password[0] = 'd'; 
	password[29] = '3'; 
	password[4] = 'r'; 
	password[2] = '5'; 
	password[23] = 'r'; 
	password[3] = 'c'; 
	password[17] = '4'; 
	password[1] = '3'; 
	password[7] = 'b'; 
	password[10] = '_'; 
	password[5] = '4'; 
	password[9] = '3'; 
	password[11] = 't'; 
	password[15] = 'c'; 
	password[8] = 'l'; 
	password[12] = 'H'; 
	password[20] = 'c'; 
	password[14] = '_'; 
	password[6] = 'm'; 
	password[24] = '5'; 
	password[18] = 'r'; 
	password[13] = '3'; 
	password[19] = '4'; 
	password[21] = 'T'; 
	password[16] = 'H'; 
	password[27] = 'f'; 
	password[30] = 'b'; 
	password[25] = '_'; 
	password[22] = '3'; 
	password[28] = '6'; 
	password[26] = 'f'; 
	password[31] = '0';
	
	return new String(password);
}
```
Now, we only need to compile java code and execute program, will capture the flag.
```
password: d35cr4mbl3_tH3_cH4r4cT3r5_ff63b0
Access granted.
Flag: picoCTF{d35cr4mbl3_tH3_cH4r4cT3r5_ff63b0}
```