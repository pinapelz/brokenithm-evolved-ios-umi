# Brokenithm-Evolved-iOS-Umi

A version of [esterTion/Brokenithm-iOS](https://github.com/esterTion/Brokenithm-iOS) but maps inputs to keybinds (for UMIGURI). Uses a WIRED connection with usbmux. Also works on UMIGURI NEXT

Has support for slider LEDs via websockets ([UMIGURI LED Controller Protocol](https://gist.github.com/inonote/00251fed881a82c9df1e505eef1722bc)) so you can get glowy lights if its supported (port 7124)

[![Demo](https://files.catbox.moe/w3564o.png)](https://files.catbox.moe/oz9kos.mp4)

# Usage
You will should first download an iOS client/app. Some options are listed below:
- [OWCramer/Brokenithm-SwiftUI](https://github.com/OWCramer/Brokenithm-SwiftUI) - Shown in demo image. Build from source and sideload the IPA OR Join the TestFlight on the repo's README
- [esterTion/Brokenithm-iOS](https://github.com/esterTion/Brokenithm-iOS) - Build from source or download the IPA [here](https://redive.estertion.win/ipas/Brokenithm-iOS-build-10.ipa) ([backup](https://files.catbox.moe/3zhhn2.ipa)) then sideload

Download the latest built version from Releases. Extract the files into some folder, you should keep all the files in the ZIP together.

Run `Brokenithm-Evolved-iOS-Umi.exe`

**Ensure that UMIGURI is sending LED data on port 7124**

> [!IMPORTANT]  
> You must launch the server before Umiguri. If Umiguri is already opened you will need to restart the game. 

# Config
By default no configuration is required. This application will use UMIGURI's 32-zone keyboard layout. 32-zone input is supported, but you will need to find a client that also supports 32-zones of input (with the exception of air-zones). The default config can be found in `key_config.json`

Due to how the iOS clients above were programmed, the AIR ZONES are out of order due to some IO differences. In the default `key_config.json` this has been adjusted to fix the order when outputting keybinds. However, if for any reason you require the original order then replace the contents `key_config.json` with whats inside `chuniio_key_config.json`
