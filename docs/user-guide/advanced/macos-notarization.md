# macOS Notarization

Sign and notarize your app on macOS.

---

Applications on macOS need to be notarized by Apple in order to run on other
macOS devices without warning. This is accomplished by code signing the
app bundle generated by PyInstaller, submitting the file to Apple, then
stapling a notarization ticket to the app bundle.

## Requirements

Code signing an app bundle requires an active Apple Developer account. You will
need to create a Developer ID certificate for signing applications. Follow the
[instructions on the Apple Developer support page](https://developer.apple.com/help/account/create-certificates/create-developer-id-certificates)
to create a Developer ID certificate.

You will need to install Xcode 13 or later to gain access to the `xcrun`
command, which PyDeployment uses during the notarization process. You may need to
use the `xcode-select` utility to choose an appropriate version of Xcode.

```
sudo xcode-select -s /path/to/Xcode13.app
```
## Code Sign

To code sign the app bundle generated by PyInstaller, include the Common Name
of your Developer ID certificate in your build options. This can be included as
`CERT` in the environment file or by using `-C`, `--cert`, or `--certificate`
to include the value as a command line argument. For example, the following
command will code sign the application generated by `myapp.spec` with the
specified Developer ID certificate.

```
pydeploy myapp.spec -C 'Developer ID Application: Name Here (TEAMIDHERE)'
```

Note that this application will still need to be submitted for notarization
separately.

## Notarize With a Stored Keychain Profile

If you wish to both sign and notarize your application, you have two options
for information to include.

| Option 1 | Option 2 |
| :--      | :--      |
| Name of a stored Keychain Profile | Apple ID, Team ID, and an App-Specific Password |

You will want to create an App Store Connect API key and save it locally on
your device. Then run the following command to store the Keychain Profile with
the name of your choice.

```
xcrun notarytool store-credentials 'profile-name' -k <key> -d <key-id> -i <issuer>
```

The field `<key>` refers to the path to the App Store Connect API Key. Field
`<key-id>` refers to the App Store Connect API Key ID, which is usually 10
alphanumeric characters. The field `<issuer>` refers to the App Store Connect
Issuer ID, which is in UUID format.

It is possible to store a Keychain Profile using the information in Option 2.
Use the following command to do so.

```
xcrun notarytool store-credentials `keychain-profile-name` --apple-id <apple-id> --team-id <team-id> --password <password>
```

The field `<apple-id>` refers to your Apple ID, an email address. Field
`<team-id>` refers to your Team ID, which is usually 10 uppercase alphanumeric
characters. The field `<password>` refers to the an App-Specific Password,
which has the format of 16 lowercase alphabetical characters separated into
groups of 4 characters by hyphens, e.g. `pass-word-goes-here`.

With your Keychain Profile now stored, you may now use PyDeployment while
specifying its name.

```
pydeploy myapp.spec -C 'Developer ID Application: Name Here (TEAMIDHERE)' -K 'profile-name'
```

It is recommended to use an App Store Connect API Key to store a Keychain
Profile, as App-Specific Passwords tend to be more fickle.

## Notarize Without a Stored Keychain Profile

If you do not wish to store your information in a Keychain Profile, you can
feed the information from Option 2 directly to PyDeployment for notarization.

```
pydeploy myapp.spec -C 'Developer ID Application: Name Here (TEAMIDHERE)' -A <apple-id> -T <team-id> -P <password>
```