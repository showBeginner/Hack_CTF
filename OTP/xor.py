def str_xor_str(flag:str, key:str):
    flag_bytes = bytes.fromhex(flag)
    key_bytes = bytes.fromhex(key)
    result = ''.join([chr(x ^ y) for x,y in zip(flag_bytes, key_bytes)])
    return result

print(
    str_xor_str(
        "1fcb81cd1f6f1e12b429092e3647153b6c212772554ca004145b82367e1e6b7870827dc249a319601776f727434e6b6227d1",
        "6fa2e2a25c3b5869d75c7a5a062a4a51194c451e663fff306668ec42212a341f40cd199d78c72a21481596117a7c5e5217ac",
    )
)
