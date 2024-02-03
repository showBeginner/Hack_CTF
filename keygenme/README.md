# keygenme-py
**Tag:** picoCTF 2021, Reverse Engineer
## Question:
_Author: syreal_
### Description
Give keygenme-trial.py to capture flag.

## Analysis

### **Original:**
#### Program hava a menu function:
(a) Estimate Astral Projection Mana Burn:  estimate_burn()\
(b) [LOCKED] Estimate Astral Slingshot Approach Vector locked_estimate_vector()\
(c) Enter License Key `enter_license()` ----> This is our focus function \
(d) Exit Arcane Calculator\

The function `enter_license` \
global variable: `bUsername_trial = b"GOUGH"`
and `check_key()` is our keypoint.
```python
def enter_license():
    user_key = input("\nEnter your license key: ")
    user_key = user_key.strip()

    global bUsername_trial
    
    if check_key(user_key, bUsername_trial):
        decrypt_full_version(user_key)
    else:
        print("\nKey is NOT VALID. Check your data entry.\n\n")
```
In the function `check_key()`,
1. It is compare `len(user_input)` with `global key_full_template_trial`
```python
key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
```
2. It will check `key_part_static1_trial`.
3. it will check `key[i]` with `hashlib.sha256(username_trial).hexdigest()`

## Resolve
1. Insert as below code:
```python
print("key len:", len(key_full_template_trial))
test_key = hashlib.sha256(bUsername_trial).hexdigest()
index = [4, 5, 3, 6, 2, 7, 1, 8] #This index is follow original code.
real_key = ""
for i in index:
   real_key += test_key[i]
real_key = key_part_static1_trial + real_key + key_part_static2_trial
print("Key: ", real_key)
```
2. Modify `enter_license()` to use our insert global variable `real_key`
```python
def enter_license():
    #user_key = input("\nEnter your license key: ")
    #user_key = user_key.strip()

    global bUsername_trial
    # Hack enter
    global real_key
    if check_key(real_key, bUsername_trial):
        decrypt_full_version(real_key)
    else:
        print("\nKey is NOT VALID. Check your data entry.\n\n")
```
3. Execute new python and we will capture the flag.
```
key len: 32
Key:  picoCTF{1n_7h3_|<3y_of_f911a486}
```