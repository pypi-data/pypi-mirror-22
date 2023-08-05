# YARW: Yet Another Registry Wrapper

This recipe provides "Registry", a Windows registry wrapper class that makes
it easy to work with the Windows registry. The class works with an inner class
named "RegistryKey", which wraps up a Windows registry key and provides methods
to access and manipulate the key information. The class provides easy to 
remember substitutes for long method names of _winreg.


# Example


```python
key = Registry.open('HKEY_LOCAL_MACHINE', "SOFTWARE\\Python")
# Prints the RegistryKey instance
print key
# Prints the key name and the wrapped up PyHKEY instance
print key.getkeyname(), key.getkey()
corekey = key.openkey(1)

idx = 0
# Print the install path for Python 2.4 if installed.
while True:
    try:
        keyname = corekey.enumkey(idx)
        idx += 1
        if keyname == '2.4':
            keyVersion = corekey.openkey(idx)
            print keyVersion, keyVersion.getkeyname()
            keyPath = keyVersion.openkey(2)
            print keyPath, keyPath.getkeyname()
            print 'Install path is %s' % keyPath.getvalue()
            keyPath.close()
            keyVersion.close()
            break
    except RegistryError:
        break

corekey.close()
key.close()
```